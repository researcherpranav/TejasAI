import cv2
import pytesseract
from pyzbar.pyzbar import decode
import torch
import torchvision.transforms as transforms
from torchvision import models

class ComputerVision:
    def __init__(self):
        """Initialize Computer Vision functionalities"""
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Load Object Detection Model (Faster R-CNN)
        self.model = models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
        self.model.to(self.device)
        self.model.eval()

        # Label Mapping for COCO Dataset (Common Objects in Context)
        self.labels = {i: label for i, label in enumerate([
            '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train',
            'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench',
            'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe',
            'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard',
            'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
            'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana',
            'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake',
            'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse',
            'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator',
            'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
        ])}

    def extract_text_from_image(self, image_path):
        """Extract text from an image using OCR"""
        image = cv2.imread(image_path)
        return pytesseract.image_to_string(image)

    def extract_text_from_camera(self):
        """Extract text from live camera feed"""
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            text = pytesseract.image_to_string(frame)
            cv2.imshow("OCR Live", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()
        return text

    def scan_barcode(self):
        """Scan a QR code or Barcode from live camera"""
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            decoded_objects = decode(frame)
            for obj in decoded_objects:
                cap.release()
                cv2.destroyAllWindows()
                return obj.data.decode("utf-8")  # Return barcode data

            cv2.imshow("Barcode Scanner", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()
        return None

    def detect_objects(self):
        """Detect objects from live camera feed"""
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Convert to Tensor
            transform = transforms.Compose([transforms.ToPILImage(), transforms.ToTensor()])
            img_tensor = transform(frame).to(self.device).unsqueeze(0)

            # Detect Objects
            with torch.no_grad():
                preds = self.model(img_tensor)[0]

            for i in range(len(preds["labels"])):
                score = preds["scores"][i].item()
                if score > 0.5:
                    label = self.labels.get(preds["labels"][i].item(), "Unknown")
                    box = preds["boxes"][i].cpu().numpy().astype(int)

                    # Draw Bounding Box
                    cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)
                    cv2.putText(frame, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            cv2.imshow("Object Detection", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()

    def scan_real_time_environment(self):
        """Detect objects, recognize text, and scan barcodes in real-time"""
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            text = pytesseract.image_to_string(frame)
            barcode = self.scan_barcode()

            print("📝 Text:", text)
            print("📌 Barcode Data:", barcode)

            self.detect_objects()  # Run object detection

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()
