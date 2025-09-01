from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from googletrans import Translator
import re

app = Flask(__name__)
translator = Translator()

def extract_video_id(url):
    regex = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(regex, url)
    return match.group(1) if match else None

@app.route('/translate_youtube', methods=['POST'])
def translate_youtube():
    data = request.json
    url = data.get('url')
    target_lang = data.get('target_lang', 'ar')

    video_id = extract_video_id(url)
    if not video_id:
        return jsonify({'error': 'رابط غير صالح'}), 400

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_text = ' '.join([entry['text'] for entry in transcript])
        translated = translator.translate(full_text, dest=target_lang)
        return jsonify({'translatedText': translated.text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
