import mediapipe as mp
import numpy as np
import cv2

class GestureDetector:
    def __init__(self, config):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=config['hand_detection_confidence'],
            min_tracking_confidence=0.5
        )
        self.reach_threshold = config['reach_threshold']
        self.grasp_threshold = config['grasp_threshold']
        self.release_threshold = config['release_threshold']
        self.movement_history = []
        self.history_size = 10  # Number of frames to keep in history

    def detect(self, frame):
        results = self.hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        return results.multi_hand_landmarks

    def classify_gestures(self, hand_landmarks, person_bbox):
        gestures = []
        for landmarks in hand_landmarks:
            gesture = self.classify_single_hand_gesture(landmarks, person_bbox)
            if gesture:
                gestures.append(gesture)
        return gestures

    def classify_single_hand_gesture(self, landmarks, person_bbox):
        # Convert landmarks to numpy array for easier calculations
        points = np.array([[lm.x, lm.y, lm.z] for lm in landmarks.landmark])

        # Update movement history
        self.update_movement_history(points[0])  # Use wrist point for movement tracking

        if self.is_reaching(points, person_bbox):
            return "Reaching"
        elif self.is_grasping(points):
            return "Grasping"
        elif self.is_releasing(points):
            return "Releasing"
        elif self.is_holding(points):
            return "Holding"
        else:
            return None

    def update_movement_history(self, wrist_point):
        self.movement_history.append(wrist_point)
        if len(self.movement_history) > self.history_size:
            self.movement_history.pop(0)

    def is_reaching(self, points, person_bbox):
        wrist = points[0]
        fingertips = points[[4, 8, 12, 16, 20]]  # thumb, index, middle, ring, pinky tips

        # Check if the hand is moving towards the shelf area
        if len(self.movement_history) >= 2:
            movement_vector = self.movement_history[-1] - self.movement_history[0]
            if movement_vector[1] < -self.reach_threshold:  # Moving upwards
                # Check if fingers are extended
                if np.all(fingertips[:, 1] < wrist[1]):
                    # Check if hand is above the person's shoulder (assumed to be top 1/3 of bounding box)
                    shoulder_height = person_bbox[1] + person_bbox[3] / 3
                    if wrist[1] < shoulder_height:
                        return True
        return False

    def is_grasping(self, points):
        thumb_tip = points[4]
        index_tip = points[8]
        middle_tip = points[12]

        # Calculate distances between fingertips
        thumb_index_distance = np.linalg.norm(thumb_tip - index_tip)
        thumb_middle_distance = np.linalg.norm(thumb_tip - middle_tip)

        # Check if thumb is close to index and middle fingers
        if thumb_index_distance < self.grasp_threshold and thumb_middle_distance < self.grasp_threshold:
            return True
        return False

    def is_releasing(self, points):
        if len(self.movement_history) < 2:
            return False

        wrist = points[0]
        fingertips = points[[4, 8, 12, 16, 20]]

        # Check if fingers are extending
        fingers_extending = np.all(fingertips[:, 1] < wrist[1])

        # Check if hand is moving downwards
        movement_vector = self.movement_history[-1] - self.movement_history[0]
        moving_down = movement_vector[1] > self.release_threshold

        return fingers_extending and moving_down

    def is_holding(self, points):
        # Similar to grasping, but with less movement
        if self.is_grasping(points):
            if len(self.movement_history) >= 2:
                movement = np.linalg.norm(self.movement_history[-1] - self.movement_history[0])
                if movement < self.release_threshold:
                    return True
        return False

    def visualize_gesture(self, frame, landmarks, gesture):
        if landmarks:
            mp_drawing = mp.solutions.drawing_utils
            mp_drawing.draw_landmarks(frame, landmarks, self.mp_hands.HAND_CONNECTIONS)

            # Get the bounding box of the hand
            x_coords = [lm.x for lm in landmarks.landmark]
            y_coords = [lm.y for lm in landmarks.landmark]
            text_x = int(min(x_coords) * frame.shape[1])
            text_y = int(min(y_coords) * frame.shape[0]) - 10

            # Draw the detected gesture
            cv2.putText(frame, gesture, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        return frame