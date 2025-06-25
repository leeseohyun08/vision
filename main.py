import streamlit as st

st.set_page_config(page_title="할 일 목록", page_icon="📝")
st.title("📝 오늘의 할 일 목록")

# 세션 상태 초기화
if "todos" not in st.session_state:
    st.session_state.todos = []

# 할 일 추가
with st.form(key="add_todo"):
    new_todo = st.text_input("새로운 할 일 입력", placeholder="예: 영어 단어 외우기")
    submitted = st.form_submit_button("추가")

    if submitted and new_todo.strip() != "":
        st.session_state.todos.append({"task": new_todo.strip(), "done": False})

# 삭제 요청 저장용
to_delete = None

# 할 일 목록 출력
st.subheader("📋 목록")

if st.session_state.todos:
    for i, todo in enumerate(st.session_state.todos):
        cols = st.columns([0.1, 0.75, 0.15])

        # 체크박스
        is_done = cols[0].checkbox("", value=todo["done"], key=f"checkbox_{i}")
        st.session_state.todos[i]["done"] = is_done

        # 줄긋기 처리
        task_text = f"~~{todo['task']}~~" if is_done else todo["task"]
        cols[1].markdown(task_text)

        # 삭제 버튼
        if cols[2].button("삭제", key=f"delete_{i}"):
            to_delete = i

    # 삭제 처리 (반복문 밖에서!)
    if to_delete is not None:
        st.session_state.todos.pop(to_delete)
        st.query_params.clear()  # ✅ 최신 방식
else:
    st.info("할 일을 추가해보세요!")

# 전체 삭제 버튼
if st.session_state.todos:
    if st.button("🗑️ 전체 삭제"):
        st.session_state.todos.clear()
        st.query_params.clear()  # ✅ 최신 방식
