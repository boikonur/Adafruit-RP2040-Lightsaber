# 🌟 Adafruit-RP2040-Lightsaber aka  Pythosaber
**🐍Pythonsaber** is a lightweight, kid-friendly CircuitPython lightsaber project designed to be approachable for beginners, yet packed with techniques used by professional lightsaber ecosystems like ProffieOS!

---

## ✅ Features:

- Continuous **hum sound loop**
- **Dynamic swing & clash sound mixing** (smooth audio, no interruption)
- **Simple blade ignition & retraction** with sound + light fade effects
- **LIS3DH accelerometer-based** swing/clash detection
- **Button-controlled Power ON/OFF**, debounced for reliability
- **External Power Enable pin supported**
- Clean, non-blocking logic → no freezes even under rapid swings/hits
- Simple hardware: **Adafruit Feather RP2040 PropMaker + NeoPixel strip*
    Follow the guide how to create the hardware example here: https://learn.adafruit.com/lightsaber-rp2040/

---

## **Why it’s great for kids, makers and young engineers:**

While projects like **ProffieOS** offer extreme configurability and realism, they come with a learning curve (complex configuration files, abstract C++ coding).

**🐍Pythonsaber**:

|                    | **🐍Pythonsaber (CircuitPython)**              | **Proffieboard + ProffieOS**          |
|--------------------|--------------------------------------------|--------------------------------------|
| Simplicity         | 🟢 Clean Python code, easy for beginners    | 🔴 Requires complex C++ knowledge|
| Customization      | 🟢 Change sounds, behaviors directly in code| 🟢 Highly customizable, but complex   |
| Stability          | 🟢 Simple & stable                          | 🟢 Stable, but config errors are common   |
| Hardware Cost      | 🟢 Affordable (RP2040 + NeoPixels)          | 🔴 Bit more pricey Proffieboard hardware |
| Advanced Features  | 🔴 Basic lightsaber logic                        | 🟢 SmoothSwing, blade styles, etc.    |

---

## 🚀 **Future Plans:**

- 🎯 **Pure SmoothSwing v2-style blending** → Advanced gyro-based swing modulation
- 🔥 **Gyroscope integration (LSM6DSOX)** for precise angle & strength detection (https://www.adafruit.com/product/4438)
- 🎛️ **Custom blade effects & colors** (flicker, rainbow, flash-on-clash)
- 📀 **Sound font swapping** → Multiple profiles (depends on memmory)
- 💾 Optional **SD card support** for more sound files
- 📡 Add **wireless (BLE/WiFi) control panel** to tweak settings live!

---

## 🔧 **Built For:**

- Young padawans who want to learn & tinker
- Makers who want a lightsaber without diving into C++ or complex firmware
- Hobbyists looking to extend & experiment without limitations

---

## 🔊 **NOTE:**
This build benefits from **higher quality speakers** for optimal sound output. For best results, we recommend pairing this setup with a high-quality speaker that can properly handle sound at a higher volume.

For 3D printing upgrades, check out the [Adafruit RP2040 Lightsaber Upgrades on Printables](https://www.printables.com/model/1231510-adafruit-rp2040-lightsaber-upgrades).

---

**takes just 10 minutes to setup the hardware, and run the code**  



