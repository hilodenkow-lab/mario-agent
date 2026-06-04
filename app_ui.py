import streamlit as st
import time
import atexit
from datetime import datetime

st.set_page_config(
    page_title="MARIO // TACTICAL HUD",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
#  Import orchestrator — dengan fallback kalau
#  Playwright belum diinstall
# ─────────────────────────────────────────────
try:
    from main_orchestrator import jalankan_perintah, tutup_browser
    atexit.register(tutup_browser)
    AGENT_READY = True
except ImportError as e:
    AGENT_READY = False
    IMPORT_ERROR = str(e)

# ─────────────────────────────────────────────
#  CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;800&family=JetBrains+Mono:wght@400;500;700&family=Inter:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background-color: #0B0E14 !important;
    color: #E1E2EB !important;
    font-family: 'Inter', sans-serif;
    overflow-x: hidden;
}

#MainMenu, footer, header,
[data-testid="stToolbar"], [data-testid="stDecoration"],
[data-testid="stStatusWidget"] { display: none !important; }

[data-testid="stAppViewContainer"] { padding: 0 !important; }
[data-testid="block-container"]    { padding: 0 !important; max-width: 100% !important; }
.block-container                   { padding: 0 !important; max-width: 100% !important; }

/* ── NAVBAR ── */
.mario-nav {
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 32px; height: 56px;
    border-bottom: 1px solid #2A2E35;
    background: #0B0E14;
    position: sticky; top: 0; z-index: 100;
}
.nav-logo {
    font-family: 'Montserrat', sans-serif;
    font-size: 20px; font-weight: 800;
    letter-spacing: 0.1em; color: #FFF;
    text-transform: uppercase;
    display: flex; align-items: center; gap: 12px;
}
.nav-logo .hamburger { display:flex; flex-direction:column; gap:4px; cursor:pointer; }
.nav-logo .hamburger span { width:18px; height:1.5px; background:#FFF; display:block; }
.nav-tabs { display:flex; height:100%; align-items:flex-end; }
.nav-tab {
    font-family: 'Montserrat', sans-serif;
    font-size: 11px; font-weight: 700;
    letter-spacing: 0.12em; text-transform: uppercase;
    padding: 0 20px; height: 56px;
    display: flex; align-items: center;
    color: #6B7280; cursor: pointer;
    border-top: 2px solid transparent; transition: all 0.15s;
}
.nav-tab.active { color: #FFF; border-top: 2px solid #800000; }
.nav-tab:hover  { color: #E1E2EB; }
.nav-status {
    display: flex; align-items: center; gap: 16px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px; letter-spacing: 0.08em;
}
.status-dot { display:flex; align-items:center; gap:6px; color:#E1E2EB; text-transform:uppercase; }
.status-dot::before {
    content:''; width:6px; height:6px; border-radius:50%;
    background:#800000; display:inline-block;
    box-shadow: 0 0 6px #800000;
    animation: pulse-dot 2s ease-in-out infinite;
}
.status-dot.offline::before { background:#3D4250; box-shadow:none; animation:none; }
@keyframes pulse-dot {
    0%,100% { opacity:1; box-shadow:0 0 6px #800000; }
    50%      { opacity:.5; box-shadow:0 0 12px #F00; }
}

/* ── CENTER COLUMN ── */
.mario-center {
    width: 100%; max-width: 680px;
    margin: 0 auto;
    padding: 0 16px 160px;
    display: flex; flex-direction: column; align-items: center;
}

/* ── ORB ── */
.orb-section {
    width: 100%; display: flex; flex-direction: column;
    align-items: center; padding: 48px 0 32px; flex-shrink: 0;
}
.orb-wrapper {
    position: relative; width: 260px; height: 260px;
    display: flex; align-items: center; justify-content: center;
    margin-bottom: 24px;
}
.orb-ring {
    position: absolute; border-radius: 50%;
    border: 1.5px solid rgba(128,0,0,.6);
    animation: orb-breathe 3s ease-in-out infinite;
}
.orb-ring-1 { width:230px; height:230px; box-shadow:0 0 20px rgba(128,0,0,.3),inset 0 0 20px rgba(128,0,0,.1); }
.orb-ring-2 { width:190px; height:190px; border-color:rgba(128,0,0,.3); animation-delay:.3s; }
.orb-ring-3 { width:150px; height:150px; border-color:rgba(128,0,0,.2); animation-delay:.6s; }
.orb-core {
    width:110px; height:110px; border-radius:50%;
    background: radial-gradient(circle at 40% 35%, rgba(180,0,0,.25), rgba(80,0,0,.15), transparent 70%);
    border: 1px solid rgba(128,0,0,.4);
    box-shadow: 0 0 40px rgba(128,0,0,.2), 0 0 80px rgba(128,0,0,.1);
    animation: orb-core-pulse 3s ease-in-out infinite;
}
.orb-wrapper.processing .orb-ring-1 {
    animation: orb-spin 1.5s linear infinite;
    border-color: rgba(255,0,0,.8);
    box-shadow: 0 0 30px rgba(255,0,0,.5);
}
.orb-wrapper.processing .orb-core {
    background: radial-gradient(circle at 40% 35%, rgba(255,50,50,.4), rgba(180,0,0,.3), transparent 70%);
    animation: orb-core-pulse .6s ease-in-out infinite;
}
@keyframes orb-breathe  { 0%,100%{transform:scale(1);opacity:.7} 50%{transform:scale(1.04);opacity:1} }
@keyframes orb-core-pulse { 0%,100%{box-shadow:0 0 40px rgba(128,0,0,.2),0 0 80px rgba(128,0,0,.1)} 50%{box-shadow:0 0 60px rgba(180,0,0,.4),0 0 100px rgba(128,0,0,.2)} }
@keyframes orb-spin      { from{transform:rotate(0deg)} to{transform:rotate(360deg)} }

.orb-status-primary  { font-family:'Inter',sans-serif; font-size:15px; color:#E1E2EB; margin-bottom:6px; text-align:center; }
.orb-status-secondary{ font-family:'JetBrains Mono',monospace; font-size:10px; font-weight:500; letter-spacing:.14em; text-transform:uppercase; color:#6B7280; text-align:center; }

/* ── DIVIDER ── */
.chat-divider {
    width:100%; display:flex; align-items:center; gap:12px; margin:4px 0 20px;
}
.chat-divider-line  { flex:1; height:1px; background:#1E2229; }
.chat-divider-label { font-family:'JetBrains Mono',monospace; font-size:9px; letter-spacing:.14em; text-transform:uppercase; color:#2D3140; }

/* ── CHAT BUBBLES ── */
.chat-log { width:100%; display:flex; flex-direction:column; gap:14px; }

.msg-row         { display:flex; flex-direction:column; gap:3px; }
.msg-row.user    { align-items:flex-end; }
.msg-row.mario   { align-items:flex-start; }

.msg-label { font-family:'JetBrains Mono',monospace; font-size:9px; letter-spacing:.1em; text-transform:uppercase; padding:0 4px; }
.msg-row.user  .msg-label { color:#4A5060; }
.msg-row.mario .msg-label { color:#800000; }

.msg-bubble { max-width:82%; padding:10px 14px; font-family:'Inter',sans-serif; font-size:14px; line-height:1.6; }
.msg-row.user  .msg-bubble {
    background:#161A22; border:1px solid #2A2E35; color:#C9CDD6;
    clip-path: polygon(0 0, calc(100% - 8px) 0, 100% 8px, 100% 100%, 0 100%);
}
.msg-row.mario .msg-bubble {
    background:rgba(128,0,0,.08); border:1px solid rgba(128,0,0,.22); color:#E1E2EB;
    clip-path: polygon(8px 0, 100% 0, 100% 100%, 0 100%, 0 8px);
}
.msg-time { font-family:'JetBrains Mono',monospace; font-size:9px; color:#252930; letter-spacing:.06em; padding:0 4px; }

/* typing dots */
.typing-indicator { display:flex; align-items:center; gap:5px; padding:12px 16px; background:rgba(128,0,0,.08); border:1px solid rgba(128,0,0,.22); clip-path:polygon(8px 0,100% 0,100% 100%,0 100%,0 8px); }
.typing-dot { width:5px; height:5px; border-radius:50%; background:#800000; animation:typing-bounce 1.2s ease-in-out infinite; }
.typing-dot:nth-child(2){ animation-delay:.2s; }
.typing-dot:nth-child(3){ animation-delay:.4s; }
@keyframes typing-bounce { 0%,60%,100%{transform:translateY(0);opacity:.3} 30%{transform:translateY(-5px);opacity:1} }

/* warning chip */
.warn-chip {
    width:100%; padding:10px 14px; margin-bottom:12px;
    background:rgba(128,0,0,.1); border:1px solid rgba(128,0,0,.4);
    font-family:'JetBrains Mono',monospace; font-size:11px;
    color:#FF8071; letter-spacing:.06em;
}

/* empty state */
.chat-empty { width:100%; display:flex; flex-direction:column; align-items:center; gap:10px; padding:32px 0; color:#252930; font-family:'JetBrains Mono',monospace; font-size:10px; letter-spacing:.12em; text-transform:uppercase; }

/* ── INPUT BAR ── */
.mario-input-bar {
    position:fixed; bottom:0; left:0; right:0;
    padding:14px 32px 28px;
    background:rgba(11,14,20,.97);
    border-top:1px solid #1E2229;
    backdrop-filter:blur(12px);
    z-index:50;
}
[data-testid="stForm"] { border:none !important; padding:0 !important; background:transparent !important; }
[data-testid="stForm"] > div { padding:0 !important; }

.stTextInput > div > div > input {
    background-color:#05070A !important; border:none !important;
    border-bottom:1px solid #2A2E35 !important; border-radius:0 !important;
    color:#FFF !important; font-family:'JetBrains Mono',monospace !important;
    font-size:13px !important; letter-spacing:.04em !important; padding:13px 16px !important;
}
.stTextInput > div > div > input:focus { border-bottom-color:#800000 !important; box-shadow:none !important; outline:none !important; }
.stTextInput > div > div > input::placeholder { color:#2D3140 !important; }
.stTextInput > div { border:none !important; }

div.stButton > button {
    background-color:#800000 !important; color:#FFF !important;
    border:none !important; border-radius:0 !important;
    font-family:'JetBrains Mono',monospace !important;
    font-size:12px !important; font-weight:700 !important;
    letter-spacing:.1em !important; text-transform:uppercase !important;
    padding:13px 24px !important; height:auto !important;
    transition:all .15s !important; cursor:pointer !important;
    white-space:nowrap !important;
}
div.stButton > button:hover { background-color:#9A0000 !important; box-shadow:0 0 14px rgba(128,0,0,.5) !important; }
div.stButton > button:active { background-color:#600000 !important; }
div.stButton > button:disabled { background-color:#3D1010 !important; color:#6B3030 !important; cursor:not-allowed !important; }

/* ── FOOTER ── */
.mario-footer {
    position:fixed; bottom:0; left:0; right:0;
    display:flex; justify-content:space-between; align-items:center;
    padding:5px 32px;
    font-family:'JetBrains Mono',monospace; font-size:10px;
    letter-spacing:.1em; color:#3D4250; text-transform:uppercase;
    background:rgba(11,14,20,.99); border-top:1px solid #15191F;
    z-index:200; pointer-events:none;
}
.footer-highlight { color:#5A6170; }
.footer-accent    { color:#800000; }

/* TTS button */
.tts-btn {
    display:inline-flex; align-items:center; gap:6px;
    margin-top:8px; padding:5px 10px;
    background:transparent; border:1px solid rgba(128,0,0,.3);
    color:#800000; font-family:'JetBrains Mono',monospace;
    font-size:10px; letter-spacing:.1em; text-transform:uppercase;
    cursor:pointer; transition:all .15s;
}
.tts-btn:hover { background:rgba(128,0,0,.1); border-color:rgba(128,0,0,.6); }

[data-testid="stHorizontalBlock"] { gap:0 !important; }
[data-testid="column"] { padding:0 !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────
if "messages"    not in st.session_state: st.session_state.messages    = []
if "processing"  not in st.session_state: st.session_state.processing  = False
if "query_count" not in st.session_state: st.session_state.query_count = 0

# ─────────────────────────────────────────────
#  NAVBAR
# ─────────────────────────────────────────────
status_class = "status-dot" if AGENT_READY else "status-dot offline"
status_label = "SYSTEM ONLINE" if AGENT_READY else "AGENT OFFLINE"

st.markdown(f"""
<div class="mario-nav">
    <div class="nav-logo">
        <div class="hamburger"><span></span><span></span><span></span></div>
        MARIO
    </div>
    <div class="nav-tabs">
        <span class="nav-tab active">OPERATIONS</span>
        <span class="nav-tab">ARCHIVE</span>
    </div>
    <div class="nav-status">
        <div class="{status_class}">{status_label}</div>
        <span style="font-size:16px;cursor:pointer;opacity:0.4">⚙</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  CENTER COLUMN
# ─────────────────────────────────────────────
st.markdown('<div class="mario-center">', unsafe_allow_html=True)

# ── Warning kalau agent belum ready ──
if not AGENT_READY:
    st.markdown(f"""
    <div class="warn-chip">
        ⚠ AGENT OFFLINE — {IMPORT_ERROR}<br>
        Pastiin main_orchestrator.py & playwright udah terinstall.
    </div>
    """, unsafe_allow_html=True)

# ── ORB ──
orb_class = "orb-wrapper processing" if st.session_state.processing else "orb-wrapper"
if st.session_state.processing:
    sp, ss = "Mario lagi mikir...", "EXECUTING YOUR COMMAND"
elif st.session_state.messages:
    sp, ss = "Mario is listening...", "READY FOR YOUR NEXT COMMAND"
else:
    sp, ss = "Mario is listening...", "READY FOR YOUR NEXT COMMAND"

st.markdown(f"""
<div class="orb-section">
    <div class="{orb_class}">
        <div class="orb-ring orb-ring-1"></div>
        <div class="orb-ring orb-ring-2"></div>
        <div class="orb-ring orb-ring-3"></div>
        <div class="orb-core"></div>
    </div>
    <div class="orb-status-primary">{sp}</div>
    <div class="orb-status-secondary">{ss}</div>
</div>
""", unsafe_allow_html=True)

# ── CHAT LOG ──
if st.session_state.messages or st.session_state.processing:
    st.markdown("""
    <div class="chat-divider">
        <div class="chat-divider-line"></div>
        <div class="chat-divider-label">TRANSMISSION LOG</div>
        <div class="chat-divider-line"></div>
    </div>
    """, unsafe_allow_html=True)

    msgs_html = '<div class="chat-log">'
    for i, msg in enumerate(st.session_state.messages):
        role    = msg["role"]
        # Escape HTML dulu baru format newline
        content = (msg["content"]
                   .replace("&", "&amp;")
                   .replace("<", "&lt;")
                   .replace(">", "&gt;")
                   .replace("\n", "<br>")
                   .replace("**", ""))          # strip markdown bold
        t       = msg.get("time", "")
        label   = "YOU" if role == "user" else "MARIO-01"

        # Tombol TTS hanya untuk bubble Mario
        tts_btn = ""
        if role == "mario":
            # pakai data-text attribute buat JavaScript Web Speech API
            raw_text = msg["content"].replace('"', '&quot;').replace("\n", " ")
            tts_btn = f"""
            <button class="tts-btn" onclick="
                var u=new SpeechSynthesisUtterance('{raw_text}');
                u.lang='id-ID'; u.rate=0.95; u.pitch=0.85;
                window.speechSynthesis.cancel();
                window.speechSynthesis.speak(u);
            ">▶ PUTAR SUARA</button>"""

        msgs_html += f"""
        <div class="msg-row {role}">
            <div class="msg-label">{label}</div>
            <div class="msg-bubble">{content}{tts_btn}</div>
            <div class="msg-time">{t}</div>
        </div>
        """

    if st.session_state.processing:
        msgs_html += """
        <div class="msg-row mario">
            <div class="msg-label">MARIO-01</div>
            <div class="typing-indicator">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        </div>
        """

    msgs_html += '</div>'
    st.markdown(msgs_html, unsafe_allow_html=True)

else:
    st.markdown("""
    <div class="chat-empty">
        <div style="font-size:20px;opacity:.2">◈</div>
        <div>AWAITING FIRST TRANSMISSION</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  INPUT BAR
# ─────────────────────────────────────────────
st.markdown('<div class="mario-input-bar">', unsafe_allow_html=True)
with st.form(key="mario_form", clear_on_submit=True):
    c1, c2 = st.columns([11, 1])
    with c1:
        user_input = st.text_input(
            label="q", label_visibility="collapsed",
            placeholder="Suruh Mario ngapain...",
            disabled=st.session_state.processing
        )
    with c2:
        submitted = st.form_submit_button("GAS!", disabled=st.session_state.processing)
st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="mario-footer">
    <span>AGENT <span class="footer-highlight">M-01</span> // CLEARANCE: <span class="footer-accent">OMEGA</span></span>
    <span>MSG: <span class="footer-highlight">{st.session_state.query_count}</span> &nbsp; SIGNAL: <span class="footer-accent">98%</span></span>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  LOGIC — submit → proses → rerun
# ─────────────────────────────────────────────
if submitted and user_input.strip():
    now = datetime.now().strftime("%H:%M:%S")
    st.session_state.query_count += 1
    st.session_state.messages.append({
        "role": "user", "content": user_input.strip(), "time": now
    })
    st.session_state.processing = True
    st.rerun()

if st.session_state.processing:
    last = st.session_state.messages[-1]
    if last["role"] == "user":
        if AGENT_READY:
            try:
                resp = jalankan_perintah(last["content"])
            except Exception as e:
                resp = f"ERROR: {e}"
        else:
            resp = "Agent offline. Pastiin main_orchestrator.py bisa diimport."

        now = datetime.now().strftime("%H:%M:%S")
        st.session_state.messages.append({
            "role": "mario", "content": resp, "time": now
        })
        st.session_state.processing = False
        st.rerun()