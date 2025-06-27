import yfinance as yf
from forex_python.converter import CurrencyRates, RatesNotAvailableError
from twilio.rest import Client
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import json
import os
import time

# --- CONFIGURATION ---

# Twilio WhatsApp Config from GitHub Secrets
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_WHATSAPP_FROM = os.getenv('TWILIO_WHATSAPP_FROM')
YOUR_WHATSAPP_TO = os.getenv('TWILIO_WHATSAPP_TO')

# Email Config from GitHub Secrets
EMAIL_FROM = os.getenv('EMAIL_FROM')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL_TO = os.getenv('EMAIL_TO')

# JSON file to persist last price
PRICE_FILE = 'last_price.json'

# --- UTILITY FUNCTIONS ---

def get_nvidia_stock_price():
    ticker = yf.Ticker("NVDA")
    todays_data = ticker.history(period='1d')
    last_quote = todays_data['Close'].iloc[-1]
    return round(last_quote, 2)

def convert_usd_to_inr(usd_amount):
    c = CurrencyRates()
    retries = 3
    for attempt in range(retries):
        try:
            inr = c.convert('USD', 'INR', usd_amount)
            return round(inr, 2)
        except RatesNotAvailableError:
            print(f"⚠️ Attempt {attempt+1}: Currency Rates Source Not Ready. Retrying...")
            time.sleep(2)
        except Exception as e:
            print(f"❌ Unexpected error during currency conversion: {e}")
            break
    print("❗ Fallback: Unable to fetch INR rate. Returning None.")
    return None

def send_whatsapp_message(body):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=body,
        from_=TWILIO_WHATSAPP_FROM,
        to=YOUR_WHATSAPP_TO
    )
    print("✅ WhatsApp Sent:", message.sid)

def send_email(subject, html_body):
    msg = MIMEText(html_body, "html")
    msg['Subject'] = subject
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_FROM, EMAIL_PASSWORD)
        smtp.send_message(msg)
        print("✅ Email Sent!")

# --- JSON FILE HANDLER ---

def load_last_price():
    if os.path.exists(PRICE_FILE):
        with open(PRICE_FILE, 'r') as f:
            data = json.load(f)
            return data.get("last_price")
    else:
        with open(PRICE_FILE, 'w') as f:
            json.dump({"last_price": 0}, f)
        return None

def save_last_price(price):
    with open(PRICE_FILE, 'w') as f:
        json.dump({"last_price": price}, f)

# --- MAIN LOGIC ---

def main():
    now = datetime.now().strftime('%d/%m/%Y %I:%M %p')
    stock_name = "NVIDIA (NVDA)"

    # Current prices
    current_price_usd = get_nvidia_stock_price()
    current_price_inr = convert_usd_to_inr(current_price_usd)

    # Fallback if INR is not available
    if current_price_inr is None:
        inr_display = "❌ Not Available"
    else:
        inr_display = f"₹{current_price_inr}"

    # Previous price
    last_price_usd = load_last_price()

    if last_price_usd is None:
        direction_icon = "ℹ️"
        direction = "Initial Check"
        percent_change = "N/A"
    else:
        change = current_price_usd - last_price_usd
        percent_change = f"{(change / last_price_usd) * 100:.2f}%"
        direction_icon = "📈" if change > 0 else "📉" if change < 0 else "🔁"
        direction = f"{direction_icon} {'Increased' if change > 0 else 'Decreased' if change < 0 else 'No Change'}"

    # WhatsApp Message
    whatsapp_message = f"""🔔 NVIDIA Stock Update - {now}

Stock: NVDA
USD: ${current_price_usd}
INR: {inr_display}
Change: {direction_icon} {percent_change}
"""
    send_whatsapp_message(whatsapp_message)

    # Email Message
    subject = f"INDMoney - NVIDIA Stock Price - {now}"
    html_body = f"""
    <p>Hello Karthikeyan,</p>
    <p>🔔 <strong>NVIDIA (NVDA) Stock Update</strong></p>

    <table border="1" cellpadding="6" cellspacing="0" style="border-collapse: collapse; font-family: Arial; font-size: 14px;">
      <tr style="background-color: #f2f2f2;">
        <th>Stock Name</th>
        <th>USD Price</th>
        <th>INR Price</th>
        <th>Change</th>
      </tr>
      <tr>
        <td>NVDA</td>
        <td>${current_price_usd}</td>
        <td>{inr_display}</td>
        <td>{direction_icon} {percent_change}</td>
      </tr>
    </table>

    <p style="color: gray;">Date & Time: {now}</p>
    """
    send_email(subject, html_body)

    # Save price
    save_last_price(current_price_usd)

# --- EXECUTE ---
if __name__ == "__main__":
    main()
