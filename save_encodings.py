import face_recognition
import os
import pickle

images_path = './buidinhtri'
known_face_encodings = []
known_face_names = []

image_filenames = [f for f in os.listdir(images_path) if os.path.isfile(os.path.join(images_path, f))]

for image_filename in image_filenames:
    image = face_recognition.load_image_file(os.path.join(images_path, image_filename))
    encodings = face_recognition.face_encodings(image)
    if encodings:
        known_face_encodings.append(encodings[0])
        known_face_names.append("Bui Dinh Tri")
    else:
        print(f"No faces found in the image {image_filename}.")

# Save the encodings and names
with open('known_face_encodings.pickle', 'wb') as f:
    pickle.dump(known_face_encodings, f)

with open('known_face_names.pickle', 'wb') as f:
    pickle.dump(known_face_names, f)
