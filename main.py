import streamlit as st
from datetime import date

# 기본 테마 목록
default_themes = {
    "라이트": {
        "bg_color": "#ffffff",
        "text_color": "#000000",
        "accent": "#4CAF50"
    },
    "다크": {
        "bg_color": "#1e1e1e",
        "text_color": "#f5f5f5",
        "accent": "#00bcd4"
    },
    "핑크 테마": {
        "bg_color": "#fff0f6",
        "text_color": "#4a0033",
        "accent": "#ff69b4"
    },
    "사용자 정의": {}  # 사용자 정의 색상은 따로 저장됨
}

# 세션 초기화
if "selected_theme" not in st.session_state:
    st.session_state.selected_theme = "라이트"
if "custom_theme" not in st.session_state:
    st.session_state.custom_theme = {
        "bg_color": "#eeeeee",
        "text_color": "#111111",
        "accent": "#4CAF50"
    }
if "todos" not in st.session_state:
    st.session_state.todos = []

# ----------------------------
# 🎨 테마 선택 UI
# ----------------------------
st.markdown("## 🎨 테마 설정")
theme_choice = st.selectbox("테마를 선택하세요", list(default_themes.keys()), index=list(default_themes.keys()).index(st.session_state.selected_theme))
st.session_state.selected_theme = theme_choice

# 사용자 정의 테마 색상 선택
if theme_choice == "사용자 정의":
    st.markdown("#### 🎛️ 사용자 정의 색상 선택")
    st.session_state.custom_theme["bg_color"] = st.color_picker("배경색", st.session_state.custom_theme["bg_color"])
    st.session_state.custom_theme["text_color"] = st.color_picker("글자색", st.session_state.custom_theme["text_color"])
    st.session_state.custom_theme["accent"] = st.color_picker("강조색 (버튼 등)", st.session_state.custom_theme["accent"])
    theme = st.session_state.custom_theme
else:
    theme = default_themes[theme_choice]

# ----------------------------
# 🎨 스타일 적용
# ----------------------------
st.markdown(f"""
    <style>
    .stApp {{
        background-color: {theme['bg_color']};
        color: {theme['text_color']} !important;
    }}
    .stMarkdown, .stText, .stDataFrame, .stTable, .stAlert {{
        color: {theme['text_color']} !important;
    }}
    div[role="textbox"] *,
    .stTextInput > div > input,
    .stSelectbox > div > div,
    .stDateInput > div > input {{
        color: {theme['text_color']} !important;
        background-color: transparent;
    }}
    .stButton > button {{
        background-color: {theme['accent']};
        color: white !important;
        border-radius: 5px;
        padding: 0.4em 1em;
        margin-top: 0.5em;
    }}
    label, .css-1cpxqw2 {{
        color: {theme['text_color']} !important;
    }}
    </style>
""", unsafe_allow_html=True)

# ----------------------------
# ✅ 메인 앱
# ----------------------------
st.title("📝 오늘의 할 일 목록")

# 할 일 추가
with st.form("할 일 추가"):
    new_task = st.text_input("할 일을 입력하세요", placeholder="예: 산책하기")
    task_date = st.date_input("기한", value=date.today())
    priority = st.selectbox("우선순위", ["🔴 높음", "🟡 중간", "🟢 낮음"])
    submitted = st.form_submit_button("추가")
    if submitted and new_task.strip():
        st.session_state.todos.append({
            "task": new_task.strip(),
            "done": False,
            "date": task_date,
            "priority": priority
        })

# 할 일 목록 출력
to_delete = None
if st.session_state.todos:
    st.subheader("📋 할 일 목록")

    # 우선순위 정렬
    priority_order = {"🔴 높음": 0, "🟡 중간": 1, "🟢 낮음": 2}
    sorted_todos = sorted(
        st.session_state.todos,
        key=lambda x: (x["date"], priority_order[x["priority"]])
    )

    for i, todo in enumerate(sorted_todos):
        cols = st.columns([0.05, 0.5, 0.2, 0.1, 0.15])
        done = cols[0].checkbox("", value=todo["done"], key=f"check_{i}")
        todo["done"] = done
        task_text = f"~~{todo['task']}~~" if done else todo["task"]
        cols[1].markdown(f"{task_text}  \n📅 {todo['date']}")
        cols[2].markdown(todo["priority"])
        if cols[4].button("삭제", key=f"delete_{i}"):
            to_delete = i

    if to_delete is not None:
        st.session_state.todos.remove(sorted_todos[to_delete])
        st.rerun()
else:
    st.info("할 일을 추가해보세요!")

# 전체 삭제 버튼
if st.session_state.todos:
    if st.button("🗑️ 전체 삭제"):
        st.session_state.todos.clear()
        st.rerun()
