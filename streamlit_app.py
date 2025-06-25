import streamlit as st
import subprocess
import os
import zipfile
from pathlib import Path

st.set_page_config(page_title="RKIT Converter", layout="centered")
st.title("📄 RKIT Document Converter")

uploaded_file = st.file_uploader("Upload a Word (.docx) file", type="docx")
format = st.selectbox("Choose output format", ["gfm", "html", "pdf", "txt", "latex"])

if uploaded_file:
    filename = uploaded_file.name
    with open(filename, "wb") as f:
        f.write(uploaded_file.read())

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{Path(filename).stem}.{format}")
    media_path = os.path.join(output_dir, "media")

    try:
        subprocess.run([
            "pandoc", filename,
            "-t", format,
            "--extract-media", media_path,
            "-o", output_path
        ], check=True)

        zip_name = f"{Path(filename).stem}_converted.zip"
        zip_path = os.path.join(output_dir, zip_name)

        with zipfile.ZipFile(zip_path, "w") as zipf:
            zipf.write(output_path, arcname=os.path.basename(output_path))
            for root, dirs, files in os.walk(media_path):
                for file in files:
                    full_path = os.path.join(root, file)
                    arcname = os.path.relpath(full_path, output_dir)
                    zipf.write(full_path, arcname=arcname)

        with open(zip_path, "rb") as f:
            st.success("✅ Conversion complete!")
            st.download_button("Download ZIP", f, file_name=zip_name)

    except subprocess.CalledProcessError:
        st.error("❌ Pandoc conversion failed.")
