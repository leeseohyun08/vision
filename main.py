import streamlit as st
from datetime import date

st.set_page_config(page_title="할 일 목록", page_icon="📝")
st.title("📝 오늘의 할 일 목록")

# 초기화
if "todos" not in st.session_state:
    st.session_state.todos = []

# 할 일 추가 폼
with st.form(key="add_todo"):
    new_task = st.text_input("할 일을 입력하세요", placeholder="예: 수학 문제 풀기")
    task_date = st.date_input("언제까지 해야 하나요?", value=date.today())
    priority = st.selectbox("우선순위", ["🔴 높음", "🟡 중간", "🟢 낮음"])
    submitted = st.form_submit_button("추가")

    if submitted and new_task.strip():
        st.session_state.todos.append({
            "task": new_task.strip(),
            "done": False,
            "date": task_date,
            "priority": priority
        })

# 삭제 요청 저장용
to_delete = None

st.subheader("📋 할 일 목록")

if st.session_state.todos:
    # 우선순위 정렬 (높음 > 중간 > 낮음)
    priority_order = {"🔴 높음": 0, "🟡 중간": 1, "🟢 낮음": 2}
    sorted_todos = sorted(
        st.session_state.todos,
        key=lambda x: (x["date"], priority_order[x["priority"]])
    )

    for i, todo in enumerate(sorted_todos):
        cols = st.columns([0.1, 0.5, 0.2, 0.1, 0.1])

        # 체크박스 (완료 여부)
        done = cols[0].checkbox("", value=todo["done"], key=f"check_{i}")
        todo["done"] = done

        # 할 일 텍스트
        task_text = f"~~{todo['task']}~~" if done else todo["task"]
        cols[1].markdown(f"{task_text}  \n📅 {todo['date']}")

        # 우선순위
        cols[2].markdown(todo["priority"])

        # 삭제 버튼
        if cols[4].button("삭제", key=f"delete_{i}"):
            to_delete = i

    # 삭제 처리
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
