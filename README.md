# MY_CAR

Python-based Raspberry Pi robot control project with three control modes:

- Keyboard control
- Voice control
- Hand gesture control

## Files

- `keyboard.py` - Control the robot with `W`, `A`, `S`, `D`, `X`, and `Q`
- `voice.py` - Control the robot using spoken commands
- `hand.py` - Control the robot using webcam hand gestures
- `robot_config.py` - Stores the robot IP address and control/video ports
- `requirements.txt` - Python dependencies for the project

## Requirements

- Python 3
- Raspberry Pi robot server running and reachable on the same network
- Webcam for hand gesture control
- Microphone for voice control

## Installation

Install the required packages:

```bash
pip install -r requirements.txt
```

## Configuration

Update the robot connection settings in `robot_config.py`:

```python
ROBOT_IP = "10.128.230.14"
CONTROL_PORT = 5003
VIDEO_PORT = 5006
```

Change `ROBOT_IP` if your robot uses a different address.

## Usage

### Keyboard Control

```bash
python keyboard.py
```

Controls:

- `W` - Forward
- `A` - Left
- `S` - Backward
- `D` - Right
- `X` - Stop
- `Q` - Quit

### Voice Control

```bash
python voice.py
```

Example commands:

- `go`
- `forward`
- `back`
- `left`
- `right`
- `stop`
- `quit`

### Hand Gesture Control

```bash
python hand.py
```

Gesture mapping:

- `1 finger` - Forward
- `2 fingers` - Right
- `3 fingers` - Left
- `4 fingers` - Backward
- `5 fingers` - Stop

Press `Q` to quit the hand control window.

## Notes

- Make sure the Raspberry Pi robot server is running before starting any controller.
- Voice control uses Google speech recognition, so internet access may be required.
- Hand gesture control uses OpenCV and MediaPipe with your default camera.
