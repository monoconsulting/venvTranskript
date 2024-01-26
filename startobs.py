import json
import websocket

def start_obs_recording(scene_name):
    obs_ws_url = "ws://localhost:4444"  # Standardporten används

    ws = websocket.create_connection(obs_ws_url)

    # Sätt OBS scen
    set_scene_command = json.dumps({
        "request-type": "SetCurrentScene",
        "scene-name": scene_name,
        "message-id": "setscene"
    })
    ws.send(set_scene_command)
    ws.recv()  # Ta emot svar

    # Starta inspelning
    start_recording_command = json.dumps({
        "request-type": "StartRecording",
        "message-id": "startrecording"
    })
    ws.send(start_recording_command)
    ws.recv()  # Ta emot svar

    ws.close()

