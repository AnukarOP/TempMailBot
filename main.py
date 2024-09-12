import os
import requests
import asyncio
import random
from telethon import TelegramClient, events, Button
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_ID = os.getenv("API_ID") #Get this from my.telegram.org
API_HASH = os.getenv("API_HASH") #Get this from my.telegram.org
BOT_TOKEN = os.getenv("BOT_TOKEN") #Get this from @Botfather
TEMPMAIL_API_KEY = os.getenv("TEMPMAIL_API_KEY")
NAMESPACE = os.getenv("NAMESPACE")

EMAIL_DOMAIN = "@inbox.testmail.app"

client = TelegramClient('TempMailBot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

user_data = {}

def generate_random_email():
    random_name = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz1234567890', k=6))
    return f"{NAMESPACE}.{random_name}{EMAIL_DOMAIN}"

def generate_custom_email(keyword):
    return f"{NAMESPACE}.{keyword}{EMAIL_DOMAIN}"

def get_inbox(email):
    url = f"https://api.testmail.app/api/json?apikey={TEMPMAIL_API_KEY}&namespace={NAMESPACE}&pretty=true"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["emails"]
    return []

async def auto_refresh_inbox(user_id, email):
    while True:
        await asyncio.sleep(300)
        emails = get_inbox(email)
        if emails:
            await client.send_message(user_id, f"📨 **New email!** You have {len(emails)} new message(s).")
        else:
            await client.send_message(user_id, "📬 No new emails yet.")

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    user_id = event.sender_id
    
    await event.respond(
        f"👋 **Hello!** Welcome to TempMail Bot.\n\nYou can generate a random email or create your custom email.\n\nUse the buttons below to proceed.",
        buttons=[
            [Button.inline("🔀 Generate Random Email", data="generate_random")],
            [Button.inline("📝 Create Custom Email", data="create_custom")]
        ]
    )

@client.on(events.CallbackQuery)
async def handle_callback(event):
    user_id = event.sender_id

    if event.data == b"generate_random":
        email = generate_random_email()
        user_data[user_id] = {
            "email": email,
            "inbox": []
        }
        asyncio.create_task(auto_refresh_inbox(user_id, email))
        await event.edit(
            f"🎉 **Random email generated:**\n\n`📧 {email}`\n\nYou can now check your inbox.",
            buttons=[
                [Button.inline("📥 Check Inbox", data="check_inbox")],
                [Button.inline("🔀 Generate Another", data="generate_random")],
                [Button.inline("📝 Create Custom Email", data="create_custom")]
            ]
        )

    elif event.data == b"create_custom":
        user_data[user_id] = {"state": "awaiting_keyword"}
        await event.edit(
            f"📝 **Please send the custom keyword** you'd like to add to the email in the format:\n\n`{NAMESPACE}.[your_keyword]@inbox.testmail.app`\n\nJust send your desired keyword now!"
        )

    elif event.data == b"check_inbox":
        if user_id in user_data and "email" in user_data[user_id]:
            email = user_data[user_id]["email"]
            emails = get_inbox(email)
            user_data[user_id]["inbox"] = emails

            if emails:
                buttons = []
                for idx, email_data in enumerate(emails):
                    buttons.append([Button.inline(f"📧 Email {idx + 1}: {email_data['subject']}", data=f"view_email_{idx}")])

                await event.edit(
                    f"📬 **Inbox for** `{email}`\nYou have {len(emails)} email(s).",
                    buttons=buttons
                )
            else:
                await event.edit("📭 Your inbox is empty.")
        else:
            await event.edit("❌ No email found. Please generate one first.")

    elif event.data.startswith(b"view_email_"):
        email_idx = int(event.data.decode('utf-8').split("_")[-1])
        inbox = user_data[user_id]["inbox"]
        selected_email = inbox[email_idx]

        from_email = selected_email["from"]
        subject = selected_email["subject"]
        body = selected_email["text"]

        await event.edit(
            f"**From**: `{from_email}`\n"
            f"**Subject**: `{subject}`\n\n"
            f"**Message**:\n`{body}`\n",
            buttons=[[Button.inline("🔙 Back to Inbox", data="check_inbox")]]
        )

@client.on(events.NewMessage)
async def handle_keyword(event):
    user_id = event.sender_id
    if user_id in user_data and user_data[user_id].get("state") == "awaiting_keyword":
        keyword = event.text.strip()
        if len(keyword) > 0:
            email = generate_custom_email(keyword)
            user_data[user_id] = {
                "email": email,
                "inbox": []
            }
            asyncio.create_task(auto_refresh_inbox(user_id, email))
            await event.respond(
                f"🎉 **Custom email created:**\n\n`📧 {email}`\n\nYou can now check your inbox.",
                buttons=[
                    [Button.inline("📥 Check Inbox", data="check_inbox")],
                    [Button.inline("🔀 Generate Random Email", data="generate_random")],
                    [Button.inline("📝 Create Another Custom", data="create_custom")]
                ]
            )
        else:
            await event.respond("❌ **Invalid keyword.** Please try again.")

client.start()
client.run_until_disconnected()
