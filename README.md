# 📈 NVIDIA Stock Price Alert Bot (via Email + WhatsApp)

Automatically tracks NVIDIA (NVDA) stock price every 3 hours and sends personalized alerts:
- ✅ Email (with USD & INR pricing in table format)
- ✅ WhatsApp Notification using Twilio
- ✅ Runs automatically using GitHub Actions

---

## 🛠 Features

- Tracks **NVIDIA (NVDA)** stock in USD
- Converts price to **INR** (₹)
- Calculates **percentage change** since last check
- Sends formatted:
  - 📧 **Email**
  - 💬 **WhatsApp**
- Built with:
  - `yfinance`
  - `forex-python`
  - `twilio`
  - GitHub Actions
- Runs **every 3 hours** using a CRON job

---

## 🚀 How It Works

| Step | Action |
|------|--------|
| 🕒 1 | GitHub Actions runs every 3 hours |
| 💹 2 | Fetches NVDA stock price (USD) using `yfinance` |
| 🔁 3 | Converts to INR using `forex-python` |
| 📉 4 | Compares with last known price (stored in JSON) |
| 🔔 5 | Sends alerts via email and WhatsApp |

---

## 📊 Live NVIDIA Stock Dashboard

> ℹ️ This value is updated every 3 hours by the automation script.

| Stock | USD Price | INR Price | Last Change |
|-------|-----------|-----------|--------------|
| NVDA  | ![USD](https://img.shields.io/badge/dynamic/json?color=blue&label=USD&query=last_price&url=https://raw.githubusercontent.com/Karthikeyan01V/nvdia-stock-alert-bot/blob/main/last_price.json) | Auto-calculated | % change in email |

---

## 👁️ Repo Traffic & Insights

![Repo Views](https://komarev.com/ghpvc/?username=Karthikeyan01V&label=Repo+Views&color=brightgreen)
![Stars](https://img.shields.io/github/stars/Karthikeyan01V/nvdia-stock-alert-bot?style=social)
![Forks](https://img.shields.io/github/forks/Karthikeyan01V/nvdia-stock-alert-bot?style=social)

---

## 📥 Setup Instructions (If You Want to Fork/Use)

1. Fork this repo
2. Add the following **GitHub Secrets**:
   - `TWILIO_ACCOUNT_SID`
   - `TWILIO_AUTH_TOKEN`
   - `TWILIO_WHATSAPP_FROM`
   - `TWILIO_WHATSAPP_TO`
   - `EMAIL_FROM`
   - `EMAIL_PASSWORD`
   - `EMAIL_TO`
3. GitHub Actions will run every 3 hours

---

## 🙋‍♂️ Author

Made with ❤️ by [Karthikeyan V ](https://github.com/Karthikeyan01V)

---

## ☕ Like This Project?

Give it a ⭐ and share it!
