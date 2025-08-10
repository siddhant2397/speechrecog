import streamlit as st
import azure.cognitiveservices.speech as speechsdk
import tempfile

st.title("Azure Speech-to-Text Demo")

# Access Azure secrets from Streamlit's secrets management
speech_key = st.secrets["speechkey"]
service_region = st.secrets["serviceregion"]

# Record audio from browser using the built-in Streamlit widget
audio_file = st.audio_input("Record your message (max 60s)", type="wav")
if audio_file is not None:
    st.audio(audio_file, format="audio/wav")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_wav:
        tmp_wav.write(audio_file.read())
        tmp_wav_path = tmp_wav.name

    st.write("Transcribing with Azure Speech-to-Text...")

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    audio_config = speechsdk.AudioConfig(filename=tmp_wav_path)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    result = speech_recognizer.recognize_once_async().get()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        st.success(f"Recognized Text:\n{result.text}")
    elif result.reason == speechsdk.ResultReason.NoMatch:
        st.warning("No speech could be recognized.")
    elif result.reason == speechsdk.ResultReason.Canceled:
        st.error(f"Speech Recognition canceled: {result.cancellation_details.reason}")
else:
    st.info("Click above to record your speech.")

