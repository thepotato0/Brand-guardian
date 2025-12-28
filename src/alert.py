from notifypy import Notify
from textblob import TextBlob

def _eval(text):
    return TextBlob(text).sentiment.polarity


def Alert(comment_author, comment_body, comment_permalink, notifications, matched_keyword):
    
    message = f"{comment_author} has a {"positive" if _eval(comment_body) > 0 else "negative"} opinion about {matched_keyword}!:\n{comment_body[:100]}...\nLink: {comment_permalink}"

    if notifications.get("desktop_alerts", False): 
        notification = Notify()
        notification.title = "BrandGuardian Alert"
        notification.message = message
        notification.icon = "icon.png"  
        notification.send()
    if notifications.get("email_alerts", False):
        # Placeholder for email alert logic
        pass
    if notifications.get("sms_alerts", False):
        # Placeholder for SMS alert logic
        pass