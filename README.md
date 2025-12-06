# 🛡️ Secure-OS: AI-Powered Smart Security System

**Secure-OS** — bu Raspberry Pi va shaxsiy kompyuterlar uchun mo'ljallangan, sun'iy intellekt (AI) va Computer Vision texnologiyalariga asoslangan zamonaviy video kuzatuv tizimi.

Loyiha **YOLOv8** neyron tarmog'idan foydalanib, real vaqt rejimida insonlarni aniqlaydi, "Cyberpunk" uslubidagi adaptiv interfeys orqali xavf haqida ogohlantiradi va avtomatik ravishda video yozib oladi.

---

## 📸 Screenshots

| **Safe Mode (Tinch Holat)** | **Intruder Mode (Xavf)** |
|:---:|:---:|
| ![Safe Mode](https://via.placeholder.com/400x250/00f3ff/000000?text=System+Safe+UI) | ![Danger Mode](https://via.placeholder.com/400x250/ff003c/000000?text=Intruder+Detected!) |
| *Tizim barqaror, UI rangi: Cyan* | *Xavf aniqlandi, UI rangi: Qizil, Sirena yoqilgan* |

---

## ✨ Asosiy Imkoniyatlar

* **🧠 AI Object Detection:** YOLOv8 yordamida odamlar ("Person") va boshqa obyektlarni 95%+ aniqlikda topadi.
* **🚨 Smart Alarm System:** O'g'ri (Intruder) aniqlanganda avtomatik sirena chalinadi va interfeys qizil rangga kiradi.
* **🎥 Intelligent DVR:** Faqat harakat yoki odam aniqlanganda video yozadi (Disk joyini tejash uchun).
* **📱 Mobile Responsive:** Telefon, planshet va kompyuter ekranlariga to'liq moslashuvchan Cyberpunk interfeys.
* **🎛️ Masofaviy Boshqaruv:**
    * Yorug'lik (Brightness) va Kontrastni o'zgartirish.
    * FPS (Frame Rate) ni boshqarish (Internetni tejash uchun).
    * AI va Sirena funksiyalarini yoqish/o'chirish.
* **📊 Tizim Monitoringi:** CPU, RAM va Disk holatini real vaqtda grafik ko'rinishida kuzatish.
* **🔒 Xavfsiz Kirish:** Parol bilan himoyalangan Login tizimi.
* **🌍 Remote Access:** Ngrok orqali dunyoning istalgan nuqtasidan ulanish imkoniyati.

---

## 🛠️ O'rnatish (Installation)

### 1. Talablar (Prerequisites)
* **Hardware:** Raspberry Pi 4/5 yoki Windows/Linux Laptop (Web kamera bilan).
* **Software:** Python 3.8+

### 2. Loyihani yuklab olish
```bash
git clone [https://github.com/xemis-dev/secure-os.git](https://github.com/xemis-dev/secure-os.git)
cd secure-os

