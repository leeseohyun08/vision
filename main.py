import streamlit as st
from datetime import date

# 페이지 기본 설정
st.set_page_config(page_title="할 일 목록", page_icon="📝")

# ----- 🎨 테마 선택 -----
themes = {
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
    }
}

st.sidebar.header("🎨 테마 설정")
selected_theme = st.sidebar.selectbox("테마 선택", list(themes.keys()))
theme = themes[selected_theme]

# ----- 💄 CSS 스타일 적용 -----
st.markdown(f"""
    <style>
        body {{
            background-color: {theme['bg_color']};
            color: {theme['text_color']};
        }}
        .stApp {{
            background-color: {theme['bg_color']};
            color: {theme['text_color']};
        }}
        .stTextInput > div > div > input {{
            background-color: #f5f5f5;
        }}
        .stButton>button {{
            background-color: {theme['accent']} !important;
            color: white !important;
            border-radius: 5px;
        }}
    </style>
""", unsafe_allow_html=True)

st.title("📝 오늘의 할 일 목록")

# ----- 📦 세션 상태 초기화 -----
if "todos" not in st.session_state:
    st.session_state.todos = []

# ----- ✅ 할 일 추가 -----
with st.form(key="add_todo"):
    new_task = st.text_input("할 일을 입력하세요", placeholder="예: 운동하기")
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

# 삭제 요청 저장
to_delete = None

# ----- 📋 할 일 목록 -----
st.subheader("📋 할 일 목록")

if st.session_state.todos:
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

# 전체 삭제
if st.session_state.todos:
    if st.button("🗑️ 전체 삭제"):
        st.session_state.todos.clear()
        st.rerun()
