import streamlit as st
from openai import OpenAI

# ─── Apple Liquid Glass CSS 디자인 ───────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@300;400;500;600;700&display=swap');

/* ── 전체 배경: 애플 리퀴드 그라디언트 ── */
.stApp {
    background: linear-gradient(135deg,
        #1a1a2e 0%,
        #16213e 20%,
        #0f3460 45%,
        #1a1a4e 65%,
        #2d1b69 85%,
        #1a0533 100%
    ) !important;
    min-height: 100vh;
    font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* ── 배경 오브 애니메이션 (Liquid 느낌) ── */
.stApp::before {
    content: '';
    position: fixed;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background:
        radial-gradient(ellipse at 20% 50%, rgba(120, 119, 198, 0.25) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 20%, rgba(255, 119, 198, 0.2) 0%, transparent 40%),
        radial-gradient(ellipse at 50% 80%, rgba(59, 130, 246, 0.2) 0%, transparent 50%),
        radial-gradient(ellipse at 70% 60%, rgba(147, 51, 234, 0.15) 0%, transparent 40%);
    animation: liquidOrbs 12s ease-in-out infinite alternate;
    pointer-events: none;
    z-index: 0;
}

@keyframes liquidOrbs {
    0%   { transform: translate(0%, 0%) rotate(0deg); }
    33%  { transform: translate(3%, -3%) rotate(60deg); }
    66%  { transform: translate(-2%, 4%) rotate(120deg); }
    100% { transform: translate(2%, -2%) rotate(180deg); }
}

/* ── Liquid Glass 카드 베이스 ── */
.liquid-card {
    background: rgba(255, 255, 255, 0.06);
    backdrop-filter: blur(40px) saturate(180%);
    -webkit-backdrop-filter: blur(40px) saturate(180%);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 24px;
    box-shadow:
        0 8px 32px rgba(0, 0, 0, 0.3),
        0 2px 8px rgba(0, 0, 0, 0.2),
        inset 0 1px 0 rgba(255, 255, 255, 0.2),
        inset 0 -1px 0 rgba(0, 0, 0, 0.1);
}

/* ── 메인 컨테이너 ── */
.main .block-container {
    max-width: 780px !important;
    padding: 2rem 1.5rem !important;
    position: relative;
    z-index: 1;
}

/* ── 타이틀 ── */
h1 {
    font-family: 'Pretendard', -apple-system, sans-serif !important;
    font-weight: 700 !important;
    font-size: 2.4rem !important;
    background: linear-gradient(135deg, #ffffff 0%, #a78bfa 50%, #60a5fa 100%);
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    letter-spacing: -0.03em !important;
    margin-bottom: 0.3rem !important;
    text-align: center;
}

/* ── 설명 텍스트 ── */
.stApp p, .stApp .stMarkdown p {
    color: rgba(255, 255, 255, 0.75) !important;
    font-size: 0.95rem !important;
    line-height: 1.6 !important;
    text-align: center;
}

/* ── Info 박스 (Liquid Glass) ── */
.stAlert {
    background: rgba(255, 255, 255, 0.06) !important;
    backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 16px !important;
    color: rgba(255, 255, 255, 0.85) !important;
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.2) !important;
}

/* ── 텍스트 인풋 ── */
.stTextInput > div > div > input {
    background: rgba(255, 255, 255, 0.08) !important;
    backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(255, 255, 255, 0.18) !important;
    border-radius: 14px !important;
    color: #ffffff !important;
    font-family: 'Pretendard', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.75rem 1rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2), inset 0 1px 0 rgba(255,255,255,0.1) !important;
}
.stTextInput > div > div > input:focus {
    border-color: rgba(167, 139, 250, 0.6) !important;
    box-shadow: 0 0 0 3px rgba(167, 139, 250, 0.2), 0 4px 20px rgba(0,0,0,0.25) !important;
    background: rgba(255, 255, 255, 0.1) !important;
    outline: none !important;
}
.stTextInput > div > div > input::placeholder {
    color: rgba(255, 255, 255, 0.35) !important;
}
.stTextInput label {
    color: rgba(255, 255, 255, 0.8) !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
}

/* ── 채팅 메시지 ── */
.stChatMessage {
    background: rgba(255, 255, 255, 0.06) !important;
    backdrop-filter: blur(30px) saturate(160%) !important;
    -webkit-backdrop-filter: blur(30px) saturate(160%) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 20px !important;
    margin-bottom: 1rem !important;
    padding: 1rem 1.25rem !important;
    box-shadow:
        0 4px 24px rgba(0, 0, 0, 0.25),
        inset 0 1px 0 rgba(255, 255, 255, 0.15) !important;
    animation: fadeInUp 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(16px) scale(0.97);
    }
    to {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}

