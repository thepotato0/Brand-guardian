import json

from sympy import true
def get_config():
    # check for config.json if not found create one and return with error and exit
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
            return config
    except FileNotFoundError:
        default_config = {
                "reddit_creds": {
                    "client_id": "YOUR_ACTUAL_ID",
                    "client_secret": "YOUR_ACTUAL_SECRET",
                    "user_agent": "BrandGuardian v1.0 by /u/YourRedditUsername"
                },
                "settings": {
                    "keywords": ["your_product", "your_brand", "your_service"],
                    "subreddits": "apple",
                    "min_sentiment_threshold": 0.2,
                    "check_frequency_seconds": 180
                },
                "notifications": {
                    "sms_alerts": True,
                    "email_alerts": True,
                    "desktop_alerts": True
                },
                "logging": {
                    "log": True,
                    "log_file": "app.log",
                    "log_level": "INFO"
                }
}
        with open("config.json", "w") as f:
            json.dump(default_config, f, indent=4)
        raise FileNotFoundError("config.json not found. A default config file has been created. Please update it with your settings and restart the application.")