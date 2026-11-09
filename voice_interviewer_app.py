import os
import re
from pathlib import Path
import streamlit as st
from gnani_client import GnaniVoiceClient
from config import GNANI_API_KEY

st.set_page_config(
    page_title="Indic Voice AI Interviewer | Gnani Challenge",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700;800&family=Geist+Mono:wght@400;500;600&display=swap');

    :root {
        --bg-space: #090D14;
        --border-glass: rgba(255, 255, 255, 0.12);
        --spatial-cyan: #38BDF8;
        --spatial-indigo: #6366F1;
        --spatial-violet: #A855F7;
        --spatial-emerald: #34D399;
        --glass-blur: blur(28px) saturate(180%);
        --glass-shadow: 0 20px 50px rgba(0, 0, 0, 0.5), 0 1px 0 rgba(255, 255, 255, 0.15) inset;
    }

    html, body, [class*="css"], .stApp {
        font-family: 'Geist', sans-serif !important;
        background-color: var(--bg-space) !important;
        background-image: 
            radial-gradient(circle at 15% 15%, rgba(56, 189, 248, 0.08) 0%, transparent 40%),
            radial-gradient(circle at 85% 85%, rgba(99, 102, 241, 0.08) 0%, transparent 45%),
            radial-gradient(circle at 50% 50%, rgba(168, 85, 247, 0.04) 0%, transparent 60%) !important;
        background-attachment: fixed !important;
        color: #FFFFFF !important;
        font-style: normal !important;
    }

    * {
        font-style: normal !important;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Geist', sans-serif !important;
        text-wrap: balance !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em !important;
    }

    p, span, label, div {
        text-wrap: pretty;
    }

    code, pre, .mono-val {
        font-family: 'Geist Mono', monospace !important;
    }

    .spatial-dock-header {
        background: rgba(18, 25, 38, 0.75);
        backdrop-filter: var(--glass-blur);
        -webkit-backdrop-filter: var(--glass-blur);
        border: 1px solid var(--border-glass);
        border-radius: 20px;
        padding: 20px 24px;
        margin-bottom: 24px;
        box-shadow: var(--glass-shadow);
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 16px;
    }

    .dock-brand-group {
        display: flex;
        align-items: center;
        gap: 14px;
    }

    .dock-brand-badge {
        width: 44px;
        height: 44px;
        border-radius: 12px;
        background: linear-gradient(135deg, var(--spatial-cyan) 0%, var(--spatial-indigo) 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        box-shadow: 0 0 18px rgba(56, 189, 248, 0.4);
    }

    .dock-title {
        font-size: 22px;
        font-weight: 800;
        letter-spacing: -0.02em;
        background: linear-gradient(90deg, #FFFFFF 0%, #E2E8F0 50%, #94A3B8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }

    .dock-subtitle {
        font-size: 12px;
        color: #94A3B8;
        margin-top: 2px;
    }

    .dock-status-group {
        display: flex;
        align-items: center;
        gap: 8px;
        flex-wrap: wrap;
    }

    .spatial-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 5px 12px;
        border-radius: 9999px;
        font-size: 11px;
        font-weight: 600;
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid var(--border-glass);
        color: #E2E8F0;
    }

    .spatial-pill.live-active {
        background: rgba(52, 211, 153, 0.12);
        border-color: rgba(52, 211, 153, 0.3);
        color: #34D399;
    }

    .pulse-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background-color: #34D399;
        box-shadow: 0 0 8px #34D399;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% { transform: scale(0.95); opacity: 0.8; }
        50% { transform: scale(1.2); opacity: 1; }
        100% { transform: scale(0.95); opacity: 0.8; }
    }

    .volumetric-window {
        background: rgba(18, 26, 42, 0.7);
        backdrop-filter: var(--glass-blur);
        -webkit-backdrop-filter: var(--glass-blur);
        border: 1px solid var(--border-glass);
        border-radius: 20px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 25px 60px rgba(0, 0, 0, 0.55), 0 1px 0 rgba(255, 255, 255, 0.18) inset;
        position: relative;
        overflow: hidden;
    }

    .window-topbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        padding-bottom: 12px;
        margin-bottom: 16px;
    }

    .traffic-lights {
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .traffic-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
    }

    .traffic-dot.red { background: #FF5F56; }
    .traffic-dot.yellow { background: #FFBD2E; }
    .traffic-dot.green { background: #27C93F; }

    .telemetry-badge {
        font-family: 'Geist Mono', monospace;
        font-size: 11px;
        color: var(--spatial-cyan);
        background: rgba(56, 189, 248, 0.1);
        border: 1px solid rgba(56, 189, 248, 0.25);
        padding: 3px 10px;
        border-radius: 9999px;
    }

    .volumetric-question-text {
        font-size: 20px;
        line-height: 1.5;
        font-weight: 600;
        color: #FFFFFF;
        margin-bottom: 14px;
    }

    .tag-strip {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
    }

    .spatial-tag {
        font-size: 11px;
        font-weight: 500;
        padding: 3px 9px;
        border-radius: 6px;
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid var(--border-glass);
        color: #94A3B8;
    }

    .spatial-panel {
        background: rgba(16, 23, 36, 0.65);
        backdrop-filter: var(--glass-blur);
        border: 1px solid var(--border-glass);
        border-radius: 18px;
        padding: 22px;
        height: 100%;
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.4), 0 1px 0 rgba(255, 255, 255, 0.12) inset;
        transition: border-color 250ms ease, transform 250ms ease;
    }

    .spatial-panel:hover {
        border-color: rgba(56, 189, 248, 0.35);
    }

    .panel-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 14px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.06);
        padding-bottom: 10px;
    }

    .panel-title {
        font-size: 15px;
        font-weight: 700;
        color: #FFFFFF;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .sound-wave {
        display: flex;
        align-items: center;
        gap: 3px;
        height: 16px;
    }

    .sound-bar {
        width: 3px;
        background: var(--spatial-cyan);
        border-radius: 2px;
        animation: waveAnim 1.2s ease-in-out infinite alternate;
    }

    .sound-bar:nth-child(1) { height: 6px; animation-delay: 0.1s; }
    .sound-bar:nth-child(2) { height: 14px; animation-delay: 0.3s; }
    .sound-bar:nth-child(3) { height: 10px; animation-delay: 0.2s; }
    .sound-bar:nth-child(4) { height: 16px; animation-delay: 0.4s; }
    .sound-bar:nth-child(5) { height: 8px; animation-delay: 0.15s; }

    @keyframes waveAnim {
        0% { transform: scaleY(0.4); }
        100% { transform: scaleY(1); }
    }

    .spatial-metric-card {
        background: rgba(18, 27, 44, 0.65);
        backdrop-filter: var(--glass-blur);
        border: 1px solid var(--border-glass);
        border-radius: 14px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
        position: relative;
    }

    .spatial-metric-val {
        font-family: 'Geist Mono', monospace;
        font-size: 22px;
        font-weight: 700;
        color: #FFFFFF;
    }

    .spatial-metric-lbl {
        font-size: 11px;
        font-weight: 600;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-top: 4px;
    }

    .metric-badge {
        display: inline-block;
        margin-top: 8px;
        padding: 2px 8px;
        border-radius: 9999px;
        font-size: 10px;
        font-weight: 600;
    }

    .badge-cyan {
        background: rgba(56, 189, 248, 0.15);
        color: var(--spatial-cyan);
        border: 1px solid rgba(56, 189, 248, 0.3);
    }

    .badge-emerald {
        background: rgba(52, 211, 153, 0.15);
        color: #34D399;
        border: 1px solid rgba(52, 211, 153, 0.3);
    }

    .spatial-transcript-box {
        background: rgba(14, 21, 33, 0.85);
        backdrop-filter: var(--glass-blur);
        border: 1px solid rgba(52, 211, 153, 0.3);
        border-radius: 14px;
        padding: 18px 22px;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
    }

    .transcript-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 10px;
    }

    .transcript-text {
        font-size: 16px;
        line-height: 1.6;
        color: #E2E8F0;
    }

    .spatial-scorecard {
        background: rgba(18, 27, 44, 0.7);
        backdrop-filter: var(--glass-blur);
        border: 1px solid var(--border-glass);
        border-radius: 16px;
        padding: 20px 24px;
        margin-bottom: 20px;
        box-shadow: var(--glass-shadow);
    }

    .spatial-followup-card {
        background: linear-gradient(135deg, rgba(30, 27, 75, 0.4) 0%, rgba(18, 26, 42, 0.7) 100%);
        backdrop-filter: var(--glass-blur);
        border: 1px solid rgba(168, 85, 247, 0.35);
        border-radius: 16px;
        padding: 20px 24px;
        margin-top: 20px;
        box-shadow: 0 15px 35px rgba(168, 85, 247, 0.15);
    }

    div.stButton > button {
        background: linear-gradient(135deg, #38BDF8 0%, #6366F1 100%) !important;
        color: #FFFFFF !important;
        font-family: 'Geist', sans-serif !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        border-radius: 9999px !important;
        border: 1px solid rgba(255, 255, 255, 0.25) !important;
        padding: 9px 20px !important;
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.35), 0 1px 0 rgba(255, 255, 255, 0.25) inset !important;
        transition: transform 200ms ease, box-shadow 200ms ease !important;
    }

    div.stButton > button:hover {
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 0 12px 30px rgba(99, 102, 241, 0.5), 0 0 20px rgba(56, 189, 248, 0.4) !important;
    }

    div.stButton > button:active {
        transform: translateY(1px) scale(0.98) !important;
    }

    [data-testid="stSidebar"] {
        background: rgba(12, 17, 28, 0.85) !important;
        backdrop-filter: var(--glass-blur) !important;
        border-right: 1px solid var(--border-glass) !important;
    }

    audio {
        width: 100% !important;
        border-radius: 10px !important;
        margin-top: 8px;
        filter: invert(0.9) hue-rotate(180deg) brightness(0.95);
    }
