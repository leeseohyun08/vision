import streamlit as st
from datetime import date

# --- 기본 테마 ---
default_themes = {
    "라이트": {"bg_color": "#ffffff", "text_color": "#000000", "accent": "#4CAF50"},
    "다크": {"bg_color": "#1e1e1e", "text_color": "#f5f5f5", "accent": "#00bcd4"},
    "핑크 테마": {"bg_color": "#fff0f6", "text_color": "#4a0033", "accent": "#ff69b4"},
    "사용자 정의": {}
}

# --- 세션 초기화 ---
if "selected_theme" not in st.session_state:
    st.session_state.selected_theme = "라이트"
if "custom_theme" not in st.session_state:
    st.session_state.custom_theme = {
        "bg_color": "#eeeeee", "text_color": "#111111", "accent": "#4CAF50"
    }
if "todos" not in st.session_state:
    st.session_state.todos = []

# --- 테마 선택 ---
st.markdown("## 🎨 테마 설정")
theme_choice = st.selectbox("테마를 선택하세요", list(default_themes.keys()),
                            index=list(default_themes.keys()).index(st.session_state.selected_theme))
st.session_state.selected_theme = theme_choice

if theme_choice == "사용자 정의":
    st.session_state.custom_theme["bg_color"] = st.color_picker("배경색", st.session_state.custom_theme["bg_color"])
    st.session_state.custom_theme["text_color"] = st.color_picker("글자색", st.session_state.custom_theme["text_color"])
    st.session_state.custom_theme["accent"] = st.color_picker("강조색", st.session_state.custom_theme["accent"])
    theme = st.session_state.custom_theme
else:
    theme = default_themes[theme_choice]

# --- 스타일 적용 ---
st.markdown(f"""
    <style>
    .stApp {{
        background-color: {theme['bg_color']};
        color: {theme['text_color']} !important;
    }}
    .stButton > button {{
        background-color: {theme['accent']};
        color: white !important;
        border-radius: 5px;
        padding: 0.3em 1em;
        margin-top: 0.3em;
    }}
    .stTextInput input, .stDateInput input {{
        color: {theme['text_color']} !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 할 일 추가 ---
st.title("📝 오늘의 할 일 목록")
with st.form("add_task"):
    task = st.text_input("할 일")
    task_date = st.date_input("기한", date.today())
    priority = st.selectbox("우선순위", ["🔴 높음", "🟡 중간", "🟢 낮음"])
    if st.form_submit_button("추가"):
        if task.strip():
            st.session_state.todos.append({
                "task": task.strip(),
                "date": task_date,
                "priority": priority,
                "done": False
            })

# --- 목록 출력 및 수정 ---
st.subheader("📋 할 일 목록")
priority_order = {"🔴 높음": 0, "🟡 중간": 1, "🟢 낮음": 2}
sorted_todos = sorted(enumerate(st.session_state.todos), key=lambda x: (x[1]["date"], priority_order[x[1]["priority"]]))

to_delete = None
for i, todo in sorted_todos:
    st.markdown("---")
    st.checkbox("완료", value=todo["done"], key=f"done_{i}", on_change=lambda idx=i: st.session_state.todos[idx].update({"done": not todo["done"]}))

    new_task = st.text_input("할 일", todo["task"], key=f"task_{i}")
    new_date = st.date_input("기한", todo["date"], key=f"date_{i}")
    new_priority = st.selectbox("우선순위", ["🔴 높음", "🟡 중간", "🟢 낮음"], index=["🔴 높음", "🟡 중간", "🟢 낮음"].index(todo["priority"]), key=f"prio_{i}")

    cols = st.columns([0.2, 0.2])
    if cols[0].button("💾 저장", key=f"save_{i}"):
        st.session_state.todos[i]["task"] = new_task
        st.session_state.todos[i]["date"] = new_date
        st.session_state.todos[i]["priority"] = new_priority
        st.rerun()
    if cols[1].button("❌ 삭제", key=f"delete_{i}"):
        to_delete = i

if to_delete is not None:
    st.session_state.todos.pop(to_delete)
    st.rerun()

if st.session_state.todos:
    if st.button("🗑️ 전체 삭제"):
        st.session_state.todos.clear()
        st.rerun()
