#!/bin/bash
# Script to download and install Vosk model for Spanish
# Civil Technology: 100% local, open source, no API, no credits

echo "🎤 Installing Vosk model for voice commands..."
echo ""

# Create directory for models
MODELS_DIR="$HOME/vosk-models"
mkdir -p "$MODELS_DIR"

# Recommended model: vosk-model-small-es-0.22 (50MB, Spanish)
MODEL_NAME="vosk-model-small-es-0.22"
MODEL_URL="https://alphacephei.com/vosk/models/${MODEL_NAME}.zip"
MODEL_PATH="${MODELS_DIR}/${MODEL_NAME}"

# Check if already exists
if [ -d "$MODEL_PATH" ]; then
    echo "✅ Model already exists at: $MODEL_PATH"
    echo "   If you want to reinstall, delete the directory first."
    exit 0
fi

echo "📥 Downloading Spanish Vosk model..."
echo "   URL: $MODEL_URL"
echo "   Approximate size: 50MB"
echo ""

# Download model
cd "$MODELS_DIR"
if command -v wget &> /dev/null; then
    wget "$MODEL_URL" -O "${MODEL_NAME}.zip"
elif command -v curl &> /dev/null; then
    curl -L "$MODEL_URL" -o "${MODEL_NAME}.zip"
else
    echo "❌ Error: You need wget or curl to download the model"
    exit 1
fi

if [ ! -f "${MODEL_NAME}.zip" ]; then
    echo "❌ Error: Could not download the model"
    exit 1
fi

echo "📦 Extracting model..."
unzip -q "${MODEL_NAME}.zip" || {
    echo "❌ Error: Could not extract the model. Do you have unzip installed?"
    echo "   Install with: sudo apt install unzip"
    exit 1
}

# Clean up ZIP file
rm "${MODEL_NAME}.zip"

if [ -d "$MODEL_PATH" ]; then
    echo ""
    echo "✅ Model installed successfully at:"
    echo "   $MODEL_PATH"
    echo ""
    echo "🎤 Voice commands are now available in F3-OS Assistant"
    echo "   Open http://localhost:8080 and click the 🎤 button"
else
    echo "❌ Error: Model was not extracted correctly"
    exit 1
fi
