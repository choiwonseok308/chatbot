import streamlit as st
from openai import OpenAI

# 제목과 설명을 표시합니다.
st.title("💬 AI 챗봇")
st.write(
    "안녕하세요! 😊 이 챗봇은 OpenAI의 GPT-3.5 모델을 활용한 대화형 AI예요. "
    "사용하시려면 OpenAI API 키가 필요한데요, [여기](https://platform.openai.com/account/api-keys)에서 발급받으실 수 있어요. "
    "챗봇을 직접 만들어보고 싶으신 분은 [튜토리얼](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)을 참고해보세요!"
)

# 사용자에게 OpenAI API 키를 입력받습니다.
# 또는 `./.streamlit/secrets.toml` 파일에 API 키를 저장하고
# `st.secrets`로 불러올 수도 있어요. 자세한 내용은 https://docs.streamlit.io/develop/concepts/connections/secrets-management 를 참고하세요.
openai_api_key = st.text_input("🔑 OpenAI API 키를 입력해주세요", type="password")

if not openai_api_key:
    st.info("API 키를 입력하시면 챗봇을 사용하실 수 있어요!", icon="🗝️")
else:
    # OpenAI 클라이언트를 생성합니다.
    client = OpenAI(api_key=openai_api_key)

    # 채팅 메시지를 저장할 세션 상태 변수를 만듭니다.
    # 이렇게 하면 페이지가 새로고침되어도 대화 내용이 유지돼요.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 기존 채팅 메시지들을 화면에 표시합니다.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자가 메시지를 입력할 수 있는 채팅 입력창입니다.
    # 화면 하단에 자동으로 표시돼요.
    if prompt := st.chat_input("무엇이든 물어보세요! 😊"):
        # 입력된 메시지를 저장하고 화면에 표시합니다.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # OpenAI API를 사용하여 응답을 생성합니다.
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # 응답을 스트리밍 방식으로 채팅창에 출력하고, 세션 상태에 저장합니다.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})