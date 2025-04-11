import torch
import argparse
import cv2
import os
from pathlib import Path

def load_model(weights='yolov5s.pt'):
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=weights, force_reload=True)
    return model

def detect(model, source='0', output_dir='runs/detect-custom', img_size=640, conf_thres=0.25):
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Handle source type: webcam, video, or image
    if source.isnumeric():
        cap = cv2.VideoCapture(int(source))
    else:
        cap = cv2.VideoCapture(source)

    if not cap.isOpened():
        print(f"[ERROR] Cannot open source: {source}")
        return

    print("[INFO] Starting detection...")
    frame_id = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame, size=img_size)
        annotated_frame = results.render()[0]

        # Save each frame with detections
        output_path = Path(output_dir) / f'frame_{frame_id:04d}.jpg'
        cv2.imwrite(str(output_path), annotated_frame)

        # Display the output
        cv2.imshow("YOLOv5 Detection", annotated_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame_id += 1

    cap.release()
    cv2.destroyAllWindows()
    print(f"[INFO] Detection complete. Results saved to {output_dir}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', type=str, default='yolov5s.pt', help='Path to weights file')
    parser.add_argument('--source', type=str, default='0', help='Path to image/video or webcam index')
    parser.add_argument('--img-size', type=int, default=640, help='Inference image size')
    parser.add_argument('--conf-thres', type=float, default=0.25, help='Confidence threshold')
    parser.add_argument('--output-dir', type=str, default='runs/detect-custom', help='Output directory')

    opt = parser.parse_args()

    model = load_model(weights=opt.weights)
    detect(model, source=opt.source, output_dir=opt.output_dir, img_size=opt.img_size, conf_thres=opt.conf_thres)

if __name__ == '__main__':
    main()
