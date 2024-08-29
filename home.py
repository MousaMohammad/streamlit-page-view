import json
import streamlit as st
from course_view import course_view

course_plan = st.file_uploader("Upload Course plan json file", type="json")

if course_plan:
    try:
        course_structure = json.load(course_plan)
    except json.JSONDecodeError:
        st.error("Invalid JSON file")
        st.stop()
    course_view(course_structure)