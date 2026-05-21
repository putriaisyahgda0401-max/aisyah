import json

import streamlit as st

st.title("Fasilitas Sekolah")
st.write("Halaman ini menampilkan fasilitas yang bisa digunakan siswa.")

with open("database_chatbot.json", "r", encoding="utf-8") as f:
    db = json.load(f)

fasilitas = db.get("silabus", {}).get("fasilitas", [])

if not fasilitas:
    st.info("Data fasilitas belum tersedia.")
else:
    for fasilitas_item in fasilitas:
        nama = fasilitas_item.get("nama", "Fasilitas")
        jam = fasilitas_item.get("jam_operasional", "-")
        lokasi = fasilitas_item.get("lokasi", "-")

        st.subheader(nama)
        st.write(f"Jam operasional: {jam}")
        st.write(f"Lokasi: {lokasi}")