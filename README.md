# Indic Voice AI Technical Interviewer

A voice-first technical mock interview platform built for **The Great Indian AI Internship Challenge** by **Gnani.ai**.

Practicing for technical interviews can feel intimidating, especially when English isn't your primary language. Most traditional platforms expect textbook English and struggle with Indian accents and code-mixed speech (Hinglish). 

This project bridges that gap by combining Gnani AI's state-of-the-art speech models (**Timbre v2.5** and **Prisma v3.0**) to create an interactive interviewer that speaks natural Indian English and accurately understands code-mixed answers.

---

## Key Features

- **Indic Voice Synthesis (Timbre v2.5):** Voices technical questions and spoken feedback with realistic Indian English and Hindi accents across multiple personas (Nalini, Pranav, Saanvi, Vikrant).
- **Code-Mixed Speech Recognition (Prisma v3.0):** Transcribes candidate speech in real time with high acoustic confidence, even when blending technical terms with Hindi phrases.
- **Speech Delivery Intelligence:** Analyzes articulation speed (~WPM), detects filler words (e.g. *um, basically, matlab, yaani*), and provides delivery clarity feedback.
- **Adaptive Follow-Up Questions:** Generates dynamic, context-aware follow-up prompts to probe deeper architectural understanding.
- **Multi-Domain Practice:** Built-in interview tracks for Software Development (SDE), Machine Learning Systems, and Distributed Systems.

---

## Tech Stack & Architecture

- **Speech-to-Text (STT):** Gnani Prisma v3.0 via `gnani-vachana` SDK
- **Text-to-Speech (TTS):** Gnani Timbre v2.5 via `gnani-vachana` SDK
- **Frontend / Dashboard:** Streamlit with custom VisionOS-inspired Spatial UI and volumetric glassmorphism
- **Core Language:** Python 3.10+

---

## Quickstart

### 1. Clone the repository
```bash
git clone https://github.com/nandinimalik/indic-voice-interviewer.git
cd indic-voice-interviewer
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

*(Ensure `gnani-vachana` and `streamlit` are installed)*

### 3. Configure credentials
Add your Gnani API key in `config.py` or set it via environment variable:
```bash
export GNANI_API_KEY="your_api_key_here"
```
*(You can also paste the API key directly into the application sidebar).*

### 4. Run the application
```bash
streamlit run voice_interviewer_app.py
```

---

## Project Structure

```text
├── voice_interviewer_app.py   # Main Streamlit dashboard and UI
├── gnani_client.py            # Wrapper client for Prisma STT and Timbre TTS
├── config.py                  # API credentials and default voice settings
├── test_api_connection.py     # Simple API key verification script
├── test_voice_call.py         # Script to test Timbre TTS audio generation
├── test_stt_call.py           # Script to test Prisma STT transcription
└── README.md                  # Documentation and setup instructions
```

---

## Submission Details

- **Author:** Nandini Malik
- **Target Challenge:** The Great Indian AI Internship Challenge (Gnani.ai)
- **Target Categories:** 
  - `02 Mixed Vibes Award` (Code-mixed Indic speech transcription)
  - `08 Small Town, Big Build` (Empowering students across campuses)
  - `09 Demo Day Drop` (60-second video demo)

---

## Acknowledgments
Built with ❤️ using the official speech models provided by [Gnani.ai](https://www.gnani.ai).
