import datefrommkv
import subprocess
timestamp = datefrommkv.extract_timestamp("testmkv.mkv")
print(timestamp)
def extract_metadata(mkv_file_path):
    try:
        # Använd FFmpeg för att extrahera metadata
        # FFmpeg skriver metadata till stderr när det inte finns någon output-fil
        result = subprocess.run(["ffmpeg", "-i", mkv_file_path], stderr=subprocess.PIPE, text=True)
        
        # Metadata finns i stderr
        metadata = result.stderr
        return metadata
    except Exception as e:
        return f"Ett fel uppstod: {e}"

# Exempelanvändning
metadata = extract_metadata("E:\\Dropbox\\CODE\\Transkript\\venvTranskript\\testmkv.mkv")
print(metadata)