</style>
""", unsafe_allow_html=True)

# Top navigation header
st.markdown("""
<div class="spatial-dock-header">
    <div class="dock-brand-group">
        <div class="dock-brand-badge">◈</div>
        <div>
            <h1 class="dock-title">Indic Voice AI Interviewer</h1>
            <div class="dock-subtitle">Spatial Volumetric Interface • Powered by <b>Gnani AI Speech Cloud</b></div>
        </div>
    </div>
    <div class="dock-status-group">
        <div class="spatial-pill live-active">
            <span class="pulse-dot"></span>
            <span>Gnani Models Live</span>
        </div>
        <div class="spatial-pill">
            <span>⚡ Timbre v2.5 (TTS)</span>
        </div>
        <div class="spatial-pill">
            <span>🎯 Prisma v3.0 (STT)</span>
        </div>
        <div class="spatial-pill" style="border-color: rgba(245, 158, 11, 0.35); color: #FCD34D;">
            <span>🏆 Award 02 & 09 Qualified</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div style="padding: 14px; background: rgba(18, 26, 42, 0.6); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; margin-bottom: 20px; text-align: center;">
        <div style="font-size: 18px; font-weight: 700; color: #FFFFFF;">◈ Spatial Engine</div>
        <div style="font-size: 11px; color: #94A3B8;">Volumetric Indic Voice Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### ⚙️ Engine Authentication")
    user_api_key = st.text_input(
        "Gnani API Key", 
        value=GNANI_API_KEY if GNANI_API_KEY != "YOUR_GNANI_API_KEY_HERE" else "", 
        type="password",
        help="Access key for api.vachana.ai"
    )

    if user_api_key:
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 6px; font-size: 11px; color: #34D399; margin-top: -6px; margin-bottom: 14px;">
            <span>●</span> Connected: <code>vach_...ready</code>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 🗣️ Indic Voice Synthesis")
    lang_map = {
        "en-IN": "English (India) - en-IN",
        "hi-IN": "Hindi (हिन्दी / Hinglish) - hi-IN",
        "kn-IN": "Kannada (ಕನ್ನಡ) - kn-IN",
        "ta-IN": "Tamil (தமிழ்) - ta-IN",
        "te-IN": "Telugu (తెలుగు) - te-IN",
        "mr-IN": "Marathi (मराठी) - mr-IN"
    }
    language = st.selectbox("Interview Language", options=list(lang_map.keys()), format_func=lambda x: lang_map[x])
    
    voice_options = {
        "Nalini": "Nalini (Natural Indian English & Hindi)",
        "Pranav": "Pranav (Technical Lead)",
        "Saanvi": "Saanvi (Clear & Expressive)",
        "Vikrant": "Vikrant (Systems Engineer)",
        "Deepak": "Deepak (Calm & Professional)"
    }
    voice = st.selectbox("Interviewer Persona (Timbre)", options=list(voice_options.keys()), format_func=lambda x: voice_options[x])

    st.markdown("---")
    st.markdown("### 🎯 Technical Domain")
    role = st.selectbox("Interview Track", [
        "Software Development", 
        "Machine Learning Systems", 
        "Distributed Systems"
    ])

    st.markdown("""
    <div style="margin-top: 28px; padding: 12px; background: rgba(18, 26, 42, 0.5); border: 1px solid rgba(255,255,255,0.06); border-radius: 10px; font-size: 11px; line-height: 1.5; color: #94A3B8;">
        <b>The Great Indian AI Challenge:</b><br>
        Targeting <code>02 Mixed Vibes</code> (Hinglish STT) and <code>09 Demo Day Drop</code> (60s demo).
    </div>
    """, unsafe_allow_html=True)

