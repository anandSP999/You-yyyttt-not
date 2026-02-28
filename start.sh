#!/bin/bash
# yt-dlp install karo aur server start karo

echo "🚀 yt-dlp install ho raha hai..."
pip install --upgrade yt-dlp

echo "🚀 Server start ho raha hai..."
gunicorn app:app
