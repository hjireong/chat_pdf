import streamlit as st
import openai
import PyPDF2

# OpenAI API 키 설정
openai.api_key = "your_openai_api_key"

# 텍스트 추출 함수
def extract_text_from_pdf(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

st.title("ChatPDF 챗봇")

uploaded_file = st.file_uploader("PDF 파일을 업로드하세요", type="pdf")
if uploaded_file:
    pdf_text = extract_text_from_pdf(uploaded_file)
    st.write("PDF 내용:")
    st.write(pdf_text)

    user_input = st.text_input("질문을 입력하세요:")
    if st.button("질문 보내기"):
        # OpenAI ChatCompletion API 호출
        messages = [
            {"role": "system", "content": "PDF 내용을 기반으로 질문에 답변하세요."},
            {"role": "assistant", "content": pdf_text},
            {"role": "user", "content": user_input}
        ]

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=messages
            )
            reply = response["choices"][0]["message"]["content"]
            st.write(f"챗봇: {reply}")
        except Exception as e:
            st.error(f"오류 발생: {str(e)}")
