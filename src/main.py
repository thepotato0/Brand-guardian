import pystray,praw,alert,time,sys,threading,logging
from PIL import Image
import config  #  helper script for config.json
class App: 
    def __init__(self):
        self.running = True
        self.icon_image = Image.open("icon.png")
        self.icon = pystray.Icon(
            'shield',
            self.icon_image,
            menu=pystray.Menu(
                pystray.MenuItem("Exit", self.on_clicked)
            )
        )

    def on_clicked(self, icon, item):
        self.running = False  # stop the search loop
        icon.stop()           # stop the tray icon

    def run(self):
        # start the search logic in a background thread
        # this prevents the 'while True' from freezing the tray icon
        self.search_thread = threading.Thread(target=self.continuous_search, daemon=True)
        self.search_thread.start()

        # start the system tray (this blocks the main thread)
        self.icon.run()

    def continuous_search(self):
        """The actual background worker logic"""
        try:
            self.config = config.get_config()
        except FileNotFoundError as e:
            print(e)
            self.icon.stop()
            sys.exit(1)

        creds = self.config['reddit_creds']
        self.notifications = self.config['notifications']
        self.settings = self.config['settings']
        self.keywords = self.settings['keywords']
        self.subreddits = self.settings['subreddits']
        self.logging_config = self.config.get('logging', {})

        self.reddit = praw.Reddit(
            client_id=creds['client_id'],
            client_secret=creds['client_secret'],
            user_agent=creds['user_agent']
        )
        logging.basicConfig(level=self.logging_config.get('log_level', 'INFO'),
                            filename=self.logging_config.get('log_file', 'app.log') if self.logging_config.get('log', False) else None,
                            format='%(asctime)s - %(levelname)s - %(message)s')

        while self.running:
            try:
                self.search()
            except Exception as e:
                logging.error(f"Search error: {e}")
            time.sleep(self.settings.get('check_frequency_seconds', 60))

    def search(self):
        subreddit = self.reddit.subreddit(self.subreddits)
        logging.info("Starting search loop")
        for comment in subreddit.stream.comments(skip_existing=True):
            logging.info(f"Checking comment {comment.id} by {comment.author}")
            if not self.running:
                break
                
            text = comment.body.lower()
            if any(key in text for key in self.keywords):
                logging.info(f"Keyword match found in comment {comment.id}")
                try:
                    alert.Alert(
                        comment.author.name, 
                        comment.body, 
                        f"https://reddit.com{comment.permalink}", 
                        self.notifications,
                    )
                except Exception as e:
                    logging.error(f"Alert error for comment {comment.id}: {e}")

if __name__ == "__main__":
    app = App()
    app.run()
    sys.exit(0)