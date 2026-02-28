#!/bin/bash
# Render build time par ye run hoga

echo "📦 Dependencies install ho rahi hain..."
pip install -r requirements.txt

echo "⬇️ yt-dlp binary download ho raha hai..."
# yt-dlp ka latest binary download karo
wget https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -O /usr/local/bin/yt-dlp
chmod a+rx /usr/local/bin/yt-dlp

# Verify installation
yt-dlp --version
echo "✅ yt-dlp install ho gaya!"
