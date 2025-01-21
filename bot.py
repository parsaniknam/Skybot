import telegram
from flask import Flask, request
import requests

app = Flask(__name__)

# توکن ربات تلگرام
bot_token = '8003753624:AAG7xmi83PlCI3eNSJlQAFljdDagsM0uzlI'
bot = telegram.Bot(token=bot_token)

# کلید API برای OpenWeatherMap
weather_api_key = '2f4ed9a4ec7dcd51e6bad438e3d356a0'

# مسیر Webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        chat_id = update.message.chat.id
        text = update.message.text

        # پردازش پیام کاربر
        if text.lower() == "start" or text.lower() == "/start":
            bot.send_message(chat_id, "سلام! برای دریافت اطلاعات آب و هوا نام شهر را وارد کنید.")
        elif "5 روز" in text:
            city = text.replace("5 روز", "").strip()
            response = get_weather_forecast(city, 5)
            bot.send_message(chat_id, response)
        elif "10 روز" in text:
            city = text.replace("10 روز", "").strip()
            response = get_weather_forecast(city, 10)
            bot.send_message(chat_id, response)
        else:
            response = get_current_weather(text)
            bot.send_message(chat_id, response)

        return 'OK'


# دریافت آب و هوای فعلی
def get_current_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric&lang=fa"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        description = data['weather'][0]['description']
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        return f"آب و هوای {city}:\nوضعیت: {description}\nدمای فعلی: {temp}°C\nاحساس واقعی: {feels_like}°C"
    else:
        return "شهر موردنظر پیدا نشد. لطفاً نام شهر را درست وارد کنید."


# دریافت پیش‌بینی آب و هوا
def get_weather_forecast(city, days):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={weather_api_key}&units=metric&lang=fa"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        forecasts = data['list'][:days * 8]  # هر روز 8 داده 3 ساعته دارد
        forecast_text = f"پیش‌بینی {days} روز آینده برای {city}:\n"
        for forecast in forecasts:
            time = forecast['dt_txt']
            description = forecast['weather'][0]['description']
            temp = forecast['main']['temp']
            forecast_text += f"{time}: {description}, {temp}°C\n"
        return forecast_text
    else:
        return "شهر موردنظر پیدا نشد. لطفاً نام شهر را درست وارد کنید."


@app.route('/')
def index():
    return "ربات تلگرام شما در حال اجراست."


if __name__ == '__main__':
    bot.set_webhook(url='https://your-app-name.onrender.com/webhook')
    app.run(host='0.0.0.0', port=5000)