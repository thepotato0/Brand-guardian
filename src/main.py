import pystray
import praw
import alert
import time
import sys
import threading
import logging
import re
from PIL import Image
import config  # helper script for config.json

def setup_global_logging(log_file="app.log", log_level='INFO'):
    handlers = [logging.StreamHandler(sys.stdout)]
    if log_file:
        handlers.append(logging.FileHandler(log_file))

    logging.basicConfig(
        level=getattr(logging, log_level.upper(), logging.INFO),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=handlers,
        force=True 
    )

class App:
    def __init__(self):
        self.running = True
        
        # 1. Setup Class Logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("Initializing Application...")

        # 2. Load Config File
        try:
            self.config = config.get_config()
            self._parse_config()
        except Exception as e:
            self.logger.critical(f"Failed to load configuration: {e}")
            sys.exit(1)

        # 3. Initialize Reddit Client
        try:
            self.reddit = praw.Reddit(
                client_id=self.creds.get('client_id'),
                client_secret=self.creds.get('client_secret'),
                user_agent=self.creds.get('user_agent')
            )
            self.logger.info(f"Reddit Client Initialized (Read Only: {self.reddit.read_only})")
        except Exception as e:
            self.logger.critical(f"Failed to initialize Reddit client: {e}")
            sys.exit(1)

        # 4. Initialize System Tray
        self.icon_image = Image.open("icon.png")
        self.icon = pystray.Icon(
            'shield',
            self.icon_image,
            menu=pystray.Menu(
                pystray.MenuItem("Exit", self.on_exit)
            )
        )
        self.search_thread = None

    def _parse_config(self):
        self.creds = self.config.get('reddit_creds', {})
        self.notifications = self.config.get('notifications', {})
        self.settings = self.config.get('settings', {})
        self.keywords = self.settings.get('keywords', [])
        self.subreddits = self.settings.get('subreddits', [])

        logging_conf = self.config.get('logging', {})
        if logging_conf.get('log', False):
            setup_global_logging(
                log_file=logging_conf.get('log_file', 'app.log'), 
                log_level=logging_conf.get('log_level', 'INFO')
            )
            self.logger.info("Logging configuration updated from config file.")

    def on_exit(self):
        self.logger.info("Exiting...")
        self.running = False
        if self.icon:
            self.icon.stop()

    def run(self):
        self.logger.info("Starting background search thread...")
        self.search_thread = threading.Thread(target=self.continuous_search, daemon=True)
        self.search_thread.start()

        self.logger.info("Starting System Tray Icon...")
        self.icon.run()

    def continuous_search(self):
        """Background worker loop"""
        check_freq = self.settings.get('check_frequency_seconds', 60)
        
        # Prepare subreddit string once
        if isinstance(self.subreddits, list):
            sub_name = "+".join(self.subreddits)
        else:
            sub_name = str(self.subreddits)

        if not sub_name:
            self.logger.critical("No subreddits configured, Exiting...")
            self.on_exit()
            

        self.logger.info(f"Monitoring subreddits: {sub_name}")

        while self.running:
            try:
                self._stream_comments(sub_name)
            except Exception as e:
                self.logger.error(f"Error in search loop: {e}", exc_info=True)
                # Sleep before retrying to avoid rapid-fire API errors
                time.sleep(check_freq)

    def _stream_comments(self, sub_name):
        subreddit = self.reddit.subreddit(sub_name)
        
        for comment in subreddit.stream.comments(skip_existing=True, pause_after=0):
            if not self.running:
                break
            
            if comment is None:
                continue

            self._process_comment(comment)

    def _process_comment(self, comment):
        try:
            self.logger.info(f"Processing comment {comment.id}...")
            text = comment.body.lower()

            # 1. Check for whole-word matches only using Regex
            matched_keyword = None
            for k in self.keywords:
                # \b ensures "{keyword}" matches but "something{keyword}something" does not
                pattern = rf"\b{re.escape(k.lower())}\b"
                if re.search(pattern, text):
                    matched_keyword = k
                    break
                
            # 2. Only proceed if a match was found
            if matched_keyword:
                author = getattr(comment, 'author', None)
                author_name = getattr(author, 'name', 'unknown') if author else 'unknown'
                self.logger.info(f"MATCH FOUND: '{matched_keyword}' in {comment.id} by {author_name}")

                alert.Alert(
                    author_name,
                    comment.body,
                    comment.permalink,
                    self.notifications,
                )

        except Exception as e:
            self.logger.error(f"Error processing comment {comment.id}: {e}", exc_info=True)

if __name__ == "__main__":
    setup_global_logging() # Initial basic setup
    app = App()
    app.run()