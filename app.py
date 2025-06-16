import streamlit as st
from streamlit_paste_button import paste_image_button
from PIL import Image
import io
import psycopg2
from datetime import datetime

# PostgreSQL 연결 함수
def get_conn():
    return psycopg2.connect(
        host="10.166.253.42",
        database="imageuploadtest",
        user="postgres",
        password="rca",
        port=5432
    )

def save_image(img_bytes):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO images (image_data) VALUES (%s)", (psycopg2.Binary(img_bytes),))
        conn.commit()

def load_last_image():
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT image_data FROM images ORDER BY uploaded_at DESC LIMIT 1")
        row = cur.fetchone()
        return row[0] if row else None

st.title("클립보드 이미지 저장 & 보기")

paste_result = paste_image_button("📋 이미지 붙여넣기")
if paste_result is not None and paste_result.image_data is not None:
    pil_img = paste_result.image_data
    buf = io.BytesIO()
    pil_img.save(buf, format="PNG")
    img_bytes = buf.getvalue()

    st.image(img_bytes, caption="미리보기", use_container_width=True)
    if st.button("💾 저장"):
        save_image(img_bytes)
        st.success("저장 완료 ✅")

if st.button("🖼 저장된 최신 이미지 보기"):
    last = load_last_image()
    if last:
        # memoryview → bytes → BytesIO
        image_data = io.BytesIO(bytes(last))
        st.image(image_data, caption="DB에서 불러온 이미지", use_container_width=True)
    else:
        st.warning("저장된 이미지가 없습니다.")
