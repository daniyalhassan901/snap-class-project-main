import io
import numpy as np 
import streamlit as st

# --- SAFE IMPORTS ---
try:
    from resemblyzer import VoiceEncoder, preprocess_wav
    import librosa
    import torch
    VOICE_AVAILABLE = True
except Exception as e:
    print(f"Voice libs not available: {e}")
    VOICE_AVAILABLE = False
    VoiceEncoder = None
    preprocess_wav = None
    librosa = None
    torch = None

@st.cache_resource
def load_voice_encoder():
    if not VOICE_AVAILABLE:
        return None
    return VoiceEncoder()

def get_voice_embedding(audio_bytes):
    if not VOICE_AVAILABLE:
        return None
    try:
        encoder = load_voice_encoder()
        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)
        wav = preprocess_wav(audio)
        embedding = encoder.embed_utterance(wav)
        return embedding.tolist()
    except Exception as e:
        st.error(f'Voice recog error: {e}')
        return None

def process_bulk_audio(audio_bytes, candidates_dict, threshold=0.65):
    if not VOICE_AVAILABLE:
        return {}
    try:
        encoder = load_voice_encoder()
        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)
        segments = librosa.effects.split(audio, top_db=30)
        identified_results = {}
        for start, end in segments:
            if (end-start) < sr * 0.5:
                continue
            segment_audio = audio[start:end]
            wav = preprocess_wav(segment_audio)
            embedding = encoder.embed_utterance(wav)
            # simple dot product similarity
            for sid, stored_embedding in candidates_dict.items():
                if stored_embedding:
                    similarity = np.dot(embedding, stored_embedding)
                    if similarity >= threshold:
                        identified_results[sid] = similarity
        return identified_results
    except Exception as e:
        st.error(f'Bulk process error: {e}')
        return {}