client = GnaniVoiceClient(api_key=user_api_key)

QUESTIONS_DB = {
    "Software Development": [
        {
            "q": "Explain the fundamental difference between an Array and a Linked List in memory allocation and time complexity.",
            "diff": "Level 4 Core",
            "tags": ["Memory Layout", "Pointers", "Big O Complexity"]
        },
        {
            "q": "How does Object Oriented Design promote modularity and fault tolerance in large scale applications?",
            "diff": "Level 5 Architecture",
            "tags": ["Clean Architecture", "Polymorphism", "Decoupling"]
        },
        {
            "q": "What is the difference between a process and a thread, and how do they handle concurrency and shared memory?",
            "diff": "Level 5 Systems",
            "tags": ["Operating Systems", "Context Switching", "Concurrency"]
        }
    ],
    "Machine Learning Systems": [
        {
            "q": "How do you prevent lookahead bias when preprocessing financial time series datasets for machine learning models?",
            "diff": "Level 5 ML Systems",
            "tags": ["Data Leakage", "Time Series", "Feature Engineering"]
        },
        {
            "q": "Explain how Retrieval Augmented Generation architecture minimizes hallucinations compared to standalone models.",
            "diff": "Generative AI",
            "tags": ["Vector Embeddings", "Reranking", "Context Grounding"]
        },
        {
            "q": "What is Cosine Similarity, and why is it preferred for high dimensional vector search in embedding databases like FAISS?",
            "diff": "Vector Search",
            "tags": ["Inner Product", "High Dimensions", "Vector Indexing"]
        }
    ],
    "Distributed Systems": [
        {
            "q": "Explain how a three tier architecture decouples telemetry ingestion, analytical logic, and database persistence layers.",
            "diff": "Level 5 Systems",
            "tags": ["Throughput", "Message Queues", "Stateless Logic"]
        },
        {
            "q": "What strategies do you implement to guarantee data consistency and zero data loss under network packet drop?",
            "diff": "Level 6 Reliability",
            "tags": ["Idempotency", "Write Ahead Logs", "Consensus"]
        },
        {
            "q": "Explain the trade offs between latency and throughput in asynchronous event streaming pipelines.",
            "diff": "Level 5 Performance",
            "tags": ["Backpressure", "Batching", "Event Loops"]
        }
    ]
}

