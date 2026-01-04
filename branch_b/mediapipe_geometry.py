import numpy as np
import cv2
import logging
import mediapipe as mp

mp_holistic = mp.solutions.holistic

# Global reusable holistic model
_HOLISTIC = mp_holistic.Holistic(
    static_image_mode=True,
    model_complexity=1,
    refine_face_landmarks=False,
)

def _landmark_stats(landmarks, img_w: int, img_h: int):
    xs = [lm.x * img_w for lm in landmarks.landmark]
    ys = [lm.y * img_h for lm in landmarks.landmark]
    x1, x2 = float(min(xs)), float(max(xs))
    y1, y2 = float(min(ys)), float(max(ys))
    cx, cy = float((x1 + x2) / 2.0), float((y1 + y2) / 2.0)
    return {
        "bbox": [x1, y1, x2, y2],
        "centroid": [cx, cy],
        "count": len(landmarks.landmark),
    }

def mediapipe_geometry_from_bytes(image_bytes: bytes) -> dict:
    try:
        img = cv2.imdecode(
            np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR
        )
        if img is None:
            return {"error": "Invalid image for mediapipe"}

        h, w = img.shape[:2]
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        out = {
            "has_face": False,
            "has_left_hand": False,
            "has_right_hand": False,
            "has_pose": False,
            "face": None,
            "left_hand": None,
            "right_hand": None,
            "pose": None,
        }

        res = _HOLISTIC.process(rgb)

        if res.face_landmarks:
            out["has_face"] = True
            out["face"] = _landmark_stats(res.face_landmarks, w, h)

        if res.left_hand_landmarks:
            out["has_left_hand"] = True
            out["left_hand"] = _landmark_stats(res.left_hand_landmarks, w, h)

        if res.right_hand_landmarks:
            out["has_right_hand"] = True
            out["right_hand"] = _landmark_stats(res.right_hand_landmarks, w, h)

        if res.pose_landmarks:
            out["has_pose"] = True
            out["pose"] = _landmark_stats(res.pose_landmarks, w, h)

        out["human_interaction_score"] = float(
            (1.0 if out["has_pose"] else 0.0)
            + (0.5 if out["has_face"] else 0.0)
            + (0.5 if out["has_left_hand"] else 0.0)
            + (0.5 if out["has_right_hand"] else 0.0)
        ) / 2.5

        return out

    except Exception as e:
        logging.exception("MediaPipe geometry failed")
        return {"error": str(e)}
