import csv

import requests
from bs4 import BeautifulSoup


def send_telegram_message(message, chat_id, token):
    """
    Sends a message to a specified Telegram chat using a bot.
    :param message: The message to send.
    :param chat_id: The chat ID to send the message to.
    :param token: Your Telegram bot token.
    """
    url = f"https://api.telegram.org/bot{token}/sendMessage"  # Ensure your token is correctly formatted here
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }
    response = requests.post(url, data=payload)
    return response.json()


bot_token = ''  # Example token, replace with yours
chat_id = ''  # Replace 'YOUR_CHAT_ID' with your actual chat ID

# Initialize an empty list to collect headlines
headlines = []

with open('scraped_news_titles.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # Write the header row
    writer.writerow(['Headline'])

    # Make a request to TechCrunch
    page_to_scrape = requests.get("https://techcrunch.com")
    soup = BeautifulSoup(page_to_scrape.text, 'html.parser')

    # Find all article titles using the 'h2' tag, you might need to adjust the class name
    article_titles = soup.findAll('h2')

    # Iterate over the list and write their text content to the CSV file
    for title in article_titles:
        headline = title.text.strip()
        print(headline)
        headlines.append(headline)
        writer.writerow([headline])

# Construct a message with the headlines
message = "\n".join(headlines[:10])  # Sending only the first 10 headlines for brevity
send_telegram_message(message, chat_id, bot_token)
