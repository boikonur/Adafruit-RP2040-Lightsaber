import board
import audiobusio
import audiocore
import audiomixer
import time
import busio
from digitalio import DigitalInOut, Direction, Pull
from adafruit_debouncer import Button
import adafruit_lis3dh
import neopixel
import math
import random
import os

print("Booting...")

# === External Power ON === #
external_power = DigitalInOut(board.EXTERNAL_POWER)
external_power.direction = Direction.OUTPUT
external_power.value = True

# === Audio Setup === #
audio = audiobusio.I2SOut(board.I2S_BIT_CLOCK, board.I2S_WORD_SELECT, board.I2S_DATA)

mixer = audiomixer.Mixer(
    voice_count=2,
    sample_rate=22050,
    channel_count=1,
    bits_per_sample=16,
    samples_signed=True
)
audio.play(mixer)

# === Accelerometer === #
i2c = busio.I2C(board.SCL, board.SDA)
lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, address=0x18)
lis3dh.range = adafruit_lis3dh.RANGE_2_G

# === NeoPixels Blade === #
num_pixels = 100
blade = neopixel.NeoPixel(board.EXTERNAL_NEOPIXELS, num_pixels, auto_write=False)
blade.brightness = 0.8

# Blade color list for cycling
blade_colors = [(0, 125, 255), (0, 255, 0), (255, 0, 0), (255, 255, 0)]  # Cyan, Green, Red, Yellow
current_color_index = 0
blade_color = blade_colors[current_color_index]

# === Button === #
button_pin = DigitalInOut(board.EXTERNAL_BUTTON)
button_pin.direction = Direction.INPUT
button_pin.pull = Pull.UP
button = Button(button_pin)

# === Sounds === #
swing_sounds = []
clash_sounds = []

for filename in os.listdir("/sounds"):
    if filename.lower().startswith("swing") and filename.lower().endswith(".wav"):
        swing_sounds.append("/sounds/" + filename)
    if filename.lower().startswith("clash") and filename.lower().endswith(".wav"):
        clash_sounds.append("/sounds/" + filename)

swing_sounds.sort()
clash_sounds.sort()

hum_wave = open("/sounds/hum.wav", "rb")
hum = audiocore.WaveFile(hum_wave)

# === Parameters === #
SWING_THRESHOLD = 15
CLASH_THRESHOLD = 20

DISABLE_CLASH = False  # Enable/disable clash events

power_on = False
fade_step = 0
fade_active = False

# Button press timing
BUTTON_LONG_PRESS_DURATION = 0.5  # Seconds
button_pressed_time = None
long_press_handled = False

# === Functions === #
def blade_on_animation():
    for i in range(num_pixels):
        blade[i] = blade_color
        blade.show()
        time.sleep(0.002)

def start_power_on():
    global power_on
    wave_file = open("/sounds/poweron.wav", "rb")
    poweron = audiocore.WaveFile(wave_file)
    mixer.voice[1].play(poweron, loop=False)
    mixer.voice[1].level = 1.0
    blade_on_animation()
    mixer.voice[0].play(hum, loop=True)
    mixer.voice[0].level = 0.9
    power_on = True

def start_power_off():
    global power_on
    power_on = False

    # Stop hum
    mixer.voice[0].stop()

    # Play power-off sound
    wave_file = open("/sounds/poweroff.wav", "rb")
    poweroff = audiocore.WaveFile(wave_file)
    mixer.voice[1].play(poweroff, loop=False)
    mixer.voice[1].level = 1.0

    # Blocking fade animation
    for step in range(num_pixels - 1, -1, -1):
        brightness_factor = step / (num_pixels - 1)
        r = int(blade_color[0] * brightness_factor)
        g = int(blade_color[1] * brightness_factor)
        b = int(blade_color[2] * brightness_factor)
        blade[step] = (r, g, b)
        blade.show()
        time.sleep(0.002)

    blade.fill((0, 0, 0))
    blade.show()

def trigger_swing():
    if not mixer.voice[1].playing and power_on:
        sound_file = random.choice(swing_sounds)
        wave_file = open(sound_file, "rb")
        swing = audiocore.WaveFile(wave_file)
        mixer.voice[1].play(swing, loop=False)
        mixer.voice[1].level = 1.0
        print(f"Swing: {sound_file}")

def trigger_clash():
    if not mixer.voice[1].playing and power_on and not DISABLE_CLASH:
        sound_file = random.choice(clash_sounds)
        wave_file = open(sound_file, "rb")
        clash = audiocore.WaveFile(wave_file)
        mixer.voice[1].play(clash, loop=False)
        mixer.voice[1].level = 1.0
        print(f"Clash: {sound_file}")
        # Flash white
        blade.fill((255, 255, 255))
        blade.show()
        time.sleep(0.3)
        # Restore color
        blade.fill(blade_color)
        blade.show()

def change_blade_color():
    global current_color_index, blade_color
    current_color_index = (current_color_index + 1) % len(blade_colors)
    blade_color = blade_colors[current_color_index]
    print(f"Blade color changed: {blade_color}")
    if power_on:
        blade.fill(blade_color)
        blade.show()

# === Main Loop === #
while True:
    button.update()

    # Button pressed
    if button.fell:
        button_pressed_time = time.monotonic()
        long_press_handled = False

    # Button held → check long press
    if button.value == False and button_pressed_time is not None:
        press_duration = time.monotonic() - button_pressed_time
        if press_duration >= BUTTON_LONG_PRESS_DURATION and not long_press_handled:
            print("Long Press Detected!")
            change_blade_color()
            long_press_handled = True

    # Button released → check short press
    if button.rose:
        press_duration = time.monotonic() - button_pressed_time
        if press_duration < BUTTON_LONG_PRESS_DURATION and not long_press_handled:
            print("Short Press Detected!")
            if not power_on:
                start_power_on()
            else:
                start_power_off()

        button_pressed_time = None
        long_press_handled = False

    # Swing/Clash detection
    if power_on:
        x, y, z = lis3dh.acceleration
        accel_mag = math.sqrt(x * x + y * y + z * z)
        if accel_mag > CLASH_THRESHOLD:
            trigger_clash()
        elif accel_mag > SWING_THRESHOLD:
            trigger_swing()

    time.sleep(0.005)
