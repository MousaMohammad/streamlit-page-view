import streamlit as st
from code_eval import CodeTester

import streamlit as st

def display_content(key, value):
    if isinstance(value, dict):
        st.subheader(key.replace('_', ' ').title())
        for sub_key, sub_value in value.items():
            display_content(sub_key, sub_value)
    elif isinstance(value, list):
        st.subheader(key.replace('_', ' ').title())
        for item in value:
            display_content("", item)
    else:
        st.text(f"{key.replace('_', ' ').title()}: {value}")

def course_view(course_plan):
    try:
        st.divider()
        st.title(course_plan['project_title'])
        st.subheader('Project Description')
        st.write(course_plan['project_description'])

        st.subheader('Language')
        st.write(course_plan['language'])

        st.subheader('Target Audience')
        st.write(course_plan['target_audience'])

        st.subheader('Difficulty')
        st.write(course_plan['difficulty'])

        st.subheader('Time to Complete (in hours)')
        st.write(course_plan['time_to_complete_in_hours'])

        st.subheader('Number of Stages')
        st.write(course_plan['num_of_stages'])

        st.subheader('List of Stage Titles')
        st.write(course_plan['list_of_stages_titles'])

        for i in range(1, course_plan['num_of_stages'] + 1):
            stage_key = f'stage_{i}'
            stage_title = course_plan['list_of_stages_titles'][i - 1]
            if stage_key in course_plan:
                st.subheader(f'Stage {i}: {stage_title}')
                stage = course_plan[stage_key]
                st.markdown('#### List of Topics')
                for topic in stage['list_of_topics_covered']:
                    st.markdown(f'- {topic}')

                st.markdown('#### Work on Project')
                st.markdown(f'**Description:** {stage["work_on_project"]["description"]}')
                st.markdown(f'**Requirements Functionality:** {stage["work_on_project"]["requirements_functionality"]}')
                st.markdown(f'**Output Example:** {stage["work_on_project"]["output_example"]}')

                if "test_script" in stage:
                    st.subheader("Test Script")
                    st.code(stage["test_script"], language="python", line_numbers=True)
                    if st.button(f"Compile Test Script {i}", key=f"compile_test_script_{i}"):
                        code_tester = CodeTester(st.write)
                        code_tester.check_single_code(stage["test_script"])
                if "code" in stage:
                    st.subheader("Code")
                    st.code(stage["code"], language="python", line_numbers=True)
                    if st.button(f"Compile Code {i}", key=f"compile_code_{i}"):
                        code_tester = CodeTester(st.write)
                        code_tester.check_single_code(stage["code"])
                st.divider()

    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.write(course_plan)