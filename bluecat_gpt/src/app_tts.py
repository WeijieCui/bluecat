import os
import re
import time
from datetime import datetime

import pyttsx3
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS

import whisper
from openai import OpenAI

app = Flask(__name__)
CORS(app, origins='*')

client = OpenAI(
    api_key= os.environ.get("OPENAI_API_KEY"),
)

model = whisper.load_model("small")

engine = pyttsx3.init()

PATTERN = r'(\n)|\*|#|-'


@app.route('/bluecat_bk/chat', methods=['POST'])
def chat():
    print('receive a request:', time.time())
    t0 = time.time()
    audio_file = request.files['audio']
    t = datetime.now().strftime('%Y%m%d%H%M%S')
    input_file = "input_{}.webm".format(t)
    output_file = "out_{}.mp3".format(t)
    audio_file.save(input_file)
    t1 = time.time()
    print('save file:', t1 - t0)
    result = model.transcribe(input_file)
    t2 = time.time()
    print('transcribe: ', result['text'], t2 - t1)
    response = client.chat.completions.create(
        messages=[
            {
                'role': 'user',
                'content': result["text"],
            }
        ],
        model="gpt-4o-2024-05-13",
    )
    complement = fine_response(response.choices[0].message.content)
    t3 = time.time()
    print({
        'time': t3 - t2,
        'input': result['text'],
        'output': complement,
        'prompt_tokens': response.usage.prompt_tokens,
        'completion_tokens': response.usage.completion_tokens,
    })
    # complement_voice = gTTS(text=complement, lang=result['language'], slow=False)
    # complement_voice.save(output_file)
    engine.save_to_file(complement, filename=output_file)
    engine.runAndWait()
    print('save file: ', time.time() - t3, 'total:', time.time() - t0)
    return send_file(output_file, mimetype='audio/mpeg')


def fine_response(text: str) -> str:
    return re.sub(PATTERN, '', text)


@app.errorhandler(404)
def not_found(e):
    return jsonify({"message": "Not Found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
    # print(fine_response('abc*ced*.eef\n\n1abc'))
