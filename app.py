from flask import Flask, render_template, request, jsonify, send_file
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index_1.html')

@app.route('/process', methods=['POST'])
def process():
    input_text = request.form.get('text') 
    voice_selection = request.form.get('modelVoice')

    if input_text:  
        with open("inputText.txt", "w") as file:
            file.write(input_text)

        with open("model.txt", "w") as file:
            file.write(voice_selection)
        
        try:
            subprocess.run(['python3', 'createVid.py'], check=True)
            video_path = 'fullVid.mp4'

            if os.path.exists(video_path):
                result = "Video created successfully."
                video_url = f"/download/{video_path}" 
            else:
                result = "Error: Video creation failed."
                video_url = None
        except subprocess.CalledProcessError:
            result = "Error: Failed to generate video."
            video_url = None
    else:
        result = "Error: No input provided."
        video_url = None

    return jsonify({"result": result, "video_url": video_url})

@app.route('/generate_story', methods=['POST'])
def generate_story():
    story_type = request.form.get('storyType')

    if story_type:
        # Store the selected story type in storyType.txt
        with open("storyType.txt", "w") as file:
            file.write(story_type)

        try:
            subprocess.run(['python3', 'genScript.py'], check=True)

            return jsonify({"result": "Story generated successfully."})
        except subprocess.CalledProcessError:
            return jsonify({"result": "Error: Story generation failed."})

    return jsonify({"result": "Error: No story type selected."})

@app.route('/get_generated_story')
def get_generated_story():
    if os.path.exists('inputText.txt'):
        with open('inputText.txt', 'r') as file:
            generated_story = file.read()
        return generated_story
    else:
        return "Error: Generated story not found."

@app.route('/download/<path:filename>')
def download_file(filename):
    return send_file(filename, as_attachment=True)

@app.route('/convert_to_brainrot', methods=['POST'])
def convert_to_brainrot():
    try:
        subprocess.run(['python3', 'genBrainrot.py'], check=True)

        if os.path.exists('inputText.txt'):
            with open('inputText.txt', 'r') as file:
                brainrot_text = file.read()
            return jsonify({"result": "Conversion successful.", "brainrot_text": brainrot_text})
        else:
            return jsonify({"result": "Error: Processed text not found."})
    except subprocess.CalledProcessError:
        return jsonify({"result": "Error: Brainrot conversion failed."})

@app.route('/get_reddit_story', methods=['POST'])
def get_reddit_story():
    subreddit = request.form.get('subreddit')

    if subreddit:
        with open("subreddit.txt", "w") as file:
            file.write(subreddit)

        try:
            subprocess.run(['python3', 'reddit.py'], check=True)

            if os.path.exists('inputText.txt'):
                with open('inputText.txt', 'r') as file:
                    reddit_story = file.read()
                return jsonify({"result": "Reddit story fetched successfully.", "story": reddit_story})
            else:
                return jsonify({"result": "Error: No story fetched from Reddit."})

        except subprocess.CalledProcessError:
            return jsonify({"result": "Make sure you entered the correct subreddit name (excluding r/) : 'subreddit_name' "})

    return jsonify({"result": "Error: No subreddit provided."})

if __name__ == '__main__':
    app.run(debug=True)
