import base64
import json
import requests
import functions_framework

# This is your Google Chat webhook URL.
# It's hardcoded here for simplicity, but in a production environment,
# you should use an environment variable for security.
WEBHOOK_URL = "URL WebHook"

# Use a global flag to ensure the 'ready' notification is sent only once.


def send_notification(message):
    """Sends a message to the configured webhook URL."""
    try:
        response = requests.post(WEBHOOK_URL, json={"text": message})
        response.raise_for_status()
        print("Notification sent successfully.")
    except Exception as e:
        print(f"Failed to send notification: {e}")

@functions_framework.cloud_event
def billing_webhook_handler(cloud_event):
    """
    Handles incoming Pub/Sub messages from GCP budget alerts.
    The function name here must match the 'Function entry point' in the UI.
    """

    try:
        # Get the Pub/Sub message data from the CloudEvent
        message = cloud_event.data.get("message")
        if not message or "data" not in message:
            print("Invalid Pub/Sub message format.")
            return

        # Decode the base64-encoded message data
        pubsub_data = base64.b64decode(message["data"]).decode("utf-8")
        billing_data = json.loads(pubsub_data)

        # Build a simplified message for Google Chat.
        message_text = ("This is a notification from the Pub/Sub notification channel")
        
        send_notification(message_text)
        
        return "OK"

    except Exception as e:
        print(f"Error processing webhook: {e}")
        return "Error"
