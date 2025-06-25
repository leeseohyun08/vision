import streamlit as st
from datetime import date

# --- 테마 정의 ---
default_themes = {
    "라이트": {"bg_color": "#ffffff", "text_color": "#000000", "accent": "#4CAF50"},
    "다크": {"bg_color": "#1e1e1e", "text_color": "#f5f5f5", "accent": "#00bcd4"},
    "핑크 테마": {"bg_color": "#fff0f6", "text_color": "#4a0033", "accent": "#ff69b4"},
    "사용자 정의": {}
}

# --- 세션 상태 초기화 ---
if "selected_theme" not in st.session_state:
    st.session_state.selected_theme = "라이트"
if "custom_theme" not in st.session_state:
    st.session_state.custom_theme = {
        "bg_color": "#eeeeee", "text_color": "#111111", "accent": "#4CAF50"
    }
if "todos" not in st.session_state:
    st.session_state.todos = []
if "edit_index" not in st.session_state:
    st.session_state.edit_index = None

# --- 테마 선택 UI ---
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

# --- CSS 스타일 적용 ---
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

# --- 할 일 추가 폼 ---
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

# --- 정렬 기준 ---
priority_order = {"🔴 높음": 0, "🟡 중간": 1, "🟢 낮음": 2}
sorted_todos = sorted(st.session_state.todos, key=lambda x: (x["date"], priority_order[x["priority"]]))

# --- 목록 출력 ---
st.subheader("📋 할 일 목록")
edit_index = st.session_state.edit_index
to_delete = None

for i, todo in enumerate(sorted_todos):
    if edit_index == i:
        # --- 수정 폼 ---
        with st.form(f"edit_form_{i}"):
            new_task = st.text_input("할 일 수정", todo["task"])
            new_date = st.date_input("기한 수정", todo["date"])
            new_priority = st.selectbox("우선순위 수정", ["🔴 높음", "🟡 중간", "🟢 낮음"],
                                        index=["🔴 높음", "🟡 중간", "🟢 낮음"].index(todo["priority"]))
            save = st.form_submit_button("저장")
            cancel = st.form_submit_button("취소")
            if save:
                todo["task"] = new_task
                todo["date"] = new_date
                todo["priority"] = new_priority
                st.session_state.edit_index = None
                st.rerun()
            elif cancel:
                st.session_state.edit_index = None
                st.rerun()
    else:
        # --- 일반 출력 모드 ---
        cols = st.columns([0.05, 0.5, 0.15, 0.07, 0.07])
        todo["done"] = cols[0].checkbox("", value=todo["done"], key=f"done_{i}")
        task_display = f"~~{todo['task']}~~" if todo["done"] else todo["task"]
        cols[1].markdown(f"{task_display}  \n📅 {todo['date']}")
        cols[2].markdown(todo["priority"])
        if cols[3].button("✏️", key=f"edit_{i}"):
            st.session_state.edit_index = i
            st.rerun()
        if cols[4].button("🗑️", key=f"del_{i}"):
            to_delete = i

# --- 삭제 처리 ---
if to_delete is not None:
    st.session_state.todos.remove(sorted_todos[to_delete])
    st.rerun()

# --- 전체 삭제 버튼 ---
if st.session_state.todos:
    if st.button("🗑️ 전체 삭제"):
        st.session_state.todos.clear()
        st.rerun()
