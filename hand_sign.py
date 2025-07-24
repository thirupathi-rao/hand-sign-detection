import cv2
import time
import pickle
import mediapipe as mp
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# Load the trained RandomForestClassifier model
with open("randomforest_hands.plk", "rb") as f:
    rfc = pickle.load(f)

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    model_complexity=1,
    min_detection_confidence=0.8,
    min_tracking_confidence=0.8
)

# Drawing utility
mp_drawing = mp.solutions.drawing_utils

# Start webcam
vid = cv2.VideoCapture(1)

# Prediction history and delay control
prediction_text = []
prediction_delay = 3  # seconds between predictions
last_prediction_time = 0

while True:
    success, frame = vid.read()
    if not success:
        break

    # Convert to RGB
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    current_time = time.time()

    if result.multi_hand_landmarks:
        row = []
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            for point in hand_landmarks.landmark:
                row.extend([point.x, point.y, point.z])

        if len(row) == 63:
            input_df = pd.DataFrame([row])
            try:
                # Only predict if enough time has passed
                if current_time - last_prediction_time > prediction_delay:
                    prediction = rfc.predict(input_df)[0]
                    last_prediction_time = current_time

                    if prediction == "backspace":
                        if prediction_text:
                            prediction_text.pop()
                    else:
                        prediction_text.append(prediction)
            except Exception as e:
                print(f"Prediction Error: {e}")

    # Join predicted characters
    display_text = "".join(prediction_text)

    # Overlay prediction and cooldown timer
    cv2.putText(frame, f"Predicted: {display_text}", (50, 100),
                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

    time_left = max(0, prediction_delay - (current_time - last_prediction_time))
    if time_left > 0:
        cv2.putText(frame, f"Next prediction in: {time_left:.1f}s", (50, 150),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    # Show the frame
    cv2.imshow("Hand Gesture Recognition", frame)

    # Press ESC to exit
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Cleanup
vid.release()
cv2.destroyAllWindows()
