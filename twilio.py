from twilio.rest import Client
from dotenv import load_dotenv
import os
load_dotenv()

# Your Account SID and Auth Token from console.twilio.com
account_sid = os.getenv('ACCOUNT_SID')
auth_token  = os.getenv("AUTH_TOKEN")

client = Client(account_sid, auth_token)

message = client.messages.create(
    to="whatsapp:+31645421019",
    from_="whatsapp:+14155238886",
    body="Hello from Python!")

print(message.sid)