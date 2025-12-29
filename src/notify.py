from notifypy import Notify as Notify_
from textblob import TextBlob
import yagmail
from twilio.rest import Client

def _eval(text):
    return TextBlob(text).sentiment.polarity


def Notify(comment_author, comment_body, comment_permalink, notifications, matched_keyword,logger,EMAIL_USER,EMAIL_PASS,TARGET_EMAIL,TWILIO_SID,TWILIO_AUTH_TOKEN,TWILIO_PHONE,TARGET_PHONE):
    
    message = f"{comment_author} has a {"positive" if _eval(comment_body) > 0 else "negative"} opinion about {matched_keyword}!:\n{comment_body[:100]}...\nLink: {comment_permalink}"

    if notifications.get("desktop", False): 
        notification = Notify_() # from notifypy
        notification.title = "BrandGuardian Notification"
        notification.message = message
        notification.icon = "icon.png"
        try:
            notification.send()
        except Exception as e:
            logger.error(f"Failed to send desktop notification: {e}", exc_info=True)

    if notifications.get("emails", False):
        try:
            yag = yagmail.SMTP(EMAIL_USER, EMAIL_PASS)
            yag.send(
                to=TARGET_EMAIL,
                subject=f"Brand Alert: mention of {matched_keyword}",
                contents=message
            )
        except Exception as e:
            logger.error(f"Failed to send email notification: {e}", exc_info=True)
    if notifications.get("sms", False):
        try:
            client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
            client.messages.create(
                body=f"BrandGuardian: {message[:140]}", # SMS length limit
                from_=TWILIO_PHONE,
                to=TARGET_PHONE
            )
        except Exception as e:
            print(f"SMS failed: {e}")