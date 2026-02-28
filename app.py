from flask import Flask, request, jsonify, render_template
import subprocess
import os
import shutil

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_video_url', methods=['POST'])
def get_video_url():
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({'error': 'URL nahi mila'}), 400

    try:
        # yt-dlp ka path check karo
        yt_dlp_path = shutil.which('yt-dlp')
        if not yt_dlp_path:
            return jsonify({'error': 'yt-dlp server par install nahi hai'}), 500
        
        print(f"🎯 yt-dlp found at: {yt_dlp_path}")
        print(f"🎯 Processing URL: {url}")
        
        # Command: best video+audio format ka direct URL lo
        command = [
            yt_dlp_path,
            '-g',  # Sirf URL output karo
            '-f', 'best[ext=mp4]/best',  # Best mp4 format
            '--no-playlist',  # Sirf ek video, playlist nahi
            url
        ]
        
        print(f"🚀 Running command: {' '.join(command)}")
        
        # Command run karo
        result = subprocess.run(
            command, 
            capture_output=True, 
            text=True, 
            timeout=60,
            env=os.environ.copy()
        )
        
        print(f"✅ Return code: {result.returncode}")
        print(f"📤 stdout: {result.stdout[:200]}...")  # Pehle 200 chars
        
        if result.returncode != 0:
            error_msg = result.stderr or "Unknown error"
            print(f"❌ yt-dlp error: {error_msg}")
            return jsonify({'error': f'yt-dlp error: {error_msg[:200]}'}), 500
        
        # Pehli line mein video URL milega
        video_url = result.stdout.strip().split('\n')[0]
        
        if video_url and video_url.startswith('http'):
            print(f"✅ Video URL mil gaya!")
            return jsonify({'video_url': video_url})
        else:
            return jsonify({'error': 'Video URL generate nahi hua'}), 500
            
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Timeout: video load karne mein zyada time lag raha hai'}), 500
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/check_ytdlp', methods=['GET'])
def check_ytdlp():
    """yt-dlp install hai ya nahi check karne ke liye endpoint"""
    yt_dlp_path = shutil.which('yt-dlp')
    if yt_dlp_path:
        try:
            result = subprocess.run(['yt-dlp', '--version'], capture_output=True, text=True)
            version = result.stdout.strip()
            return jsonify({
                'installed': True,
                'path': yt_dlp_path,
                'version': version
            })
        except:
            return jsonify({'installed': False, 'error': 'version check failed'})
    else:
        return jsonify({'installed': False, 'error': 'not found in PATH'})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
