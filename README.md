Tejas AI - Advanced AI System

📌 Overview

Tejas AI is an advanced AI assistant integrating:

Face Recognition for secure unlocking 🔒

Voice Commands using Speech-to-Text (STT) and Text-to-Speech (TTS) 🎙️

Computer Vision for OCR, barcode scanning, and real-time object detection 📷

AI Chatbot using LLaMA and ChromaDB 🤖

3D Model Reconstruction from real-time camera input 🏗️

Image Generation using a free API 🎨

Modular Design for future automation, GUI, and OS integration



---

🛠️ Features of Tejas AI

🔒 Face Unlock

Tejas AI ensures secure access with face recognition. When you start the system, it scans your face and grants access only if it matches an authorized user.

🎙️ Speech-to-Text (STT) & Text-to-Speech (TTS)

You can interact with the AI using voice commands. It converts speech to text for processing and responds using AI-generated speech.

📄 Optical Character Recognition (OCR)

The AI can scan images and extract text, making it useful for reading documents, handwritten notes, and printed text.

🔍 Barcode & QR Code Scanner

It detects and reads barcodes and QR codes from images or real-time camera input.

🖼️ Image Recognition

The AI can identify objects, scenes, and elements within an image using deep learning-based recognition.

📦 Object Detection

Using advanced computer vision models, the AI detects objects in real time, highlighting and classifying them from a live camera feed.

🌎 Real-Time Environment Scanning

The AI processes the surroundings through a real-time camera feed, identifying objects and analyzing the environment dynamically.

🏗️ 3D Model Reconstruction

By scanning real-world objects, Tejas AI creates a 3D model, reconstructing shapes and structures from camera input.

🎨 AI Image Generation

The system can generate AI-created images based on a text prompt, allowing users to create artwork, designs, and conceptual visuals.

🤖 AI Chatbot with LLaMA & ChromaDB

Tejas AI processes queries intelligently, responding with well-structured answers using an AI chatbot powered by LLaMA and ChromaDB.

🛠️ Modular System

The project is structured into multiple modules, making it easy to extend functionality. Future integrations include Automation, GUI, and OS controls for enhanced AI-powered tasks.


---

🚀 Installation

🔹 Prerequisites

Ensure you have Python 3.8+ installed.

🔹 Install Dependencies

Run the following command to install all required libraries:

pip install -r requirements.txt


---

📂 Project Structure

📂 Tejas AI/
│── 📂 Brain/                     # AI Processing & Knowledge  
│   │── 📜 knowledge.py           # AI response system (formerly tejas_ai.py)  
│   │── 📜 real_time_processor.py # Real-time AI processing  
│   │── 📜 image_generator.py     # AI image generation  
│  
│── 📂 Vision/                    # Computer Vision Capabilities  
│   │── 📜 computer_vision.py     # OCR, barcode, object detection  
│   │── 📜 reconstruct_3d.py      # 3D model generation  
│  
│── 📂 Function/                   # Query Handling & Voice Control  
│   │── 📜 query_classifier.py     # Categorizes queries  
│   │── 📜 stt_tts.py              # Speech-to-Text & Text-to-Speech  
│  
│── 📂 Automation/                 # Reserved for future automation  
│   │── (Empty, will be updated soon)  
│  
│── 📂 GUI/                        # Reserved for graphical interface  
│   │── (Empty, will be updated soon)  
│  
│── 📂 OS/                         # OS-related operations  
│   │── (Empty, will be updated soon)  
│  
│── 📜 main.py                     # Entry point for AI system  
│── 📜 requirements.txt             # Dependencies  
│── 📜 README.md                    # Documentation


---

🛠️ How to Use

1️⃣ Face Unlock

When you run main.py, it will first check your face.

If recognized, access is granted. Otherwise, the system locks.


2️⃣ AI Commands (Text or Voice)

You can either type commands or speak them.


---

👨‍💻 Contributing

Feel free to contribute by improving features or adding new ones!


---

📜 License

This project is open-source under the MIT License.




