import face_recognition
import cv2
import numpy as np
import pickle
print("Open recognition successfully!")
# Load the known faces and encodings saved from before
with open('known_face_encodings.pickle', 'rb') as f:
    known_face_encodings = pickle.load(f)

with open('known_face_names.pickle', 'rb') as f:
    known_face_names = pickle.load(f)
net = cv2.dnn.readNetFromCaffe(
    'deploy.prototxt', 'res10_300x300_ssd_iter_140000.caffemodel')


video_capture = cv2.VideoCapture(0)

if not video_capture.isOpened():
    raise IOError("Cannot open webcam")

while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(
        frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()

    # Loop over the detections
    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.7:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            # Extract the face ROI and convert it to RGB for face_recognition
            face = frame[startY:endY, startX:endX]
            face_rgb = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            face_encodings = face_recognition.face_encodings(face_rgb)

            name = "Stranger"  # Default to Stranger for each face detected
            box_color = (0, 255, 0)
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(
                    known_face_encodings, face_encoding, tolerance=0.5)
                face_distances = face_recognition.face_distance(
                    known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                 # Determine the color of the box based on the name
                if name == "Bui Dinh Tri":
                    box_color = (0, 0, 255)
                    action_text = "Robot moving forward Tri with the speed of 20 for 1 second"
                    cv2.putText(
                        frame, action_text, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                    # Write to the signal file
                    with open('signal.txt', 'w') as signal_file:
                        signal_file.write('detected\n')

            # Draw the box around the face with the name
            cv2.rectangle(frame, (startX, startY), (endX, endY), box_color, 2)
            cv2.putText(frame, name, (startX, startY - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, box_color, 2)

    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


video_capture.release()
cv2.destroyAllWindows()
