import requests
import json

def emotion_detector(text_to_analyze):
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    json_data = { "raw_document": { "text": text_to_analyze } }

    try:
        response = requests.post(url, json=json_data, headers=headers)

        # Check for a 400 status code for blank input
        if response.status_code == 400:
            return {
                'anger': None,
                'disgust': None,
                'fear': None,
                'joy': None,
                'sadness': None,
                'dominant_emotion': None
            }

        response.raise_for_status() # This will raise an HTTPError for other bad responses

        # Convert the response text to a Python dictionary
        json_response = json.loads(response.text)

        # Extract the emotion scores
        emotion_scores = json_response['emotionPredictions'][0]['emotion']

        # Extract individual scores
        anger_score = emotion_scores['anger']
        disgust_score = emotion_scores['disgust']
        fear_score = emotion_scores['fear']
        joy_score = emotion_scores['joy']
        sadness_score = emotion_scores['sadness']

        # Find the dominant emotion
        emotions = {
            'anger': anger_score,
            'disgust': disgust_score,
            'fear': fear_score,
            'joy': joy_score,
            'sadness': sadness_score
        }
        dominant_emotion = max(emotions, key=emotions.get)

        # Return the formatted dictionary
        return {
            'anger': anger_score,
            'disgust': disgust_score,
            'fear': fear_score,
            'joy': joy_score,
            'sadness': sadness_score,
            'dominant_emotion': dominant_emotion
        }

    except requests.exceptions.RequestException as e:
        print(f"Error during API call: {e}")
        return None
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error processing API response: {e}")
        print(f"Response text: {response.text}")
        return None