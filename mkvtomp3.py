import os
import subprocess
import sys  # Importera sys för att läsa argument
from datetime import datetime
import logging
import configparser
import shutil
config = configparser.ConfigParser()
config.read('config.ini')

# Konfiguration av logger
logging.basicConfig(level=logging.INFO,
                    filename='myapp.log',
                    filemode='w',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

def convert_to_mp3(source_file, output_file):
    try:
        # Använd output_file som direkt destinationsväg
        subprocess.call(['ffmpeg', '-i', source_file, '-vn', '-ar', '44100', '-ac', '2', '-b:a', '320k', '-filter:a', 'loudnorm', output_file])
        logging.info(f"Konverterad fil: {output_file}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Ett fel inträffade vid konvertering av {source_file} till MP3: {e}")
    except Exception as e:
        logging.error(f"Ett oväntat fel inträffade: {e}")

def main():
    print(f"Antal mottagna argument: {len(sys.argv)}")
    print(f"Mottagna argument: {sys.argv}")

    if len(sys.argv) < 4:
        logging.error("Inte tillräckligt med argument.")
        sys.exit(1)

    source_file = sys.argv[1]
    output_file = sys.argv[2]

    convert_to_mp3(source_file, output_file)


if __name__ == "__main__":
    main()
