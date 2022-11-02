# Author: Tegan Hakim
# Build: pyinstaller --onefile "main.py"

# Import API and environment libraries
import vonage
from dotenv import load_dotenv
import os

# Initialize environment variables
load_dotenv()

def send_sms(client_list, message, type="text"):
    # Setup Vonage Client Rest API
    client = vonage.Client(key=os.getenv("CLIENT_API_KEY"), secret=os.getenv("SECRET_API_KEY"))
    sms = vonage.Sms(client)

    # Send a SMS message to all recipients
    for client in client_list:
        print(client)
        responseData = sms.send_message(
            {
                "from": os.getenv('VIRTUAL_NUMBER'),
                "to": "1" + client, # 1+ is required for US numbers
                "text": message,
                "type": type,
            }
        )

        # Check for errors
        if responseData["messages"][0]["status"] != "0":
            return f"Message failed with error: {responseData['messages'][0]['error-text']}"
    return "Message sent successfully."