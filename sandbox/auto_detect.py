# auto_detect.py
import argparse
import os
import time
import csv
from datetime import datetime
import cv2
from backend.model_helper import load_model, predict_from_frame, load_class_list

def ensure_dir(d):
    os.makedirs(d, exist_ok=True)

def log_event(csv_path, row):
    write_header = not os.path.exists(csv_path)
    with open(csv_path, "a", newline="") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(["timestamp_utc","filename","label","confidence"])
        writer.writerow(row)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="saved_model.pth", help="Path to model state_dict")
    parser.add_argument("--camera", type=int, default=0)
    parser.add_argument("--interval", type=float, default=1.0, help="seconds between inferences")
    parser.add_argument("--min_confidence", type=float, default=0.5)
    parser.add_argument("--save_dir", type=str, default="captures")
    parser.add_argument("--csv", type=str, default="detections.csv")
    parser.add_argument("--display", action="store_true")
    args = parser.parse_args()

    ensure_dir(args.save_dir)

    print("Loading model...")
    model, classes = load_model(args.model)
    print(f"Loaded model with {len(classes)} classes: {classes}")

    cap = cv2.VideoCapture(args.camera)
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open camera index {args.camera}")

    last_time = 0.0
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                time.sleep(0.5)
                continue

            now = time.time()
            if now - last_time >= args.interval:
                label, confidence, probs = predict_from_frame(model, frame, classes=classes)
                ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
                text = f"{label} ({confidence:.2f})"
                color = (0,255,0) if "normal" in label.lower() else (0,0,255)
                cv2.putText(frame, text, (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 2)

                print(f"[{ts}] {text}")

                # Save snapshot if damage (not 'normal') OR if very high confidence
                if ("normal" not in label.lower() and confidence >= args.min_confidence) or confidence >= 0.995:
                    fname = os.path.join(args.save_dir, f"{ts}_{label.replace(' ','_')}_{int(confidence*100)}.jpg")
                    cv2.imwrite(fname, frame)
                    log_event(args.csv, [ts, fname, label, f"{confidence:.4f}"])
                    print("Saved:", fname)
                else:
                    # Log lightweight event (no image)
                    log_event(args.csv, [ts, "", label, f"{confidence:.4f}"])

                last_time = now

            if args.display:
                cv2.imshow("AutoCarDetect", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

    except KeyboardInterrupt:
        print("Interrupted by user.")
    finally:
        cap.release()
        if args.display:
            cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
