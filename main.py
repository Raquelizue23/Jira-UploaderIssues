import pandas
import json
import streamlit as st
import io
import converterXlsxToJson as converter
import jiraClientApi
import jiraService

token=""
email=""
url = ""
project_key = ""
text_placeholder = st.empty()


st.header("Jira Uploader Issues", divider="blue")
# # st.divider()

column_1, column_2, column_3 = st.columns(3)
data_formarter=""

with st.sidebar:
    # File uploader
    uploaded_file = st.file_uploader("Sube tu archivo excel de Issues", type=['xlsx'])
    if uploaded_file is not None:
        data_formarter_json, data_formarter = converter.get_json_from_excel(uploaded_file)
        # st.text_area("JSON Output", json_dump, height=400)
        
        if data_formarter!="":
            # Add download button
            st.download_button(
                label="Descargar JSON para Jira",
                data=data_formarter_json,
                file_name="converted_file.json",
                mime="application/json"
            )

            token = st.text_input('Jira Key', type="password")
            url = st.text_input('Jira Domain/URL', '')
            email= st.text_input('Jira Email', '')
            if token and url and email:
            # se inicializa el objeto de jira_client_api en el jiraService.py
                jiraService.initialize_jira_client_api(url, email, token)

with column_1:
    if token and url and email:
        if st.button("Crear Issues con subtasks"):
            if data_formarter!="":
                # Create issues
                st.divider()
                response = jiraService.bulk_create_issues_subtask(data_formarter, "all")

with column_2:
    if token and url and email:
        if st.button("Crear Issues"):
            if data_formarter!="":
                # Create issues
                st.divider()
                response = jiraService.bulk_create_issues_subtask(data_formarter, "issues")

with column_3:            
    if token and url and email:
        if st.button("Crear Subtask"):
            if data_formarter!="":
                # Create issues
                st.divider()
                st.markdown(":blue-background[Inicia] proceso de creación de Subtareas")
                response = jiraService.create_bulk_subtasks(data_formarter)
                st.markdown(":blue-background[Fin] del proceso de creación de Subtareas")
                if st.button("Limpiar textos de salida"):
                    text_placeholder.empty()
                
              
