import socket
import cv2
import mediapipe as mp
from robot_config import ROBOT_IP, CONTROL_PORT

# Connect to Raspberry Pi
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client_socket.connect((ROBOT_IP, CONTROL_PORT))
    print("Connected to Raspberry Pi robot. Use hand gestures to control.")

    # Setup MediaPipe
    mp_hands = mp.solutions.hands
    mp_draw = mp.solutions.drawing_utils
    hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

    cap = cv2.VideoCapture(0)

    def count_fingers(hand_landmarks):
        fingers = []

        # Thumb
        if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
            fingers.append(1)
        else:
            fingers.append(0)

        # Other fingers
        tips = [8, 12, 16, 20]
        for tip in tips:
            if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
                fingers.append(1)
            else:
                fingers.append(0)

        return sum(fingers)

    last_command = None
    display_text = ""

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                finger_count = count_fingers(hand_landmarks)

                command = None
                if finger_count == 1:
                    command = 'W'
                    display_text = "Moving Forward"
                elif finger_count == 2:
                    command = 'D'
                    display_text = "Turning Right"
                elif finger_count == 3:
                    command = 'A'
                    display_text = "Turning Left"
                elif finger_count == 4:
                    command = 'S'
                    display_text = "Moving Backward"
                elif finger_count == 5:
                    command = 'X'
                    display_text = "Stopping"

                if command and command != last_command:
                    client_socket.send(command.encode())
                    last_command = command

        else:
            display_text = "No Hand Detected"

        # Show live action
        cv2.putText(frame, display_text, (10, 430),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.1, (0, 255, 0), 3)

        # Display gesture control rules
        rules = [
            "Gesture Rules:",
            "1 Finger  = Forward (W)",
            "2 Fingers = Right (D)",
            "3 Fingers = Left (A)",
            "4 Fingers = Backward (S)",
            "5 Fingers = Stop (X)",
            "Press Q to Quit"
        ]
        y_offset = 30
        for i, rule in enumerate(rules):
            cv2.putText(frame, rule, (10, y_offset + i * 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        cv2.imshow("Hand Gesture Control", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            client_socket.send(b'Q')
            break

except Exception as e:
    print(f"Error: {e}")

finally:
    client_socket.close()
    cap.release()
    cv2.destroyAllWindows()
