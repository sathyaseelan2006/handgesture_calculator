import cv2
import mediapipe as mp
import numpy as np
import pyttsx3
import time
import queue
from threading import Thread, Lock
import uuid

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Voice Engine
class VoiceEngine:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 160)
        self.queue = queue.Queue()
        self.lock = Lock()
        self.running = True
        self.thread = Thread(target=self._process_queue)
        self.thread.daemon = True
        self.thread.start()

    def speak(self, text):
        with self.lock:
            self.engine.stop()  # Stop current speech to avoid overlap
            self.queue.put(text)

    def _process_queue(self):
        while self.running:
            try:
                text = self.queue.get(timeout=0.1)
                self.engine.say(text)
                self.engine.runAndWait()
                self.queue.task_done()
            except queue.Empty:
                continue

    def stop(self):
        self.running = False
        self.thread.join()
        self.engine.stop()

voice = VoiceEngine()

# Calculator State
current_input = ""
stored_number = 0
current_operation = None
last_gesture_time = time.time()
calculation_history = []
gesture_counts = {}
min_frames = 5  # Number of frames to confirm a gesture

# Gesture Mapping
OPERATIONS = {
    'add': '+',
    'subtract': '-',
    'multiply': '*',
    'divide': '/',
    'equals': '=',
    'clear': 'C'
}

def dist(a, b):
    return ((a.x - b.x) ** 2 + (a.y - b.y) ** 2) ** 0.5

def normalize_distance(a, b, hand_landmarks):
    wrist = hand_landmarks.landmark[0]
    palm = hand_landmarks.landmark[5]
    hand_size = dist(wrist, palm)
    return dist(a, b) / hand_size if hand_size > 0 else 0

def count_fingers(hand_landmarks):
    tips = [4, 8, 12, 16, 20]
    mcp = [2, 5, 9, 13, 17]
    fingers = 0
    thumb_extended = hand_landmarks.landmark[tips[0]].x < hand_landmarks.landmark[mcp[0]].x

    if thumb_extended:
        fingers += 1

    for i in range(1, 5):
        if hand_landmarks.landmark[tips[i]].y < hand_landmarks.landmark[mcp[i]].y:
            fingers += 1

    # Normalized gesture distances
    d_im = normalize_distance(hand_landmarks.landmark[8], hand_landmarks.landmark[12], hand_landmarks)
    d_mr = normalize_distance(hand_landmarks.landmark[12], hand_landmarks.landmark[16], hand_landmarks)

    if fingers == 2 and d_im > 0.3:
        return 'add'
    elif fingers == 1 and thumb_extended:
        return 'subtract'
    elif fingers == 2 and d_im < 0.1:
        return 'equals'
    elif fingers == 3 and d_mr < 0.1:
        return 'multiply'
    elif fingers == 2 and not thumb_extended and d_im > 0.2:
        return 'divide'
    elif fingers == 5:
        return 'clear'
    else:
        return str(fingers)

def perform_calculation():
    global stored_number, current_input, current_operation, calculation_history

    if not current_input or current_operation is None:
        voice.speak("Incomplete operation")
        return

    try:
        current_num = float(current_input)
        if abs(current_num) > 1e10 or abs(stored_number) > 1e10:
            voice.speak("Number too large")
            return
    except ValueError:
        voice.speak("Invalid input")
        return

    result = None
    if current_operation == '+':
        result = stored_number + current_num
    elif current_operation == '-':
        result = stored_number - current_num
    elif current_operation == '*':
        result = stored_number * current_num
    elif current_operation == '/':
        if current_num != 0:
            result = stored_number / current_num
        else:
            voice.speak("Error: Division by zero")
            return

    calculation_history.append(f"{stored_number} {current_operation} {current_num} = {result:.2f}")
    if len(calculation_history) > 5:
        calculation_history.pop(0)

    voice.speak(f"The result is {result:.2f}")
    current_input = str(round(result, 2))
    stored_number = 0
    current_operation = None

def draw_ui(frame, width, height, gesture=None):
    # Draw input display
    cv2.rectangle(frame, (20, 20), (width - 20, 100), (30, 30, 30), -1)
    display_text = current_input[-10:] if current_input else "0"
    if current_operation and stored_number:
        display_text = f"{stored_number} {current_operation} {display_text}"
    cv2.putText(frame, display_text, (30, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)

    # Draw current gesture
    if gesture:
        cv2.putText(frame, f"Gesture: {gesture}", (30, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

    # Draw gesture guide
    cv2.putText(frame, "1-5: Numbers | V:+ | Thumb:- | 3Tight:* | L:/ | 5Open:C | 2Tight:=",
                (20, height - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 255, 100), 1)

    # Draw calculation history
    for i, calc in enumerate(calculation_history[-3:]):
        cv2.putText(frame, calc, (30, 160 + i * 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)

# Initialize Camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open camera")
    voice.speak("Error: Could not open camera")
    exit()

cap.set(cv2.CAP_PROP_FPS, 30)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

voice.speak("Hand gesture calculator ready. Show your hand to start.")

try:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        height, width, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        current_gesture = None
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                gesture = count_fingers(hand_landmarks)
                gesture_counts[gesture] = gesture_counts.get(gesture, 0) + 1
                if gesture_counts[gesture] >= min_frames:
                    current_gesture = gesture
                    for key in gesture_counts:
                        gesture_counts[key] = 0  # Reset counts

        if current_gesture and time.time() - last_gesture_time > 0.8:
            last_gesture_time = time.time()
            if current_gesture in OPERATIONS:
                op = OPERATIONS[current_gesture]
                if op == 'C':
                    current_input = ""
                    stored_number = 0
                    current_operation = None
                    voice.speak("Calculator cleared")
                elif op == '=':
                    perform_calculation()
                else:
                    if current_input:
                        try:
                            stored_number = float(current_input)
                            current_operation = op
                            current_input = ""
                            voice.speak(f"{stored_number} {op}")
                        except ValueError:
                            voice.speak("Invalid number")
                    else:
                        voice.speak("Enter a number first")
            else:
                if len(current_input) < 10:
                    current_input += current_gesture
                    voice.speak(current_gesture)

        draw_ui(frame, width, height, current_gesture)
        cv2.imshow("Hand Gesture Calculator", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
    voice.speak("Calculator shutting down")
    voice.stop()
    hands.close()