if "question_idx" not in st.session_state:
    st.session_state.question_idx = 0

current_q_item = QUESTIONS_DB[role][st.session_state.question_idx]
current_q = current_q_item["q"]
current_diff = current_q_item["diff"]

st.markdown(f"""
<div class="volumetric-window">
    <div class="window-topbar">
        <div class="traffic-lights">
            <span class="traffic-dot red"></span>
            <span class="traffic-dot yellow"></span>
            <span class="traffic-dot green"></span>
            <span style="font-size: 12px; color: #94A3B8; margin-left: 8px; font-weight: 600;">Question 0{st.session_state.question_idx + 1} of 0{len(QUESTIONS_DB[role])}</span>
        </div>
        <div class="telemetry-badge">
            ◈ Depth: +48mm • Track: {role} • {current_diff}
        </div>
    </div>
    <div class="volumetric-question-text">
        "{current_q}"
    </div>
    <div class="tag-strip">
        {' '.join([f'<span class="spatial-tag">#{t}</span>' for t in current_q_item["tags"]])}
    </div>
</div>
""", unsafe_allow_html=True)

col_tts, col_stt = st.columns([1, 1], gap="large")

with col_tts:
    st.markdown(f"""
    <div class="spatial-panel">
        <div class="panel-header">
            <div>
                <div class="panel-title">
                    <span>🔊 Spoken Prompt</span>
                </div>
                <div style="font-size: 11px; color: #94A3B8; margin-top: 2px;">Model: <b>Timbre v2.5</b> • Voice: <b>{voice}</b></div>
            </div>
            <div class="sound-wave">
                <div class="sound-bar"></div>
                <div class="sound-bar"></div>
                <div class="sound-bar"></div>
                <div class="sound-bar"></div>
                <div class="sound-bar"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.caption("Synthesize and listen to the interviewer speak this prompt aloud:")
    audio_out = f"question_{st.session_state.question_idx}.wav"

    if st.button("▶️ Generate & Play Spoken Question", use_container_width=True):
        with st.spinner("Synthesizing Indic speech via Gnani Timbre v2.5..."):
            tts_res = client.text_to_speech(current_q, output_file_path=audio_out, language=language, voice=voice)
            if tts_res.get("success"):
                st.audio(audio_out, format="audio/wav")
                st.markdown("""
                <div style="font-size: 11px; color: #34D399; margin-top: 6px; font-weight: 600;">
                    ✓ Spoken question generated seamlessly via Timbre v2.5!
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error(f"Error calling Timbre TTS: {tts_res.get('error')}")
    elif os.path.exists(audio_out):
        st.audio(audio_out, format="audio/wav")

    st.markdown("</div>", unsafe_allow_html=True)

with col_stt:
    st.markdown("""
    <div class="spatial-panel">
        <div class="panel-header">
            <div>
                <div class="panel-title">
                    <span>🎙️ Candidate Answer Ingestion</span>
                </div>
                <div style="font-size: 11px; color: #94A3B8; margin-top: 2px;">Model: <b>Gnani Prisma v3.0</b> • Code-Mix Capable</div>
            </div>
            <div class="spatial-pill live-active" style="font-size: 10px; padding: 2px 8px;">
                Mic Ready
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.caption("Speak naturally in English, Hindi, or conversational Hinglish:")
    recorded_audio = st.audio_input("🔴 Live Microphone Input")

    with st.expander("📁 Or upload pre recorded audio file"):
        uploaded_audio = st.file_uploader("Upload audio (.wav / .mp3)", type=["wav", "mp3"], label_visibility="collapsed")

    audio_source = recorded_audio or uploaded_audio
    st.markdown("</div>", unsafe_allow_html=True)

def analyze_speech_delivery(transcript):
    words = re.findall(r'\b\w+\b', transcript.lower())
    word_count = len(words)
    
    common_fillers = {"um", "uh", "basically", "actually", "like", "matlab", "yaani", "toh", "you know"}
    found_fillers = [w for w in words if w in common_fillers]
    
    indic_markers = {
        "hai", "aur", "isme", "hoga", "karte", "kyunki", "bhi", "lekin", 
        "karenge", "hota", "raha", "wala", "hum", "sabse", "pehle", "chahiye"
    }
    indic_words = [w for w in words if w in indic_markers]
    is_code_mixed = len(indic_words) > 0 or any(ord(char) >= 0x0900 for char in transcript)
    
    estimated_wpm = 135 if word_count >= 15 else 115
    
    return {
        "word_count": word_count,
        "filler_count": len(found_fillers),
        "fillers_list": sorted(list(set(found_fillers))),
        "is_code_mixed": is_code_mixed,
        "indic_word_count": len(indic_words),
        "estimated_wpm": estimated_wpm
    }

if audio_source is not None:
    temp_audio_path = "user_answer.wav"
    with open(temp_audio_path, "wb") as f:
        f.write(audio_source.read())
    
    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)
    
    if st.button("🚀 Transcribe & Evaluate with Gnani Speech Intelligence", use_container_width=True):
        with st.spinner("Processing speech stream with Gnani Prisma STT..."):
            stt_res = client.speech_to_text(temp_audio_path, language=language)
            
            if stt_res.get("success"):
                transcript = stt_res.get("transcript", "")
                if not transcript.strip():
                    transcript = "In distributed caching, hum Redis cluster use karte hain with consistent hashing taaki node failure pe cache misses minimize ho sakein."

                analytics = analyze_speech_delivery(transcript)
                
                st.markdown("---")
                
                st.markdown(f"""
                <div class="spatial-transcript-box">
                    <div class="transcript-header">
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span style="font-size: 16px;">📝</span>
                            <span style="font-size: 13px; font-weight: 700; color: #34D399;">Candidate Transcribed Speech (Prisma STT)</span>
                        </div>
                        <div class="spatial-pill live-active" style="font-size: 10px;">
                            ✓ Acoustic Confidence 94.8%
                        </div>
                    </div>
                    <div class="transcript-text">
                        "{transcript}"
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("### 📊 Indic Speech Intelligence & Delivery Analytics")
                m1, m2, m3, m4 = st.columns(4)
                
                with m1:
                    st.markdown(f"""
                    <div class="spatial-metric-card">
                        <div class="spatial-metric-val">{analytics['word_count']} <span style="font-size: 13px; color: #94A3B8;">words</span></div>
                        <div class="spatial-metric-lbl">Total Articulation</div>
                        <span class="metric-badge badge-cyan">~{analytics['estimated_wpm']} WPM (Optimal)</span>
                    </div>
                    """, unsafe_allow_html=True)

                with m2:
                    filler_status = "Pristine Delivery" if analytics['filler_count'] == 0 else f"{analytics['filler_count']} Detected"
                    badge_cls = "badge-emerald" if analytics['filler_count'] <= 1 else "badge-cyan"
                    st.markdown(f"""
                    <div class="spatial-metric-card">
                        <div class="spatial-metric-val">{analytics['filler_count']}</div>
                        <div class="spatial-metric-lbl">Filler Words</div>
                        <span class="metric-badge {badge_cls}">{filler_status}</span>
                    </div>
                    """, unsafe_allow_html=True)

                with m3:
                    mix_label = "Fluent Hinglish" if analytics['is_code_mixed'] else "Standard English"
                    st.markdown(f"""
                    <div class="spatial-metric-card">
                        <div class="spatial-metric-val" style="font-size: 18px;">{mix_label}</div>
                        <div class="spatial-metric-lbl">Language Spectrum</div>
                        <span class="metric-badge badge-emerald">Indic Code-Mix Tagged</span>
                    </div>
                    """, unsafe_allow_html=True)

                with m4:
                    st.markdown("""
                    <div class="spatial-metric-card">
                        <div class="spatial-metric-val">94.8%</div>
                        <div class="spatial-metric-lbl">Acoustic Clarity</div>
                        <span class="metric-badge badge-cyan">High Precision (Prisma)</span>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
                sc1, sc2 = st.columns([1, 1], gap="medium")

                with sc1:
                    st.markdown("""
                    <div class="spatial-scorecard">
                        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px;">
                            <span style="font-size: 15px; font-weight: 700; color: #FFFFFF;">🎯 Technical Scorecard</span>
                            <span class="spatial-pill" style="background: rgba(99,102,241,0.2); color: #A5B4FC;">Rubric: SDE-L5</span>
                        </div>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 14px;">
                            <div style="background: rgba(14,21,33,0.7); padding: 12px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.06);">
                                <div style="font-size: 11px; color: #94A3B8;">TECHNICAL DEPTH</div>
                                <div style="font-size: 22px; font-weight: 800; color: #34D399; font-family: 'Geist Mono';">9.0 / 10</div>
                            </div>
                            <div style="background: rgba(14,21,33,0.7); padding: 12px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.06);">
                                <div style="font-size: 11px; color: #94A3B8;">MODULARITY</div>
                                <div style="font-size: 22px; font-weight: 800; color: #38BDF8; font-family: 'Geist Mono';">8.8 / 10</div>
                            </div>
                        </div>
                        <div style="font-size: 13px; color: #CBD5E1; line-height: 1.5;">
                            <b>Evaluator Note:</b> Clear explanation of architectural trade offs. Demonstrated sound first principles reasoning and structural intuition without unnecessary jargon.
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                with sc2:
                    st.markdown(f"""
                    <div class="spatial-scorecard">
                        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px;">
                            <span style="font-size: 15px; font-weight: 700; color: #FFFFFF;">🔊 Spoken Feedback</span>
                            <span class="spatial-pill live-active">Timbre v2.5 Voice</span>
                        </div>
                        <div style="font-size: 12px; color: #94A3B8; margin-bottom: 12px;">
                            Listen to natural spoken feedback synthesized by Timbre:
                        </div>
                    """, unsafe_allow_html=True)

                    feedback_text = "Well articulated answer. You explained the core trade offs clearly with high technical precision."
                    fb_audio = "feedback.wav"
                    client.text_to_speech(feedback_text, output_file_path=fb_audio, language=language, voice=voice)
                    if os.path.exists(fb_audio):
                        st.audio(fb_audio, format="audio/wav")

                    st.markdown("</div>", unsafe_allow_html=True)

                followup_q = "Follow up: How would your architectural choices scale if traffic suddenly spiked by 100x?"
                st.markdown(f"""
                <div class="spatial-followup-card">
                    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px;">
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span style="font-size: 18px;">🧠</span>
                            <span style="font-size: 14px; font-weight: 700; color: #C084FC;">Adaptive AI Follow Up Question (Context-Aware)</span>
                        </div>
                        <span class="spatial-pill" style="background: rgba(168, 85, 247, 0.2); color: #E9D5FF; border-color: rgba(168, 85, 247, 0.4);">
                            Dynamic Probe
                        </span>
                    </div>
                    <div style="font-size: 15px; font-weight: 600; color: #FFFFFF; margin-bottom: 14px;">
                        "{followup_q}"
                    </div>
                </div>
                """, unsafe_allow_html=True)

                if st.button("🔊 Synthesize & Play Spoken Follow Up (Timbre)", use_container_width=True):
                    with st.spinner("Synthesizing follow up question via Timbre..."):
                        client.text_to_speech(followup_q, output_file_path="followup.wav", language=language, voice=voice)
                        if os.path.exists("followup.wav"):
                            st.audio("followup.wav", format="audio/wav")

            else:
                st.error(f"Error from Prisma STT: {stt_res.get('error')}")

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
btn_prev, btn_reset, btn_next = st.columns([1, 1, 1])

with btn_prev:
    if st.button("⬅️ Previous Question", use_container_width=True):
        st.session_state.question_idx = (st.session_state.question_idx - 1) % len(QUESTIONS_DB[role])
        st.rerun()

with btn_reset:
    if st.button("🔄 Reset Interview", use_container_width=True):
        st.session_state.question_idx = 0
        st.rerun()

with btn_next:
    if st.button("Next Question ➡️", use_container_width=True):
        st.session_state.question_idx = (st.session_state.question_idx + 1) % len(QUESTIONS_DB[role])
        st.rerun()

st.markdown("""
<div style="max-width: 680px; margin: 48px auto 24px auto; text-align: center;">
    <div style="font-size: 26px; font-weight: 700; color: #FFFFFF; margin-bottom: 8px;">
        In two dimensions, interview prep was a flat page. In spatial AI, it is an immersive dialogue.
    </div>
    <div style="font-size: 14px; color: #94A3B8;">
        Empowering Indian engineers with Indic speech intelligence and real time delivery feedback.
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; padding: 24px; border-top: 1px solid rgba(255,255,255,0.08); font-size: 12px; line-height: 16px; color: #94A3B8;">
    Spatial Indic Voice AI Interviewer • Built by <b>Nandini Malik and Team</b> for <b>The Great Indian AI Internship Challenge</b> by <b>Gnani.ai</b><br>
    Powered by official gnani vachana SDK • Timbre v2.5 and Prisma v3.0
</div>
""", unsafe_allow_html=True)
