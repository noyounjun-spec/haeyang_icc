import streamlit as st
import os
import json
import time

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="해양경찰청 미션: SEA CRET 아치 요원!",
    page_icon="🕵️‍♂️",
    layout="centered"
)

DB_FILE = "mission_db.json"

# ---------------------------------------------------------
# 데이터베이스 함수 (동시 접속 충돌 방지)
# ---------------------------------------------------------
def load_db():
    for _ in range(5):
        try:
            if os.path.exists(DB_FILE):
                with open(DB_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            return {}
        except Exception:
            time.sleep(0.1)
    return {}

def save_db(db_to_save):
    for _ in range(5):
        try:
            current_db = {}
            if os.path.exists(DB_FILE):
                with open(DB_FILE, "r", encoding="utf-8") as f:
                    current_db = json.load(f)
            
            for k, v in db_to_save.items():
                current_db[k] = v
                
            with open(DB_FILE, "w", encoding="utf-8") as f:
                json.dump(current_db, f, ensure_ascii=False, indent=4)
            break
        except Exception:
            time.sleep(0.1)

# 커스텀 스타일링
st.markdown("""
    <style>
    .block-container { padding-top: 2rem; max-width: 450px; }
    .stButton>button { width: 100%; border-radius: 20px; }
    .level-badge {
        background-color: #005ea2;
        color: white;
        padding: 8px 24px;
        border-radius: 50px;
        font-weight: 800;
        font-size: 1.6rem;
        display: inline-block;
        box-shadow: 0 4px 10px rgba(0, 94, 162, 0.3);
        margin-bottom: 10px;
    }
    .seacret-badge {
        background-color: #ffd700;
        color: #111111;
        padding: 10px 30px;
        border-radius: 50px;
        font-weight: 900;
        font-size: 1.8rem;
        display: inline-block;
        box-shadow: 0 4px 20px rgba(255, 215, 0, 0.6);
    }
    .character-box {
        border-radius: 20px;
        padding: 15px;
        text-align: center;
        margin-bottom: 15px;
    }
    .seacret-text {
        font-size: 1.7rem;
        font-weight: bold;
        color: #ffd700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

db = load_db()

main_hqs = ['central_hq', 'east_hq', 'west_hq', 'south_hq']
hq_info = {
    'central_hq': {'name': '중부지방청', 'file': '중부 아치.png'},
    'east_hq': {'name': '동해지방청', 'file': '동해 아치.png'},
    'west_hq': {'name': '서해지방청', 'file': '서해 아치.png'},
    'south_hq': {'name': '남해지방청', 'file': '남해 아치.png'}
}

if "scan" in st.query_params:
    st.session_state.pending_scan = st.query_params["scan"]
    st.query_params.clear()

# ---------------------------------------------------------
# 🔒 비밀번호가 추가된 로그인 화면
# ---------------------------------------------------------
if "username" not in st.session_state:
    st.title("🕵️‍♂️ 해양경찰청 요원 인증")
    st.write("보안을 위해 요원명과 비밀번호를 입력해주세요.")
    
    with st.form("login_form"):
        username_input = st.text_input("요원명 (예: 아치대장)")
        password_input = st.text_input("비밀번호 (숫자나 영문)", type="password") # 비밀번호 가림 처리
        submitted = st.form_submit_button("인증하고 접속하기")
        
        if submitted:
            if username_input.strip() == "" or password_input.strip() == "":
                st.error("요원명과 비밀번호를 모두 입력해주세요!")
            else:
                user = username_input.strip()
                pw = password_input.strip()
                
                # 1. 아예 처음 접속하는 신규 요원인 경우 (가입)
                if user not in db:
                    db[user] = {"password": pw, "visited": [], "is_secret_agent": False}
                    save_db(db)
                    st.success(f"환영합니다! '{user}' 요원님의 계정이 생성되었습니다.")
                    time.sleep(1) # 성공 메시지를 1초 보여주고 넘어감
                    st.session_state.username = user
                    st.rerun()
                    
                # 2. 이미 등록된 기존 요원인 경우 (로그인)
                else:
                    # (예외 처리) 예전에 비밀번호 없이 만든 계정이라면, 지금 입력한 비번으로 설정해줌
                    if "password" not in db[user]:
                        db[user]["password"] = pw
                        save_db(db)
                        
                    # 비밀번호 일치 확인
                    if db[user]["password"] == pw:
                        st.session_state.username = user
                        st.rerun()
                    else:
                        st.error("🚫 비밀번호가 틀렸습니다! 다시 확인해주세요.")
    st.stop()

# 로그인 성공 후 화면
user = st.session_state.username
user_data = db[user]

st.title("💙 SEA CRET 아치 컬렉션")
st.caption(f"[{user} 요원] 님 환영합니다! 아치 대원들을 모으세요.")

if "pending_scan" in st.session_state:
    scanned_hq = st.session_state.pending_scan
    if scanned_hq in main_hqs:
        if scanned_hq not in user_data["visited"]:
            user_data["visited"].append(scanned_hq)
            save_db(db)
            st.toast(f"🎉 [{hq_info[scanned_hq]['name']}] 아치 대원이 합류했습니다!", icon="💖")
    elif scanned_hq == 'jeju_hq':
        if set(main_hqs).issubset(set(user_data["visited"])):
            if not user_data["is_secret_agent"]:
                user_data["is_secret_agent"] = True
                save_db(db)
                st.toast("🕵️‍♂️ 당신은 SEA CRET 이 되었습니다!", icon="🏆")
        else:
            st.error("🚫 아직 4대 지방청 아치를 모두 모으지 못했습니다!")
    del st.session_state.pending_scan

level = len(user_data["visited"])

st.markdown("<div class='character-box'>", unsafe_allow_html=True)
if user_data["is_secret_agent"]:
    st.markdown("<div class='seacret-badge'>LV. SEA CRET</div>", unsafe_allow_html=True)
    st.markdown("<div class='seacret-text'>🎉 당신은 SEA CRET 이 되었습니다! 🎉</div>", unsafe_allow_html=True)
else:
    st.markdown(f"<div class='level-badge'>LV. {level}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

st.subheader("👥 나의 아치 부대원 현황")
st.write("**[기본 대원]**")
if os.path.exists("아치.png"):
    st.image("아치.png", width=140)

if user_data["visited"] or user_data["is_secret_agent"]:
    st.write("**[합류한 지방청 아치들]**")
    cols = st.columns(2)
    idx = 0
    for hq in main_hqs:
        if hq in user_data["visited"]:
            with cols[idx % 2]:
                filename = hq_info[hq]['file']
                st.markdown(f"📍 **{hq_info[hq]['name']} 아치**")
                if os.path.exists(filename):
                    st.image(filename, width=140)
            idx += 1
    if user_data["is_secret_agent"]:
        with cols[idx % 2]:
            st.markdown("👑 **최종 제주 아치**")
            if os.path.exists("제주아치.png"):
                st.image("제주아치.png", width=140)
else:
    st.caption("아직 합류한 지방청 대원이 없습니다. 아래 QR을 스캔하세요!")

st.divider()
st.write(f"**지방청 아치 수집도:** {level} / 4")
st.progress(level / 4)

# 배포된 진짜 인터넷 주소
base_url = "https://haeyangicc-naae9czhnhbfv4f2hwb2yt.streamlit.app"

st.divider()
st.subheader("🏠 메인 화면 접속 QR (친구 초대용)")
st.write("누구든 이 QR 코드를 스캔하면 '요원명 입력 화면'으로 들어옵니다.")
main_qr_api = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={base_url}"
st.image(main_qr_api, width=200)

st.divider()
st.subheader("[테스트용] 탐방 시뮬레이터")
st.write(f"📢 **현재 연결된 공식 서버 주소:** `{base_url}`")
st.write("### 1단계: 4대 지방청 아치 모으기")
cols_sim = st.columns(2)
for i, hq in enumerate(main_hqs):
    with cols_sim[i % 2]:
        is_done = hq in user_data["visited"]
        st.markdown(f"**{hq_info[hq]['name']} {'✅' if is_done else '⭕'}**")
        qr_url = f"{base_url}/?scan={hq}"
        qr_api = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={qr_url}"
        st.image(qr_api, width=120)

st.write("### 2단계: SEA CRET 요원 최종 인증")
is_jeju_ready = (level == 4)
if user_data["is_secret_agent"]:
    st.success("🕵️‍♂️ 미션 컴플리트!")
else:
    st.markdown(f"**제주지방청 최종장 {'🔓 스캔 가능' if is_jeju_ready else '🔒 잠김 (앞의 4곳 수집 필요)'}**")
    jeju_qr_url = f"{base_url}/?scan=jeju_hq"
    jeju_qr_api = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={jeju_qr_url}"
    st.image(jeju_qr_api, width=120)

st.divider()
cols_footer = st.columns(2)
with cols_footer[0]:
    if st.button("🚪 다른 요원으로 로그인 (로그아웃)"):
        del st.session_state.username
        st.rerun()
with cols_footer[1]:
    if st.button("🗑️ 내 기록 전체 삭제"):
        db[user] = {"visited": [], "is_secret_agent": False}
        save_db(db)
        st.rerun()
