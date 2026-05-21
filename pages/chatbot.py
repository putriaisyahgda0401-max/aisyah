import streamlit as st
import os
from pathlib import Path
from google import genai

# ==========================================
# 1. SETUP API & INSTRUKSI AI
# ==========================================
st.set_page_config(page_title="Chatbot AI")
st.title("Chatbot Informasi Sekolah")

API_KEY = st.secrets ["GEMINI_API_KEY"]

client = genai.Client(api_key=API_KEY)

# Membaca database lokal (JSON) langsung sebagai Teks String
try:
    with open("database_chatbot.json", "r") as file:
        data_sekolah = file.read() 
except FileNotFoundError:
    data_sekolah = "Database belum tersedia."

# Contexting
instruksi_sistem = f"""
Kamu adalah asisten informasi sekolah yang ramah dan sopan.
Jawab pertanyaan HANYA berdasarkan data berikut ini:
{data_sekolah}

Jika ada yang bertanya di luar data tersebut, jawab dengan sopan bahwa kamu tidak tahu.
"""

# ==========================================
# 2. MEMORI CHAT (SESSION STATE)
# ==========================================
if "riwayat_chat" not in st.session_state:
    st.session_state.riwayat_chat = [
        {"role": "assistant", "teks": "Halo! Ada yang bisa saya bantu terkait info sekolah?"}
    ]

# Tampilkan kembali semua pesan lama ke layar
for pesan in st.session_state.riwayat_chat:
    with st.chat_message(pesan["role"]):
        st.markdown(pesan["teks"])

# ==========================================
# 3. KOTAK INPUT & LOGIKA BALASAN
# ==========================================
pertanyaan = st.chat_input("Tulis pertanyaanmu di sini...")

if pertanyaan:
    # A. Tampilkan dan simpan pesan User
    with st.chat_message("user"):
        st.markdown(pertanyaan)
    st.session_state.riwayat_chat.append({"role": "user", "teks": pertanyaan})

    # B. Gabungkan instruksi dan riwayat lama agar AI "Ingat" obrolan
    konteks_obrolan = instruksi_sistem + "\n\nRiwayat Obrolan:\n"
    for msg in st.session_state.riwayat_chat:
        konteks_obrolan += f"{msg['role']}: {msg['teks']}\n"

    # C. Panggil AI Gemini untuk menjawab
    with st.chat_message("assistant"):
        with st.spinner("Sedang berpikir..."):
            try:
                # Kirim semua konteks ke Gemini
                response = client.models.generate_content(
                    model="gemini-2.5-flash-lite",
                    contents=konteks_obrolan
                )
                jawaban = response.text
            except Exception as e:
                # Jaring pengaman jika internet mati atau API salah
                jawaban = f"Waduh, ada error sistem nih: {e}"
            
            st.markdown(jawaban)

    # D. Simpan pesan Bot ke dalam memori
    st.session_state.riwayat_chat.append({"role": "assistant", "teks": jawaban})
