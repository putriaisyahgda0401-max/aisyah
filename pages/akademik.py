import json

import streamlit as st

st.title("Informasi Akademik")
st.write("Berikut daftar mata pelajaran dan topik yang dipelajari.")

with open("database_chatbot.json", "r") as f:
    db = json.load(f)

akademik = db.get("silabus", {}).get("akademik", [])

if not akademik:
    st.info("Data akademik belum tersedia.")
else:
    for pelajaran in akademik:
        nama = pelajaran.get("mata_kuliah", "Mata pelajaran")
        semester = pelajaran.get("semester", "-")
        daftar_topik = pelajaran.get("topik", [])

        st.subheader(f"{nama} - Semester {semester}")
        for topik in daftar_topik:
            st.write(f"- {topik}")
