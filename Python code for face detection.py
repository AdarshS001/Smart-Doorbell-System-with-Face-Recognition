import requests  # Add this to send updates to ESP32
import cv2
import face_recognition
import serial
import time
import sys

ESP32_IP = "http://192.168.1.4/"  # Change this to your ESP32 IP

try:
    esp = serial.Serial('COM9',115200, timeout=1)
    time.sleep(2)
    print("✅ Serial communication established!")
except serial.SerialException:
    print("❌ Failed to connect to ESP32! Check COM port.")
    sys.exit()

known_faces = {
    "Adarsh": face_recognition.load_image_file(r"C:\Users\Ajay Balu\OneDrive\Desktop\Project\xyz.jpg"),
     "Ajay": face_recognition.load_image_file(r"C:\Users\Ajay Balu\OneDrive\Desktop\Project\ghi.jpg")
}

try:
    known_encodings = {name: face_recognition.face_encodings(img)[0] for name, img in known_faces.items()}
    print("✅ Face encodings completed!")
except IndexError:
    print("❌ Error: One of the known face images does not contain a face.")
    sys.exit()

cam = cv2.VideoCapture(0)

if not cam.isOpened():
    print("❌ Failed to access webcam!")
    sys.exit()

print("✅ Capturing image...")
ret, frame = cam.read()
cam.release()

if not ret:
    print("❌ Failed to capture image!")
    sys.exit()

cv2.imwrite("captured_image.jpg", frame)
captured_img = face_recognition.load_image_file("captured_image.jpg")
captured_encodings = face_recognition.face_encodings(captured_img)

if len(captured_encodings) == 0:
    print("❌ No face detected!")
    esp.write(b"unknown\n")
    requests.get(ESP32_IP + "?status=unknown")  # Send update to website
    sys.exit()

captured_encoding = captured_encodings[0]

face_distances = face_recognition.face_distance(list(known_encodings.values()), captured_encoding)
best_match_idx = face_distances.argmin()

if face_distances[best_match_idx] < 0.6:
    matched_name = list(known_encodings.keys())[best_match_idx]
    print(f"✅ Known person detected: {matched_name}")
    
    message = "known"  # Prepare message
    print(f"Sending to ESP32: {message}")  # Debugging line
    esp.write(message.encode() + b'\n')   # Send to ESP32
else:
    print("❌ Unknown person detected!")
    
    message = "unknown"  # Prepare message
    print(f"Sending to ESP32: {message}")  # Debugging line
    esp.write(message.encode() + b'\n')   # Send to ESP32

print("✅ Data sent to ESP32!")
