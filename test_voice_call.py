import os
from gnani.tts import GnaniTTSClient
from config import GNANI_API_KEY

def main():
    print("Testing Timbre TTS synthesis...")
    try:
        client = GnaniTTSClient(api_key=GNANI_API_KEY)
        sample_text = "Hello! Welcome to the Indic Voice AI Technical Interviewer."
        out_file = "test_welcome.wav"

        client.synthesize(
            text=sample_text,
            voice="Nalini",
            model="timbre-v2.5",
            language="en-IN",
            output_file=out_file
        )

        if os.path.exists(out_file):
            size_kb = os.path.getsize(out_file) / 1024
            print(f"Synthesis successful -> {out_file} ({size_kb:.1f} KB)")
        else:
            print("Synthesis finished without creating file.")
    except Exception as err:
        print(f"TTS test error: {err}")

if __name__ == "__main__":
    main()
