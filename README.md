# ✋🧮 Hand Gesture Calculator

Welcome to the **Hand Gesture Calculator**, a futuristic Python-based application that lets you perform basic arithmetic operations using just your hand gestures in front of your webcam!

![Hand Gesture Calculator Demo](https://user-images.githubusercontent.com/your-gif-or-screenshot-path.gif)

---

## 🚀 Features

- 👋 Real-time hand gesture detection using **MediaPipe**
- 🧠 Gesture-to-digit recognition using **finger counting**
- ➕ Perform basic operations: **Addition, Subtraction, Multiplication, Division**
- 🗣️ Voice feedback using **pyttsx3**
- 🎥 Live camera feed using **OpenCV**

---

## 📦 Technologies Used

- `Python`
- `OpenCV` for camera access and image processing
- `MediaPipe` for hand tracking
- `pyttsx3` for text-to-speech
- `NumPy` for array operations



# Hardware: A webcam for hand gesture input

### 🚀 Getting Started
 1. Clone the Repo
git clone https://github.com/your-username/hand-gesture-calculator.git
cd hand-gesture-calculator

 2. Set Up a Virtual Environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

 3. Install Dependencies
pip install opencv-python mediapipe pyttsx3

 4. Linux Audio Setup (Optional)
For Linux users, install espeak for pyttsx3:
sudo apt-get install espeak

 5. Check Your Webcam
Ensure your webcam is connected and accessible. Test it in another app if needed.

 6. Launch the App
python gesture_calculator.py

### 🎮 How to Use

Start the App: Run the script, and the webcam feed will open with a cool UI.
Show Your Hand: Use gestures to input numbers and operations (see below).
Watch & Listen: The screen shows your input, current gesture, and last three calculations. Audio feedback confirms every action.
Exit: Press q to quit.

### ✋ Gesture Guide



Gesture
Action
Description



0-5 Fingers
Numbers 0-5
Show 0 to 5 fingers to input a number.


V-Shape (2 fingers spread)
Add (+)
Two fingers apart, like a peace sign. ✌️


Thumb Only
Subtract (-)
Extend thumb, fold other fingers. 👍


3 Fingers Close
Multiply (*)
Three fingers close together. 🤟


L-Shape (2 fingers spread, no thumb)
Divide (/)
Two non-thumb fingers apart. 🤘


2 Fingers Close
Equals (=)
Two fingers touching. ✊


5 Fingers Spread
Clear (C)
Open hand, all fingers spread. 🖐️

---------------------------------------
### Example

Show V-shape for +.
Show 3 fingers for 3.
Show V-shape again to confirm.
Show 2 fingers for 2.
Show 2 fingers close for =.
Result: 3 + 2 = 5 appears on-screen and is spoken aloud. 🎉


### 🛠️ Customization

Gesture Sensitivity: Adjust min_frames or distance thresholds in gesture_calculator.py for better detection.
Input Length: Modify the 10-character limit in the code for larger numbers.
New Gestures: Extend count_fingers to add decimal points or other operations.

### 🐛 Troubleshooting

Camera Not Working? Ensure your webcam is connected and permissions are granted. Try a different USB port.
Gestures Not Detected? Improve lighting, move closer/farther from the camera, or tweak thresholds in count_fingers.
No Audio? On Linux, ensure espeak is installed. On Windows/macOS, pyttsx3 should work automatically.
Performance Issues? Lower the resolution or FPS in the code for smoother operation.

### 🤝 Contributing
Love the project? Want to make it cooler? Here’s how to contribute:

Fork the repo.
Create a feature branch (git checkout -b epic-feature).
Commit your changes (git commit -m "Added epic feature").
Push to GitHub (git push origin epic-feature).
Open a pull request. 🎉


### 🙌 Acknowledgments

MediaPipe: For cutting-edge hand tracking. 
OpenCV: For powerful video processing.
pyttsx3: For seamless text-to-speech.

### 🌟 Star the Repo!
If you enjoy this project, give it a ⭐ on GitHub to show your support!

Built by Sathyaseelan K
----------------------------------
📬 Contact


Email: ksathyaseelan34@gmail.com 


LinkedIn: www.linkedin.com/in/sathyaseelan-dev
