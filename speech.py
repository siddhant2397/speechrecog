import streamlit as st
from audio_recorder_streamlit import audio_recorder
import azure.cognitiveservices.speech as speechsdk
import tempfile

st.title("Speech to Text for Keeping Meeting Minutes")

# Access Azure secrets from Streamlit's secrets management
speech_key = st.secrets["speech_key"]
service_region = st.secrets["service_region"]

# Record audio from the browser using audio-recorder-streamlit component
audio_bytes = audio_recorder(pause_threshold=10.0, auto_start=False)

if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_wav:
        tmp_wav.write(audio_bytes)
        tmp_wav_path = tmp_wav.name

    st.write("Transcribing with Speech-to-Text...")

    # Configure Azure Speech SDK
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    audio_config = speechsdk.AudioConfig(filename=tmp_wav_path)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    # Perform recognition
    result = speech_recognizer.recognize_once_async().get()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        st.success(f"Recognized Text:\n{result.text}")
    elif result.reason == speechsdk.ResultReason.NoMatch:
        st.warning("No speech could be recognized.")
    elif result.reason == speechsdk.ResultReason.Canceled:
        st.error(f"Speech Recognition canceled: {result.cancellation_details.reason}")
else:
    st.info("Click the record button above and speak.")

