import os
import requests
import smtplib
from email.mime.text import MIMEText

API_KEY = os.getenv("OPENWEATHER_API_KEY")
EMAIL = os.getenv("EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
TO_EMAIL = os.getenv("TO_EMAIL")

CITY = "Kochi"

url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
data = requests.get(url).json()

temp = data["main"]["temp"]
weather = data["weather"][0]["main"].lower()

alert = False
message = ""

if temp > 35:
    alert = True
    message += f"🔥 High temperature: {temp}°C\n"

if "rain" in weather:
    alert = True
    message += f"🌧 Rain expected: {weather}\n"

def send_email(msg):
    email = MIMEText(msg)
    email["Subject"] = f"Weather Alert for {CITY}"
    email["From"] = EMAIL
    email["To"] = TO_EMAIL

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL, EMAIL_PASSWORD)
    server.send_message(email)
    server.quit()

if alert:
    send_email(message)
    print("Alert sent!")
else:
    print("Weather is normal.")
