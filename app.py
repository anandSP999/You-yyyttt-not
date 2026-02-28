from flask import Flask, request, jsonify, render_template
import subprocess
import json
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # Frontend serve karega

@app.route('/get_video_url', methods=['POST'])
def get_video_url():
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({'error': 'URL nahi mila'}), 400

    try:
        # yt-dlp command: best video+audio format ka direct URL lo
        command = [
            'yt-dlp',
            '-g',  # Sirf URL output karo (download mat karo)
            '-f', 'best[ext=mp4]/best',  # Best mp4 format chahiye
            url
        ]
        
        # Command run karo
        result = subprocess.run(command, capture_output=True, text=True, timeout=30)
        
        if result.returncode != 0:
            return jsonify({'error': f'yt-dlp error: {result.stderr}'}), 500
        
        # Pehli line mein video URL milega
        video_url = result.stdout.strip().split('\n')[0]
        
        if video_url:
            return jsonify({'video_url': video_url})
        else:
            return jsonify({'error': 'Video URL generate nahi hua'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))