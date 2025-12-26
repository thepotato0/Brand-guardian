from win10toast_click import ToastNotifier
import webbrowser

def Alert(comment_author, comment_body, comment_permalink, notifications):
    if not notifications.get("desktop_alerts", False):
        return

    link = f"https://reddit.com{comment_permalink}"
    message = f"New mention by {comment_author}:\n{comment_body[:100]}...\n\n{link}"
    if notifications.get("desktop_alerts", False):
        if len(message) > 300:
            message = message[:297] + "..."
        toaster = ToastNotifier()
        toaster.show_toast(
            title="BrandGuardian Alert",
            msg=message,
            duration=10,
            callback_on_click=lambda: webbrowser.open(link),
            icon_path="icon.png"
        )

    if notifications.get("sms_alerts", False):
        pass

    if notifications.get("email_alerts", False):
        pass
