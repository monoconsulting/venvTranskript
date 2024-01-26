import os
import subprocess
from datetime import datetime
from gui import GuiApp
import polling
import logging
import configparser
config = configparser.ConfigParser()
config.read('config.ini')
# Konfiguration av logger
logging.basicConfig(level=logging.INFO,
                    filename='myapp.log',
                    filemode='w',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


def extract_timestamp_from_filename(filename):
    # Ta bort filändelsen
    name_without_extension = filename.split('.')[0]

    # Dela vid mellanslag för att separera datum och tid
    parts = name_without_extension.split(' ')

    # Kontrollera om vi har tillräckligt med delar för datum och tid
    if len(parts) == 2:
        date_part = parts[0]
        time_part = parts[1]

        # Ta endast timme och minut från tidsdelen
        time_part = time_part[:5]

        # Sätt ihop till önskat format
        formatted_timestamp = f"{date_part}_{time_part}"
        return formatted_timestamp
    else:
        # Hantera filnamn som inte innehåller förväntat mönster
        print(f"Filnamnet '{filename}' innehåller inte ett förväntat datum och tid.")
        return None
    
def process_recording(recording_file, selected_project, meeting_type):
    base_filename = os.path.splitext(os.path.basename(recording_file))[0]
    original_timestamp = extract_timestamp_from_filename(base_filename)

    if not original_timestamp:
        print(f"Kunde inte extrahera tidsstämpel från: {base_filename}")
        return

    new_filename_base = f"{selected_project}_{meeting_type}_{original_timestamp}"

    mp3_filename = os.path.join('E:\\Dropbox\\Meetings\\Audio', f"{new_filename_base}.mp3")
    transcript_filename = os.path.join('E:\\Dropbox\\Meetings\\Transcriptions', f"{new_filename_base}.docx")
    new_mkv_filename = os.path.join('E:\\Dropbox\\Meetings\\MKV', f"{new_filename_base}.mkv")


    try:
        if os.path.isfile(recording_file):
            # Konvertera till MP3
            mkvtomp3_script_path = 'E:\\Dropbox\\CODE\\Transkript\\venvTranskript\\mkvtomp3.py'
            subprocess.run(['python', mkvtomp3_script_path, recording_file, mp3_filename, selected_project, meeting_type], check=True)

            # Skapa transkript
            transcript_script_path = 'E:\\Dropbox\\CODE\\Transkript\\venvTranskript\\transkript.py'
            subprocess.run(['python', transcript_script_path, mp3_filename, transcript_filename, selected_project, meeting_type], check=True)

            # Flytta och byt namn på MKV-filen
            os.rename(recording_file, new_mkv_filename)

            print(f"Processen slutförd för inspelning: {recording_file}")
        else:
            print(f"Ogiltig inspelningsfil: {recording_file}")
    except subprocess.CalledProcessError as e:
        print(f"Ett fel inträffade vid bearbetning av {recording_file}: {e}")
    except Exception as e:
        print(f"Ett oväntat fel inträffade: {e}")


def main():
    recording_directory = 'E:\\Dropbox\\Meetings'

    while True:
        try:
            found_recordings = polling.wait_for_recordings_to_finish(recording_directory)

            for found_recording in found_recordings:
                found_recording_path = os.path.join(recording_directory, found_recording)

                if os.path.isfile(found_recording_path) and found_recording.endswith('.mkv'):
                    gui_app = GuiApp(found_recording)
                    gui_app.run()
                    selected_project = gui_app.selected_project
                    meeting_type = gui_app.meeting_type

                    # Lägg till utskriftsuttalanden här för att verifiera värdena
                    print(f"Valt projekt: {selected_project}, Mötestyp: {meeting_type}")

                    process_recording(found_recording_path, selected_project, meeting_type)
                else:
                    print(f"Ogiltig inspelningsfil: {found_recording_path}")

        except TimeoutError as e:
            print(e)

if __name__ == "__main__":
    main()