import cv2
import face_recognition
from query_categorizer import QueryCategorizer
from tejas_ai import TejasAI
from real_time_processor import RealTimeProcessor
from computer_vision import ComputerVision
from reconstruct_3d import Reconstruct3D
from image_generator import ImageGenerator
from stt_tts import STT, TTS  # Importing STT & TTS

# Initialize image generator (Choose API or Local Model)
use_api = False  # Set to True if using DeepAI API
api_key = "your_deepai_api_key"  # Required if using API


class FaceUnlock:
    """Handles face recognition-based unlocking."""
    
    def __init__(self):
        print("🔒 Face recognition activated for unlocking...")
        self.known_face_encodings = []
        self.known_face_names = []
        self.load_faces()

    def load_faces(self):
        """Load authorized faces for unlocking"""
        try:
            my_image = face_recognition.load_image_file("face.jpg")  # Replace with your face image
            my_face_encoding = face_recognition.face_encodings(my_image)[0]
            self.known_face_encodings.append(my_face_encoding)
            self.known_face_names.append("Authorized User")
        except Exception as e:
            print(f"⚠️ Error loading face: {e}")

    def authenticate(self):
        """Capture camera feed and authenticate"""
        video_capture = cv2.VideoCapture(0)
        
        while True:
            ret, frame = video_capture.read()
            if not ret:
                break

            rgb_frame = frame[:, :, ::-1]  # Convert BGR to RGB
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                if True in matches:
                    print("✅ Access Granted!")
                    video_capture.release()
                    cv2.destroyAllWindows()
                    return True

            cv2.imshow("Face Unlock", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        video_capture.release()
        cv2.destroyAllWindows()
        print("❌ Access Denied!")
        return False


class MainAI:
    """Main AI system that routes queries and commands"""
    
    def __init__(self):
        self.tejas_ai = Knowledge()
        self.real_time_processor = RealTimeProcessor()
        self.vision = ComputerVision()
        self.reconstructor = Reconstruct3D()
        self.image_generator = ImageGenerator(use_api=use_api, api_key=api_key)
        self.query_categorizer = QueryCategorizer()
        self.stt = STT()
        self.tts = TTS()

    def process_command(self, command):
        """Handle different commands"""
        command = command.lower()

        if "scan text" in command:
            result = self.vision.scan_text()
            print("📝 Scanned Text:", result)
            self.tts.speak("Here is the scanned text.")

        elif "scan code" in command:
            result = self.vision.scan_barcode()
            print("🔍 Scanned Code:", result)
            self.tts.speak("Barcode scanned successfully.")

        elif "scan image" in command:
            result = self.vision.recognize_image()
            print("🖼️ Image Recognized:", result)
            self.tts.speak("Image recognition completed.")

        elif "detect object" in command:
            result = self.vision.detect_objects()
            print("📦 Detected Objects:", result)
            self.tts.speak("Object detection successful.")

        elif "scan real time environment" in command:
            result = self.vision.scan_real_time()
            print("🌎 Real-time Environment Scanned.")
            self.tts.speak("Real-time scanning done.")

        elif "make a 3d model" in command:
            self.reconstructor.create_3d_model()
            print("🛠️ 3D Model Created!")
            self.tts.speak("3D model created successfully.")

        elif command.startswith("generate an image"):
            result = self.image_generator.generate_image(command)

            if use_api:
                print(f"🖼️ Image generated: {result}")  # Display URL
                self.tts.speak("Image generated successfully.")
            else:
                result.show()  # Display image locally
                self.tts.speak("Image displayed.")

        elif "listen mode" in command:
            print("🎙️ Entering voice command mode...")
            self.tts.speak("Voice mode activated. Say your command.")
            spoken_command = self.stt.listen()
            if spoken_command:
                self.process_command(spoken_command)

        else:
            # Categorize the query and route accordingly
            category = self.query_categorizer.categorize(command)

            if category == "general":
                response = self.tejas_ai.get_response(command)
            else:
                response = self.real_time_processor.process(command)

            print("🤖 AI Response:", response)
            self.tts.speak(response)


if __name__ == "__main__":
    face_unlock = FaceUnlock()

    if face_unlock.authenticate():
        print("🔹 Welcome to the Tejas AI System")
		self.tts.speak(" Welcome to the Tejas AI System")
        main_ai = MainAI()

        while True:
			self.tts.speak("Enter Command (or type 'listen mode' for voice commands")
            command = input("\n💬 Enter Command (or type 'listen mode' for voice commands): ")
            if command.lower() in ["exit", "quit"]:
                print("🚪 Exiting AI System...")
                break
            main_ai.process_command(command)
    else:
        print("🔒 System Locked. Unauthorized Access Denied!")
		self.tts.speak("System Locked. Unauthorized Access Denied!")