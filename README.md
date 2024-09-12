# Telegram CC Scraper Bot 🚀

This Telegram bot allows users to generate temporary email addresses, check inboxes, and retrieve email messages directly through Telegram. The bot interacts with the TempMail API to provide a seamless, user-friendly experience, including options to create random or custom email addresses. This bot is intended for educational purposes only and should not be used for any illegal activities.

## Features

- Generate random or custom temporary email addresses.
- Automatically checks inboxes for new emails every 5 minutes and notifies the user if any emails are received.
- Allows users to view email content directly in Telegram.
- Provides easy navigation with inline buttons for inbox checking and email generation.
- Simple and user-friendly interface with emoji support.

## Installation

1. Clone this repository:

```bash
git clone https://github.com/AnukarOP/TempMailBot
cd TempMailBot
```

2. Install the required Python libraries:

```bash
pip install -r requirements.txt
```

3. Open the `.env.example` file in your preferred text editor:

```bash
nano .env.example
```

4. Replace the placeholder values with your actual `API_ID`, `API_HASH`, `BOT_TOKEN`, `TEMPMAIL_API_KEY` and `NAMESPACE`. Once you're done, save the file (**Ctrl + O** in nano, then **Enter**) and Rename the file to `.env`:

```bash
mv .env.example .env
```
## Configuration

```
API_ID: Your Telegram API ID from my.telegram.org.
API_HASH: Your Telegram API hash from my.telegram.org.
BOT_TOKEN: The token you receive from @BotFather on Telegram.
TEMPMAIL_API_KEY: Your TempMail API key from testmail.app.
NAMESPACE: The namespace assigned to you by TempMail (e.g., hyuy).
```

## Usage

1. Start the bot:

```bash
python3 main.py &
```

2. The bot will start and wait for users to interact. Users can generate temporary email addresses, check inboxes, and view email content directly through the bot.

## Disclaimer

This bot is meant for educational purposes only. The use of this bot for illegal activities such as unauthorized access to information or email fraud is strictly prohibited. The authors do not take any responsibility for any misuse of this bot.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

<p align="center">
  <a href="https://github.com/AnukarOP" target="_blank">
    <img src="https://img.shields.io/badge/Made%20with%20%E2%9D%A4%20by-AnukarOP-%23FF0000.svg" alt="Made with love by AnukarOP"/>
  </a>
</p>
