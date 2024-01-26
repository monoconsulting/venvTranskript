import subprocess
import re

def extract_timestamp(mkv_file_path):
    try:
        # Använd FFmpeg för att extrahera metadata
        result = subprocess.run(["ffmpeg", "-i", mkv_file_path], stderr=subprocess.PIPE, text=True)
        output = result.stderr

        # Sök efter tidsstämpel i metadata
        timestamp_pattern = r"\d{4}-\d{2}-\d{2}_\d{2}_\d{2}"
        match = re.search(timestamp_pattern, output)
        if match:
            return match.group()  # Returnerar matchande tidsstämpel
        else:
            return "Tidsstämpel inte funnen"
    except Exception as e:
        return str(e)
