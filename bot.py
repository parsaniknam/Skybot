import requests
from flask import Flask, request

# ساخت اپلیکیشن Flask برای Webhook
app = Flask(__name__)

# توکن ربات تلگرام شما
YOUR_BOT_TOKEN = '8003753624:AAG7xmi83PlCI3eNSJlQAFljdDagsM0uzlI'

# URL Webhook رندر
YOUR_WEBHOOK_URL = 'https://skybot-z93c.onrender.com/webhook'

# تابع برای تنظیم Webhook
def set_webhook():
    webhook_url = f'https://api.telegram.org/bot{YOUR_BOT_TOKEN}/setWebhook?url={YOUR_WEBHOOK_URL}'
    response = requests.get(webhook_url)
    print(response.text)  # نمایش پاسخ

# تنظیم Webhook به محض راه‌اندازی اپلیکیشن
set_webhook()

# روت Webhook که پیام‌ها رو دریافت می‌کنه
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()  # دریافت داده‌ها از تلگرام
    chat_id = data['message']['chat']['id']  # دریافت شناسه چت
    message = data['message']['text']  # دریافت متن پیام

    # ارسال پیام به کاربر
    send_message(chat_id, message)
    return "OK", 200

# تابع ارسال پیام به تلگرام
def send_message(chat_id, message):
    url = f'https://api.telegram.org/bot{YOUR_BOT_TOKEN}/sendMessage'
    params = {
        'chat_id': chat_id,
        'text': f'پیام شما: {message}'
    }
    response = requests.get(url, params=params)
    print(response.text)  # نمایش پاسخ ارسال پیام

# اجرای اپلیکیشن Flask
if __name__ == '__main__':
    app.run(port=5000)