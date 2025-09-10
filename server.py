"""
This module is a Flask web application that serves an emotion detection tool.
It exposes an endpoint to analyze text and returns the dominant emotion.
"""
from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

# Initialize the Flask application
app = Flask("EmotionDetector")

@app.route("/")
def render_index_page():
    """This function renders the index.html page."""
    return render_template('index.html')

@app.route("/emotionDetector")
def emotion_detector_route():
    """
    This function receives text from the request, runs emotion detection,
    and returns a formatted string as a response.
    """
    text_to_analyze = request.args.get('textToAnalyze')

    response = emotion_detector(text_to_analyze)

    if response['dominant_emotion'] is None:
        return "Invalid text! Please try again with a valid input."

    formatted_output = (
        f"For the given statement, the system response is "
        f"'anger': {response['anger']}, 'disgust': {response['disgust']}, "
        f"'fear': {response['fear']}, 'joy': {response['joy']} and "
        f"'sadness': {response['sadness']}. The dominant emotion is "
        f"{response['dominant_emotion']}."
    )

    return formatted_output

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)