from config import GNANI_API_KEY

def main():
    if not GNANI_API_KEY or GNANI_API_KEY == "YOUR_GNANI_API_KEY_HERE":
        print("API key is not configured. Set GNANI_API_KEY in config.py or env.")
        return

    masked = GNANI_API_KEY[:8] + "..." + GNANI_API_KEY[-4:]
    print(f"API key detected: {masked} (length {len(GNANI_API_KEY)})")
    print("Ready to run SDK client scripts.")

if __name__ == "__main__":
    main()
