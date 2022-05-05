import os
from google.cloud import speech

#set up api permission for speech to text
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'ttaylor-med-api-3285443a6f89.json'
speechClient = speech.SpeechClient()

#converts speech to text
def speechToText(audioSource):

    #Cloud Hosted Files
    if audioSource.startswith(b'gs:'):
        #e.g. cloudURL = 'gs://ttaylor-speech-to-text/testSpeech2.wav'
        rawAudio = speech.RecognitionAudio(uri = audioSource)
    
    #Local Files
    else:
        #Open file
        with open(audioSource, 'rb') as file:
            audioData = file.read()
        #Transcribe audio
        rawAudio = speech.RecognitionAudio(content = audioData)


    #Configue media output
    configRec = speech.RecognitionConfig(sample_rate_hertz = 48000, enable_automatic_punctuation = True, language_code = 'en-US', audio_channel_count = 2)

    #Transcribe recAudio object
    sTOtData = speechClient.recognize(config = configRec, audio = rawAudio)

    print(sTOtData)

#testing
#if __name__ == '__main__':
    #speechToText('gs://ttaylor-speech-to-text/testSpeech2.wav')
    #speechToText('testSpeech1.wav')
