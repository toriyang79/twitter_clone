# auth.py
import streamlit as st
from user_manager import UserManager

def show_auth_page():
    """로그인/회원가입 페이지"""
    st.title("🐦 프롬프트 트위터")
    st.markdown("**로그인이 필요합니다**")

    # 탭으로 로그인/회원가입 구분
    tab1, tab2 = st.tabs(["🔑 로그인", "📝 회원가입"])

    user_mgr = UserManager()

    with tab1:
        st.subheader("로그인")

        username = st.text_input("사용자명", key="login_username")
        password = st.text_input("비밀번호", type="password", key="login_password")

        if st.button("로그인", type="primary"):
            if username and password:
                success, user_info = user_mgr.login_user(username, password)

                if success:
                    # Session State에 로그인 정보 저장
                    st.session_state.logged_in = True
                    st.session_state.current_user = user_info
                    st.success(f"✅ {username}님 환영합니다!")
                    st.rerun()
                else:
                    st.error("❌ 사용자명 또는 비밀번호가 틀렸습니다.")
            else:
                st.warning("⚠️ 모든 필드를 입력해주세요.")

    with tab2:
        st.subheader("회원가입")

        new_username = st.text_input("사용자명", key="signup_username")
        new_password = st.text_input("비밀번호", type="password", key="signup_password")
        confirm_password = st.text_input("비밀번호 확인", type="password")

        if st.button("회원가입", type="primary"):
            if new_username and new_password and confirm_password:
                if new_password == confirm_password:
                    success, message = user_mgr.create_user(new_username, new_password)

                    if success:
                        st.success("🎉 " + message)
                        st.info("💡 이제 로그인 탭에서 로그인해보세요!")
                    else:
                        st.error("❌ " + message)
                else:
                    st.error("❌ 비밀번호가 일치하지 않습니다.")
            else:
                st.warning("⚠️ 모든 필드를 입력해주세요.")

    # 현재 가입자 수 표시
    st.sidebar.metric("📊 총 가입자 수", user_mgr.get_user_count())

def logout_user():
    """로그아웃 처리"""
    st.session_state.logged_in = False
    if 'current_user' in st.session_state:
        del st.session_state.current_user
    st.rerun()

