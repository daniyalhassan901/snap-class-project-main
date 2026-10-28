
import streamlit as st

from src.screens.home_screen import home_screen
from src.screens.teacher_screen import teacher_screen
from src.screens.student_screen import student_screen

from src.components.dialog_auto_enroll import auto_enroll_dialog

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
# ... your other imports ...

hide_logos = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stAppDeployButton {display:none !important;}
div[data-testid="stToolbar"] {visibility: hidden !important; height: 0 !important;}
div[data-testid="stDecoration"] {visibility: hidden !important;}
div[data-testid="stStatusWidget"] {visibility: hidden !important;}
a[data-testid="stAppDeployButton"] {display: none !important;}
button[kind="header"] {display: none !important;}
</style>
"""
st.markdown(hide_logos, unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title='SnapClass - Making Attendance faster using AI',
        page_icon= "https://i.ibb.co/YTYGn5qV/logo.png"
    )
    if 'login_type' not in st.session_state:
        st.session_state['login_type'] = None
    if 'is_logged_in' not in st.session_state:
        st.session_state['is_logged_in'] = False
    if 'user_role' not in st.session_state:
        st.session_state['user_role'] = None

    match st.session_state['login_type']:
        case 'teacher':
            teacher_screen()

        case 'student':
            student_screen()
        
        case None:
            home_screen()


    join_code = st.query_params.get('join-code')
    if join_code:
        if st.session_state.login_type != 'student':
            st.session_state.login_type = 'student'
            st.rerun()
        if st.session_state.get('is_logged_in') and st.session_state.get('user_role') == 'student':
            auto_enroll_dialog(join_code)
if __name__ == "__main__":
    main()

