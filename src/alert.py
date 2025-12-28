from notifypy import Notify

def Alert(comment_author, comment_body, comment_permalink, notifications):
    
    link = f"https://reddit.com{comment_permalink}"
    message = f"New mention by {comment_author}:\n{comment_body[:100]}..."

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
