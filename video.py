import cv2
from ultralytics import YOLO  # Import YOLOv8 directly from ultralytics package

# Load the fine-tuned YOLOv8 model from 'best.pt'
model = YOLO(r'C:\Users\markj\work\practice\shoe_detector\runs\detect\train26\weights\best.pt')

# Open video stream (webcam or video file)
cap = cv2.VideoCapture("./outfits.mp4")  # Replace with '0' for webcam or video file path

# Desired output video size (e.g., 800x500)
output_width = 800
output_height = 500

# Get original FPS from the video capture
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Define the codec and create VideoWriter object (save as .mp4)
out = cv2.VideoWriter('output_video_with_annotations.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (output_width, output_height))

# Since your model has only 1 class, the class ID will be 0
shoe_class_id = 0  # Jordan 4 University Blue

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Run YOLOv8 model on each frame (inference)
    results = model(frame)

    # Extract predictions (xyxy format: [x_min, y_min, x_max, y_max, confidence, class])
    detections = results[0].boxes  # Get boxes from the first result

    # Create a copy of the frame to annotate
    annotated_frame = frame.copy()

    # Draw bounding boxes only for 'Jordan 4 University Blue'
    for box in detections:
        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()  # Coordinates of the bounding box
        conf = box.conf.cpu().numpy()  # Confidence score
        class_id = box.cls.cpu().numpy()  # Class ID
        
        if class_id == shoe_class_id:
            label = f"Jordan 4 University Blue {conf:.2f}"
            # Draw bounding box around the detected shoe
            cv2.rectangle(annotated_frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            # Add label for the shoe
            cv2.putText(annotated_frame, label, (int(x1), int(y1)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Resize the annotated frame to the desired output size
    resized_frame = cv2.resize(annotated_frame, (output_width, output_height))

    # Write the resized frame with bounding boxes to the output video
    out.write(resized_frame)

    # Display the resized frame with bounding boxes (optional for real-time viewing)
    cv2.imshow('Jordan 4 Detection', resized_frame)

    # Press 'q' to quit the video early
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
out.release()
cv2.destroyAllWindows()
