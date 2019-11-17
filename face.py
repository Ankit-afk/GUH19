#header

import requests
import json


def Mood():

    print("Detecting mood...")
    def getHighestEmotion(emotion_dict):
        highest_emotion = "neutral"
        highest_number = 0
        for emotion in emotion_dict.items():
            if emotion[1] > highest_number:
                highest_emotion = emotion[0]
        return highest_emotion


    emotions_Counter = {
        "happiness": 0, #and neutral, surprise
        "neutral": 0,
        "surprise": 0,
        "sadness": 0,
        "anger": 0,
        "fear": 0,
        "disgust": 0,
        "contempt": 0,} #disgust, contempt


    headers = {'Content-Type': 'application/octet-stream', 
                        'Ocp-Apim-Subscription-Key':"d48577bd2d8b47faa522334da1680d65"}


    params = {
        'returnFaceId': 'false',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'emotion'
    }

    headers = {'Content-Type': 'application/octet-stream', 
                        'Ocp-Apim-Subscription-Key': "d48577bd2d8b47faa522334da1680d65"}
    face_api_url = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect'

    for image in range(10):
        data = open(f"images/outfile{image}.jpg", 'rb')
        response  = requests.post(face_api_url , headers=headers, params=params, data=data)
        response_dict = response.json()

        print(f"Amount of people in image {image}: {len(response_dict)}")
        for item in response_dict:
            emotion = getHighestEmotion(item["faceAttributes"]["emotion"])
            emotions_Counter[emotion] +=1
            
    data.close()

    

    highest_emotion = "neutral"
    highest_number = 0
    for key, value in emotions_Counter.items():
        if (value > highest_number):
            highest_emotion = key

    if (highest_emotion == "neutral" or highest_emotion == "surprise"):
        real_emotion = "happiness"
    elif (highest_emotion == "disgust" or highest_emotion == "contempt"):
        real_emotion = "fear"
    else: 
        real_emotion = highest_emotion

    print("Images analyzed.")
    return [highest_emotion, real_emotion]


