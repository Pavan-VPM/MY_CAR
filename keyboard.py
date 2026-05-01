import socket
from pynput import keyboard
from robot_config import ROBOT_IP, CONTROL_PORT

# Connect to the Raspberry Pi server using config details
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect((ROBOT_IP, CONTROL_PORT))
    print("Connected to Raspberry Pi robot. Use WASD keys to control the robot.")
    print("W: Forward, S: Backward, A: Left, D: Right, X: Stop, Q: Exit")

    def on_press(key):
        try:
            if key.char.lower() in ['w', 'a', 's', 'd', 'x', 'q']:
                client_socket.send(key.char.upper().encode())
                if key.char == 'q':
                    print("Exiting...")
                    return False
        except AttributeError:
            pass

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

except Exception as e:
    print(f"Error: {e}")

finally:
    client_socket.close()
