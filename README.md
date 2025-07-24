Hand Gesture Recognition System - User Manual
1. Overview
This system uses a webcam and hand gestures to recognize letters of the alphabet (A-Z), as well as space and backspace commands. The recognized text is displayed on the screen in real time. This is especially useful for hands-free input and educational applications.
2. System Requirements
- Python 3.7 or higher
- OpenCV
- MediaPipe
- Scikit-learn
- Trained RandomForest model (randomforest_hands.plk)
- Webcam or USB camera
3. Setup Instructions
1. Clone the project or download the code.
2. Install dependencies using:
   pip install opencv-python mediapipe scikit-learn pandas
3. Ensure the trained model file `randomforest_hands.plk` is in the project directory.
4. Run the script using:
   python hand_gesture_predictor.py
4. Gesture Reference Guide:
   use the pdf for the sign guide 
5. Tips for Better Accuracy
- Keep your hand centered in front of the camera.
- Avoid background clutter.
- Use consistent lighting.
- Hold each gesture for 2-3 seconds for proper recognition.
6. Exiting the Application
Press the ESC key while the webcam window is active to close the application.
7. Contact & Support
For any issues or suggestions, contact the developer or raise an issue on the project GitHub repository.
