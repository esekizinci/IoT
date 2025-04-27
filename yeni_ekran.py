import time
import requests
from datetime import datetime
from lcd import drivers

OWM_API_KEY = 'api key'
CITY = 'Vianen,nl'

LAT = 51.975
LON = 5.091

# --- LCD Init ---
display = driver.lcd()

def get_weather():
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={OWM_API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()
        weather = data['weather'][0]['main']
        temp = int(data['main']['temp'])
        # Weather short text conversion
        weather_map = {
            'Clear': 'SUNNY',
            'Clouds': 'CLOUDY',
            'Rain': 'RAIN',
            'Snow': 'SNOW',
            'Drizzle': 'DRIZZL',
            'Thunderstorm': 'STORM',
            'Mist': 'MIST',
            'Fog': 'FOGGY'
        }
        weather_short = weather_map.get(weather, weather[:5].upper())
        return weather_short, temp
    except Exception as e:
        return 'ERROR', 0

def get_sun_times():
    try:
        url = f"https://api.sunrise-sunset.org/json?lat={LAT}&lng={LON}&formatted=0"
        response = requests.get(url)
        data = response.json()
        sunrise_utc = datetime.fromisoformat(data['results']['sunrise'])
        sunset_utc = datetime.fromisoformat(data['results']['sunset'])
        # UTC to local time (Europe/Amsterdam)
        sunrise_local = sunrise_utc.astimezone().strftime('%H:%M')
        sunset_local = sunset_utc.astimezone().strftime('%H:%M')
        return sunrise_local, sunset_local
    except Exception as e:
        return 'ERR', 'ERR'

def show_date_time():
    now = datetime.now()
    date_str = now.strftime('%d-%m-%Y')
    time_str = now.strftime('%H:%M:%S')
    display.lcd_clear()
    display.lcd_display_string(date_str.center(16), 1)
    display.lcd_display_string(time_str.center(16), 2)

def show_weather(weather, temp):
    display.lcd_clear()
    display.lcd_display_string(f'Vianen: {weather}'.ljust(16), 1)
    display.lcd_display_string(f'TEMP: {temp}C'.ljust(16), 2)

def show_sun_times(sunrise, sunset):
    display.lcd_clear()
    display.lcd_display_string(f'SUN↑ {sunrise}'.ljust(16), 1)
    display.lcd_display_string(f'SUN↓ {sunset}'.ljust(16), 2)

if __name__ == '__main__':
    # İlk verileri çek
    weather, temp = get_weather()
    sunrise, sunset = get_sun_times()
    last_update = time.time()

    while True:
        # Verileri her 10 dakika bir güncelle
        if time.time() - last_update > 600:
            weather, temp = get_weather()
            sunrise, sunset = get_sun_times()
            last_update = time.time()

        # 1. Ekran: Tarih ve Saat
        show_date_time()
        time.sleep(10)

        # 2. Ekran: Hava Durumu
        show_weather(weather, temp)
        time.sleep(10)

        # 3. Ekran: Gün Doğumu / Gün Batımı
        show_sun_times(sunrise, sunset)
        time.sleep(10)
