from flask import Flask, request, jsonify
import os
import subprocess

app = Flask(__name__)

@app.route('/api/generate_animation', methods=['POST'])
def generate_animation():
    # Check if the request contains image and audio files
    if 'image' not in request.files or 'audio' not in request.files:
        return jsonify({"error": "Image and audio files are required"}), 400

    image_file = request.files['image']
    audio_file = request.files['audio']

    # Save the files to temporary location
    image_path = 'temp_image.png'
    audio_path = 'temp_audio.wav'

    image_file.save(image_path)
    audio_file.save(audio_path)

    # Run SadTalker inference script to generate animation
    result_dir = 'results'
    subprocess.run([
        'python3.8',
        'inference.py',
        '--driven_audio',
        audio_path,
        '--source_image',
        image_path,
        '--result_dir',
        result_dir,
        '--still',
        '--preprocess',
        'full',
        '--enhancer',
        'gfpgan'
    ])

    # Get the path of the generated animation
    animation_path = os.path.join(result_dir, 'animation.mp4')

    # Return the path of the generated animation
    return jsonify({"animation_path": animation_path}), 200

if __name__ == '__main__':
    app.run(debug=True)
