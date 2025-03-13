import spidev
import lgpio as GPIO
import time
import psutil
from PIL import Image, ImageDraw, ImageFont
import datetime

# SPI Pinleri
DC_PIN = 19
RST_PIN = 13

# GPIO çipini aç
h = GPIO.gpiochip_open(0)
GPIO.gpio_claim_output(h, DC_PIN)
GPIO.gpio_claim_output(h, RST_PIN)

# SPI başlat
spi = spidev.SpiDev(0, 0)
spi.mode = 0
spi.max_speed_hz = 2000000

def reset_display():
    GPIO.gpio_write(h, RST_PIN, 0)
    time.sleep(0.1)
    GPIO.gpio_write(h, RST_PIN, 1)
    time.sleep(0.1)

def send_command(cmd):
    GPIO.gpio_write(h, DC_PIN, 0)
    spi.writebytes([cmd])
    time.sleep(0.001)

def send_data(data):
    GPIO.gpio_write(h, DC_PIN, 1)
    for byte in data:
        spi.writebytes([byte])
        time.sleep(0.0005)

def init_display():
    reset_display()
    send_command(0xAE)
    send_command(0xD5)
    send_command(0x80)
    send_command(0xA8)
    send_command(0x3F)
    send_command(0xD3)
    send_command(0x00)
    send_command(0x40)
    send_command(0x8D)
    send_command(0x14)
    send_command(0x20)
    send_command(0x00)
    send_command(0x00)
    send_command(0x10)
    send_command(0xA1)
    send_command(0xC8)
    send_command(0xDA)
    send_command(0x12)
    send_command(0x81)
    send_command(0x7F)
    send_command(0xD9)
    send_command(0xF1)
    send_command(0xDB)
    send_command(0x40)
    send_command(0xA4)
    send_command(0xA6)
    send_command(0xAF)

def get_cpu_usage():
    return f"CPU Usage: {psutil.cpu_percent()}%"

def get_cpu_temp():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp = int(f.read()) / 1000.0
        return f"CPU Temp: {temp:.1f}C"
    except:
        return "Temp: N/A"

def get_fan_status():
    try:
        with open("/sys/devices/platform/cooling_fan/hwmon/hwmon2/fan1_input", "r") as f:
            rpm = int(f.read().strip())
            return f"Fan: {rpm} RPM"
    except:
        return "Fan: N/A"  # Fan hızını okumak için uygun sensör eklenmelidir

def display_text():
    send_command(0xA4)
    while True:
        image = Image.new("1", (128, 64), color=0)
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()

        now = datetime.datetime.now()
        date_str = now.strftime("%d/%m/%Y")
        time_str = now.strftime("%H:%M:%S")

        draw.text((5, 5), date_str, font=font, fill=255)
        draw.text((5, 20), time_str, font=font, fill=255)
        draw.text((5, 35), get_cpu_usage(), font=font, fill=255)
        draw.text((5, 45), get_cpu_temp(), font=font, fill=255)
        draw.text((5, 55), get_fan_status(), font=font, fill=255)

        pixels = list(image.getdata())
        buffer = []
        for row_block in range(0, 64, 8):
            for col in range(128):
                byte = 0
                for bit in range(8):
                    if pixels[(row_block + bit) * 128 + col] > 0:
                        byte |= (1 << bit)
                buffer.append(byte)
        send_data(buffer)
        time.sleep(1)

try:
    init_display()
    display_text()
except KeyboardInterrupt:
    print("Çıkış yapılıyor...")
finally:
    send_command(0xAE)
    spi.close()
    GPIO.gpio_write(h, DC_PIN, 0)
    GPIO.gpio_write(h, RST_PIN, 0)
    GPIO.gpiochip_close(h)
    print("Ekran kapatıldı ve GPIO temizlendi.")