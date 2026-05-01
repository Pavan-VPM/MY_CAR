import socket
import speech_recognition as sr
from robot_config import ROBOT_IP, CONTROL_PORT

# Natural language mappings
COMMAND_MAP = {
    "forward": b'W',
    "go": b'W',
    "move": b'W',
    "ahead": b'W',
    "back": b'S',
    "reverse": b'S',
    "backward": b'S',
    "left": b'A',
    "turn left": b'A',
    "right": b'D',
    "turn right": b'D',
    "stop": b'X',
    "halt": b'X',
    "freeze": b'X',
    "quit": b'Q',
    "exit": b'Q',
    "shutdown": b'Q'
}

# Set up connection
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect((ROBOT_IP, CONTROL_PORT))
    print(f"Connected to Raspberry Pi robot. Speak a command (e.g., 'go', 'back', 'left', 'stop', 'quit').")

    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    # Increase sensitivity
    recognizer.energy_threshold = 100
    recognizer.pause_threshold = 0.5

    while True:
        with mic as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")

            matched = False
            for phrase, action in COMMAND_MAP.items():
                if phrase in command:
                    client_socket.send(action)
                    print(f"Command matched: {phrase.upper()} —> Sending {action.decode()}")
                    matched = True
                    if action == b'Q':
                        print("Exiting...")
                        raise KeyboardInterrupt
                    break

            if not matched:
                print("Unrecognized command. Try again.")

        except sr.UnknownValueError:
            print("Could not understand audio. Speak clearly.")
        except sr.RequestError as e:
            print(f"Speech Recognition error: {e}")

except KeyboardInterrupt:
    print("Voice control terminated by user.")

except Exception as e:
    print(f"Connection error: {e}")

finally:
    client_socket.close()
