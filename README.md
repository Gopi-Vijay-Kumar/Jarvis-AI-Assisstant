# JARVIS AI Assistant

A Python-based voice assistant designed to perform various tasks through voice commands, featuring wake-word detection and text-to-speech capabilities.

## 🚀 Features
* **Wake Word Detection**: Responds to specific wake words like "wake up", "jarvis", and "computer". 
* **Voice Commands**: Can search Wikipedia, open YouTube or Google Chrome, tell jokes, and provide the current time. 
* **Audio Feedback**: Provides spoken responses and chime sound effects for activation and deactivation. 
* **System Controls**: Includes a "standby" mode and the ability to exit via voice command.

## 🛠️ Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Gopi-Vijay-Kumar/Jarvis-AI-Assisstant.git
   cd Jarvis-AI-Assisstant
   ```
2. **Install Dependencies**:
   Ensure you have Python installed, then run:
   ```bash
   pip install -r requirements.txt
   ```
   
## 🎙️ How to Use

1. **Run the Script**:
   ```bash
   python "jarvis ai assisstant.py"
   ```
2. **Calibrate**: The system will automatically calibrate your microphone for ambient noise upon initialization.
3. **Wake Up**: Say one of the configured wake words: **"wake up"**, **"jarvis"**, **"hey jarvis"**, **"computer"**, or **"hey computer"**.
4.  **Give a Command**: Once JARVIS is listening, you can say:
  * *"Search Wikipedia for [topic]"*
  * *"Open YouTube"*
  * *"Open Google Chrome"*
  * *"What time is it?"*
  * *"Tell me a joke"*
  * *"Go to sleep"* or *"Stop listening"* to return to standby.
  * *"Exit"*, *"Quit"*, or *"Shutdown"* to close the program.
5. **Standby and Exit**:
  * After completing a task, JARVIS will say *"Returning to standby"* and play a **deactivation chime**. 
  * It will remain in the background until you use a **Wake Word** again.
  * To fully close the program, simply say: **"exit"**, **"quit"**, or **"shutdown"**.
