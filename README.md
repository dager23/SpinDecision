# 🎡 Spin the Wheel – Decision Maker (Streamlit App)

A fun, interactive **decision-making web app** built with **Streamlit + Plotly**.  
Users can enter multiple choices, spin a roulette-style wheel, and let fate decide ✨

This app features **realistic spin physics**, **audio playback**, a **fixed arrow pointer**, and a **clear winning highlight**.

---

## 🚀 Features

- 🎯 **Spin-the-wheel decision maker**
- 🔢 Choose **2–8 options**
- 📝 Custom text for each option
- 🌀 **Smooth 8-second spin** with realistic slow-down (ease-out physics)
- 🧭 **Fixed arrow pointer** (winner always matches arrow)
- ✨ **Gold highlight** for the selected partition
- 🔊 **Auto-playing sound** (HTML-based, trimmed to spin duration)
- 🎨 Distinct, high-contrast colors for all partitions
- 🔄 Reset & spin again
- 🧱 Stable Streamlit rendering (no duplicate ID issues)
- ⚙️ 2026-safe Streamlit APIs

---

## 📸 How It Works (High Level)

1. User selects number of options (2–8)
2. User enters option text
3. Clicking **SPIN**:
   - Wheel rotates for ~8 seconds
   - Audio plays during the spin
   - Wheel slows down naturally
4. The arrow at the top determines the winner
5. The winning partition is highlighted in gold

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit** – UI framework
- **Plotly** – Wheel visualization
- **NumPy** – Spin physics (ease-out animation)
- **HTML/CSS** – Audio autoplay & arrow positioning

---

## 📦 Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/spin-the-wheel.git
cd spin-the-wheel
