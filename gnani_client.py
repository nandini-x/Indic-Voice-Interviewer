import os
from config import GNANI_API_KEY
from gnani.stt import GnaniSTTClient
from gnani.tts import GnaniTTSClient

class GnaniVoiceClient:
    def __init__(self, api_key=None):
        self.api_key = api_key or GNANI_API_KEY
        self.stt_client = None
        self.tts_client = None

        if self.api_key and self.api_key != "YOUR_GNANI_API_KEY_HERE":
            try:
                self.stt_client = GnaniSTTClient(api_key=self.api_key)
                self.tts_client = GnaniTTSClient(api_key=self.api_key)
            except Exception as err:
                print(f"[gnani_client] SDK init failed: {err}")

    def speech_to_text(self, audio_path, language="en-IN"):
        if not self.stt_client:
            return {
                "success": False, 
                "error": "STT client not ready. Please verify your Gnani API key."
            }

        try:
            res = self.stt_client.transcribe(audio_path, language_code=language)
            # handle both transcript and text fields depending on SDK response format
            text = res.get("transcript") or res.get("text", "")
            return {"success": True, "transcript": text.strip(), "raw": res}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def text_to_speech(self, text, output_file_path="response.wav", language="en-IN", voice="Nalini"):
        if not self.tts_client:
            return {
                "success": False, 
                "error": "TTS client not ready. Please verify your Gnani API key."
            }

        try:
            self.tts_client.synthesize(
                text=text,
                voice=voice,
                model="timbre-v2.5",
                language=language,
                output_file=output_file_path
            )
            return {"success": True, "audio_path": output_file_path}
        except Exception as e:
            return {"success": False, "error": str(e)}

if __name__ == "__main__":
    client = GnaniVoiceClient()
    status = "authenticated" if client.stt_client else "no api key provided"
    print(f"GnaniVoiceClient check: {status}")
