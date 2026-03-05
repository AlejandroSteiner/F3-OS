# 🎤 Voice Commands - F3-OS Assistant

## Civil Technology: 100% Local, Open Source, No API, No Credits

F3-OS Assistant supports voice commands using **Vosk**, a completely offline, open source and free speech recognition library.

### ✅ Features

- **100% Local**: All processing happens on your machine
- **No API**: Does not require external services
- **No Credits**: Completely free
- **Open Source**: Vosk is Apache 2.0
- **Offline**: Works without internet connection
- **Multi-language**: Supports recognition in multiple languages (Spanish model included)

### 📦 Installation

#### 1. Install Vosk

```bash
cd agent
pip install vosk
```

Or if using virtual environment:

```bash
cd agent
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install vosk
```

#### 2. Download Language Model

Run the installation script:

```bash
./install_vosk_model.sh
```

This script downloads and installs the `vosk-model-small-es-0.22` model (50MB) to `~/vosk-models/`.

**Manual alternative:**

1. Download model from: https://alphacephei.com/vosk/models
2. Recommended: `vosk-model-small-es-0.22` (50MB, Spanish)
3. Extract to: `~/vosk-models/vosk-model-small-es-0.22`

### 🚀 Usage

1. **Start GUI server:**
   ```bash
   cd agent
   ./run.sh gui-server
   ```

2. **Open in browser:**
   ```
   http://localhost:8080
   ```

3. **Click the 🎤 button** next to the text field

4. **Speak your command** when you see "🎤 Recording... Speak now"

5. **The system will recognize your voice** and automatically send the command to the assistant

### 🎯 Example Commands

- "What are your rules?"
- "Explain from scratch"
- "What is the F3 model?"
- "What phase is the system in?"
- "Show me the system status"
- "Learn about voice recognition"

### 🔧 Configuration

The model is automatically searched in these locations:

1. `~/vosk-models/vosk-model-small-es-0.22`
2. `~/vosk-models/vosk-model-es-0.22`
3. `agent/models/vosk-model-small-es-0.22`
4. `agent/models/vosk-model-es-0.22`

### ⚙️ Technical Requirements

- **Browser**: Chrome, Firefox, Edge (Web Audio API support)
- **Microphone**: Access to system microphone
- **Python**: Vosk installed (`pip install vosk`)
- **Model**: Vosk language model downloaded
- **RAM**: ~100-200 MB additional for the model

### 🐛 Troubleshooting

#### "Voice recognition not available"

- Verify Vosk is installed: `pip list | grep vosk`
- Verify model is downloaded in `~/vosk-models/`
- Check server logs for more details

#### "Error accessing microphone"

- Make sure to grant browser permissions to use microphone
- Verify microphone is connected and working
- Try in another browser

#### "No text recognized"

- Speak more clearly and closer to microphone
- Reduce background noise
- Make sure you're speaking in the model's language
- Model works better with complete phrases

### 📚 More Information

- **Vosk**: https://alphacephei.com/vosk/
- **Available models**: https://alphacephei.com/vosk/models
- **Vosk documentation**: https://github.com/alphacep/vosk-api

### 🎨 Integration with F3-OS

Voice commands automatically integrate with:

- ✅ **GUI Assistant**: Processes commands as if they were text
- ✅ **Activity Stream**: Logs voice commands as activities
- ✅ **Internet Learning**: Can search for information based on voice commands
- ✅ **Autonomous Executor**: Can execute recognized commands

### 💡 Notes

- Recognition works better with complete phrases
- Accuracy improves with a quality microphone
- Processing is local, so there's no network latency
- Commands are processed in real-time

---

**Civil Technology**: Vosk is completely free, open source and works 100% local. No API, credits or external services required. Perfect for F3-OS.
