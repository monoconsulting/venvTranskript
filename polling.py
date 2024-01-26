import os
import time
import logging
import configparser
print(f"Pollar...")
# Konfiguration av logger
logging.basicConfig(level=logging.INFO,
                    filename='myapp.log',
                    filemode='w',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

def wait_for_recordings_to_finish(directory, timeout=3600):
    try:
        start_time = time.time()
        while (time.time() - start_time) < timeout:
            files = os.listdir(directory)
            recording_files = [f for f in files if f.endswith('.mkv')]
            if recording_files:
                sorted_recordings = sorted(recording_files)
                print(f"Hittade inspelningsfiler: {sorted_recordings}")
                time.sleep(10)  # Vänta för att försäkra att inspelningen är klar
                return sorted_recordings

            time.sleep(2)  # Polla var 5:e sekund
    except FileNotFoundError:
        print(f"Katalogen {directory} hittades inte.")
    except Exception as e:
        print(f"Ett oväntat fel inträffade: {e}")

    raise TimeoutError("Ingen inspelningsfil hittades inom angiven tid.")

if __name__ == "__main__":
    recording_directory = 'E:\\Dropbox\\Meetings'
    try:
        recordings = wait_for_recordings_to_finish(recording_directory)
        print(f"Inspelningar klara: {recordings}")
    except TimeoutError as e:
        print(e)
