import streamlit as st
import random
import plotly.graph_objects as go
import time
import numpy as np
import base64

# ------------------------------------------------
# Page Config
# ------------------------------------------------
st.set_page_config(page_title="Spin the Wheel", layout="wide")

# ------------------------------------------------
# CSS (Centered Arrow + Glow)
# ------------------------------------------------
st.markdown("""
<style>
.wheel-wrapper {
    position: relative;
    width: 100%;
    display: flex;
    justify-content: center;
}

.arrow {
    position: absolute;
    top: -22px;
    left: 50%;
    transform: translateX(-50%);
    font-size: 42px;
    z-index: 10;
}

.glow {
    animation: glowPulse 1.5s infinite alternate;
}

@keyframes glowPulse {
    from { box-shadow: 0 0 12px rgba(255,215,0,0.5); }
    to   { box-shadow: 0 0 30px rgba(255,215,0,0.9); }
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# HTML Audio Autoplay (Trimmed to 6s)
# ------------------------------------------------
def autoplay_audio_trimmed(file_path: str, duration=6):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()

    st.markdown(f"""
    <audio autoplay onloadedmetadata="this.currentTime=0; this.play(); setTimeout(() => this.pause(), {duration});">
        <source src="data:audio/wav;base64,{b64}" type="audio/wav">
    </audio>
    """, unsafe_allow_html=True)

# ------------------------------------------------
# Session State
# ------------------------------------------------
if "angle" not in st.session_state:
    st.session_state.angle = 0
if "winner" not in st.session_state:
    st.session_state.winner = None
if "spinning" not in st.session_state:
    st.session_state.spinning = False

# ------------------------------------------------
# Color Palette
# ------------------------------------------------
COLOR_PALETTE = [
    "#4E79A7", "#F28E2B", "#E15759", "#76B7B2",
    "#59A14F", "#1F7A8C", "#B07AA1", "#FF9DA7"
]

# ------------------------------------------------
# Wheel Drawing
# ------------------------------------------------
def draw_wheel(labels, rotation=0, highlight=None):
    values = [1] * len(labels)
    colors = []

    for i in range(len(labels)):
        if i == highlight:
            colors.append("#FFD700")  # gold
        else:
            colors.append(COLOR_PALETTE[i % len(COLOR_PALETTE)])

    fig = go.Figure(
        go.Pie(
            labels=labels,
            values=values,
            hole=0.35,
            rotation=rotation,
            direction="clockwise",
            marker=dict(colors=colors),
            textinfo="label",
        )
    )

    fig.update_layout(
        showlegend=False,
        height=520,
        margin=dict(t=30, b=20),
    )
    return fig

# ------------------------------------------------
# Layout
# ------------------------------------------------
left, right = st.columns([1, 1.4])

with left:
    st.header("📝 Options")

    num_sections = st.slider("Number of options", 2, 8, 4)

    options = [
        st.text_input(f"Option {i+1}", f"{i+1}")
        for i in range(num_sections)
    ]

    col1, col2 = st.columns(2)
    spin = col1.button("🎡 SPIN")
    reset = col2.button("🔄 RESET")

# ------------------------------------------------
# Reset
# ------------------------------------------------
if reset:
    st.session_state.angle = 0
    st.session_state.winner = None
    st.session_state.spinning = False
    st.rerun()

# ------------------------------------------------
# Wheel Area (Arrow perfectly centered)
# ------------------------------------------------
with right:
    st.header("🎯 Decision Wheel")
    st.markdown('<div class="wheel-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="arrow">🔻</div>', unsafe_allow_html=True)
    wheel_placeholder = st.empty()

# ------------------------------------------------
# Spin Logic (6 seconds, ease-out)
# ------------------------------------------------
if spin and not st.session_state.spinning:
    st.session_state.spinning = True

    # 🔊 Play trimmed audio (HTML-based)
    autoplay_audio_trimmed("spin.wav", duration=6)

    frames = 160
    frame_delay = 0.05
    total_spin = random.randint(1800, 2520)  # 5–7 rotations

    progress = np.linspace(0, 1, frames)
    angles = total_spin * (1 - (1 - progress) ** 3)

    for i, angle in enumerate(angles):
        st.session_state.angle = angle
        wheel_placeholder.plotly_chart(
            draw_wheel(options, rotation=angle),
            width="stretch",
            key=f"spin_{i}"
        )
        time.sleep(frame_delay)

    # ---------------------------
    # Correct winner calculation
    # ---------------------------
    final_angle = total_spin % 360
    slice_angle = 360 / num_sections
    winner = int(((360 - final_angle) % 360) // slice_angle)

    st.session_state.angle = total_spin
    st.session_state.winner = winner
    st.session_state.spinning = False

# ------------------------------------------------
# Final Wheel
# ------------------------------------------------
wheel_placeholder.plotly_chart(
    draw_wheel(
        options,
        rotation=st.session_state.angle,
        highlight=st.session_state.winner
    ),
    width="stretch",
    key="final_wheel"
)

st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------
# Result
# ------------------------------------------------
if st.session_state.winner is not None:
    st.success(f"✅ Selected: **{options[st.session_state.winner]}**")
    st.balloons()
