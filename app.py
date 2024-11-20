import streamlit as st
import openai
import PyPDF2

# OpenAI API 키 설정
openai.api_key = "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"

# 벡터 저장소 초기화
vector_store = None

# 텍스트 추출 함수
def extract_text_from_pdf(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Streamlit UI 설정
st.title("ChatPDF 챗봇")

# PDF 파일 업로드
uploaded_file = st.file_uploader("PDF 파일을 업로드하세요", type="pdf")
if uploaded_file:
    with st.spinner("PDF 내용을 읽는 중..."):
        pdf_text = extract_text_from_pdf(uploaded_file)
        st.success("PDF 내용을 성공적으로 읽었습니다.")
else:
    pdf_text = ""

# Clear 버튼: 벡터 스토어 초기화
if st.button("Clear"):
    vector_store = None
    st.info("벡터 스토어가 초기화되었습니다.")

# OpenAI 파일 검색과 대화
if uploaded_file and pdf_text:
    user_input = st.text_input("질문을 입력하세요:")
    if st.button("질문 보내기"):
        # OpenAI ChatCompletion 호출
        messages = [
            {"role": "system", "content": "PDF 내용을 기반으로 질문에 답변하세요."},
            {"role": "user", "content": user_input},
            {"role": "assistant", "content": pdf_text}
        ]

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages
        )
        reply = response['choices'][0]['message']['content']
        st.write(f"챗봇: {reply}")