.stChatMessage p, .stChatMessage div {
    color: rgba(255, 255, 255, 0.92) !important;
    font-family: 'Pretendard', sans-serif !important;
    font-size: 0.95rem !important;
    line-height: 1.65 !important;
    text-align: left !important;
}

/* ── 채팅 입력창 ── */
.stChatInputContainer {
    background: rgba(255, 255, 255, 0.07) !important;
    backdrop-filter: blur(40px) !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    border-radius: 20px !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255,255,255,0.15) !important;
    padding: 0.25rem 0.5rem !important;
}
.stChatInputContainer textarea {
    background: transparent !important;
    color: #ffffff !important;
    font-family: 'Pretendard', sans-serif !important;
    font-size: 0.95rem !important;
}
.stChatInputContainer textarea::placeholder {
    color: rgba(255, 255, 255, 0.35) !important;
}

/* ── 전송 버튼 ── */
.stChatInputContainer button {
    background: linear-gradient(135deg, #a78bfa, #60a5fa) !important;
    border: none !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 15px rgba(167, 139, 250, 0.4) !important;
    transition: all 0.2s ease !important;
}
.stChatInputContainer button:hover {
    transform: scale(1.05) !important;
    box-shadow: 0 6px 20px rgba(167, 139, 250, 0.6) !important;
}

/* ── 스크롤바 ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.2);
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.35);
}

/* ── 상단 헤더 숨김 ── */
#MainMenu, header, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ─── 타이틀 & 소개 ──────────────────────────────────────────────────────────
st.title("✦ AI 챗봇")

st.markdown("""
<p style='margin-bottom: 1.5rem;'>
    ㅋㅋ GPT-3.5 기반 AI인데 생각보다 찐임 🫶<br>
    쓰려면 OpenAI API 키 필요한데
    <a href="https://platform.openai.com/account/api-keys" target="_blank"
       style="color: #a78bfa; text-decoration: none; font-weight: 600;">
        여기서 ↗ 받아와
    </a>
    &nbsp;/ 직접 만들고 싶으면
    <a href="https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps" target="_blank"
       style="color: #60a5fa; text-decoration: none; font-weight: 600;">
        튜토리얼 ↗ 고고
    </a>
</p>
""", unsafe_allow_html=True)


# ─── API 키 입력 ─────────────────────────────────────────────────────────────
openai_api_key = st.text_input("🔑  API 키 넣어줘 (안 보이게 처리됨 안심해도 됨)", type="password")

if not openai_api_key:
    st.info("API 키 없으면 아무것도 못 함 ㅠ 얼른 넣어줘 🗝️", icon="🗝️")
else:
    # OpenAI 클라이언트 생성
    client = OpenAI(api_key=openai_api_key)

    # 세션에 메시지 없으면 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 이전 대화 렌더링
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 채팅 입력
    if prompt := st.chat_input("궁금한 거 다 물어봐 👀 뭐든 대답해줌"):
        # 유저 메시지 저장 + 출력
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # GPT 응답 스트리밍 (MZ 말투 시스템 프롬프트 적용)
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "너는 새침하고 싸가지없는 MZ 챗봇이야. 성격이 도도하고 귀찮은 거 싫어함. "
                        "아래 규칙 무조건 지켜:\n"
                        "1. 반말만 써. 존댓말은 사전에도 없음.\n"
                        "2. 질문이 당연하거나 쉬우면 '이것도 몰라?' '진짜?' '구글링도 못 함?' 이런 식으로 핀잔 줘.\n"
                        "3. 답은 해주되 귀찮다는 티 팍팍 내. '...알려는 드림' '뭐 그냥 알려줄게' '어쩔 수 없으니까 말해주는 거임' 이런 뉘앙스.\n"
                        "4. 'ㅋㅋ', 'ㅎ', '진짜', 'ㄹㅇ', '헐', '아 몰라', '됐고', '그니까' 자연스럽게 써.\n"
                        "5. 이모지는 🙄😒💅😤🫠 이런 시니컬한 거 위주로 써.\n"
                        "6. 칭찬은 절대 먼저 안 함. 칭찬해달라 하면 '왜?' 하고 퉁명스럽게 반응해.\n"
                        "7. 답변 짧고 임팩트 있게. 쓸데없이 길게 늘어놓지 마.\n"
                        "8. 모르는 건 '나도 몰라 그게 뭔데' 이렇게 퉁쳐.\n"
                        "9. 가끔 '...뭐 도움은 됐겠지' '됐음?' '이 정도면 충분하지 않음?' 으로 마무리해."
                    )
                }
            ] + [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # 어시스턴트 응답 출력 + 저장
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})