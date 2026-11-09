import os
from gnani.stt import GnaniSTTClient
from config import GNANI_API_KEY

def main():
    audio_path = "test_welcome.wav"
    if not os.path.exists(audio_path):
        print(f"File {audio_path} not found. Run test_voice_call.py first.")
        return

    print(f"Testing Prisma STT on {audio_path}...")
    try:
        client = GnaniSTTClient(api_key=GNANI_API_KEY)
        resp = client.transcribe(audio_path, language_code="en-IN")
        text = resp.get("transcript") or resp.get("text", "")
        print(f"Transcribed output: \"{text.strip()}\"")
    except Exception as err:
        print(f"STT test error: {err}")

if __name__ == "__main__":
    main()
