# Robot and Camera Simulation

This Python script provides a simulation environment where a robot (represented by an image) moves towards a detected person's face (using a webcam feed). The script integrates the functionalities of Pygame for simulation, OpenCV for webcam access, and face recognition for detecting faces.

## Prerequisites
- Python 3.x
- Pygame
- OpenCV
- face_recognition
- Webcam

## Installation

1. Ensure you have Python installed on your system. If not, download and install it from [Python's official website](https://www.python.org/).
2. Install Pygame by running: pip install pygame
3. Install OpenCV by running: pip install opencv-python-headless
4. Install face_recognition by following the installation instructions from [face_recognition GitHub repository](https://github.com/ageitgey/face_recognition).

## Usage

1. Clone or download the repository to your local machine.
2. Make sure your webcam is connected to your system.
3. Run the Python script: python robot_camera_simulation.py
4. The simulation window will appear, displaying both the webcam feed and the simulation environment.
5. The robot image will move towards any detected face in the webcam feed. If the face matches the known face encodings, the robot will move towards it.

## Configuration

- Adjust the `camera_width` and `camera_height` variables to match your webcam's resolution.
- Make sure to have the face encodings and names of known faces stored in the files `known_face_encodings.pickle` and `known_face_names.pickle` respectively. These files should be generated using face recognition techniques beforehand.
- Modify the paths to the images of the robot (`bot_image`) and the person (`tri_image`) as per your requirements.

## Acknowledgments

- This script utilizes the functionalities of Pygame, OpenCV, and face_recognition libraries. Huge thanks to the contributors of these libraries for their efforts.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

