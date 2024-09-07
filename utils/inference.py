import cv2
import numpy as np
from ultralytics import YOLO

def inference(model_path, image_path):
    
    def load_model(model_path):
        model = YOLO(model_path)
        return model

    def load_image(image_path):
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image
    
    model = load_model(model_path)
    results = model(image_path)

    image = load_image(image_path)
    annotated_image = image.copy()
    overlay = np.zeros_like(image, dtype=np.uint8)

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            confidence = box.conf[0]
            class_id = int(box.cls[0])

            cv2.rectangle(annotated_image, (x1, y1), (x2, y2), (255, 255, 255), 2)

            label = f"{confidence:.2f}"
            cv2.putText(annotated_image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            cv2.rectangle(overlay, (x1, y1), (x2, y2), (0, 0, 0), -1)

    annotated_image = cv2.addWeighted(annotated_image, 0.7, overlay, 0.3, 0)

    return annotated_image
