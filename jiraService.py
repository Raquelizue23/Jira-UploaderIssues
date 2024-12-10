
import jiraClientApi
import streamlit as st
import json

jira_client_api = None
text_placeholder = st.empty()

def initialize_jira_client_api(url, email, token):
    global jira_client_api
    jira_client_api = jiraClientApi.JiraApiService(
                jira_url=url,
                email=email,
                api_token=token
            )

def get_custom_fields():
    custom_fields = jira_client_api.get_custom_fields()
    obj_custom_field = {
        'ProcessGroup': None,
        'ExternalKey': None,
        'StoryPoints': None,
        'Template': None,
        'Effort': None,
        'EpicLink': None
    }
    
    for field in custom_fields:
        if field['name'] == 'Process Group':
            obj_custom_field['ProcessGroup'] = field['key']
        elif field['name'] == 'External Key':
            obj_custom_field['ExternalKey'] = field['key']
        elif field['name'] in ['Story Points', 'Story points']:
            obj_custom_field['StoryPoints'] = field['key']
        elif field['name'] == 'Template':
            obj_custom_field['Template'] = field['key']
        elif field['name'] == 'Effort %':
            obj_custom_field['Effort'] = field['key']
        elif field['name'] == 'Epic Link':
            obj_custom_field['EpicLink'] = field['key']
    # print(obj_custom_field)
    return obj_custom_field

def get_array_for_bulk(array_issues):
    array_issues_bulk = []
    start = 0
    end = 50
    
    cociente = len(array_issues) // 50
    residuo = len(array_issues) % 50
    
    for i in range(cociente):
        array_issues_bulk.append(array_issues[start:end])
        start = start + 50
        end = end + 50
    
    if residuo != 0:
        start = 50 * cociente
        array_issues_bulk.append(array_issues[start:len(array_issues)])
    
    return array_issues_bulk

def create_bulk_subtasks(issues):
    custom_fields = get_custom_fields()
    subtasks = []
    for issue in issues.values():
        # print(issue)
        for subtask in issue["Subtasks"]:
            if "-" in issue["Id"]:
                obj_subtask = {
                    "fields": {
                        "project": {
                            "key": issue["Project_Key"]
                        },
                        "issuetype": {
                            "name": "Sub-task"
                        },
                        "parent": {
                            "key": issue["Id"]
                        },
                        custom_fields["Template"]: subtask["Template"],
                        custom_fields["ProcessGroup"]: subtask["Process_Group"],
                        "summary": subtask["SubTask"],
                        "timetracking": {
                            "originalEstimate": subtask["Effort"]
                        }
                    }
                }
            else:
                obj_subtask = {
                    "fields": {
                        "project": {
                            "key": issue["Project_Key"]
                        },
                        "issuetype": {
                            "name": "Sub-task"
                        },
                        "parent": {
                            "id": issue["Id"]
                        },
                        custom_fields["Template"]: subtask["Template"],
                        custom_fields["ProcessGroup"]: subtask["Process_Group"],
                        "summary": subtask["SubTask"],
                        "timetracking": {
                            "originalEstimate": subtask["Effort"]
                        }
                    }
                }
            subtasks.append(obj_subtask)

    if len(subtasks) > 50:
        array_issues_bulk = get_array_for_bulk(subtasks)
        for bulk in array_issues_bulk:
            status_response, bulk_subtasks = jira_client_api.bulk_create_issues(bulk)
            st.text(f"Status response bulk Subtask: {status_response}")
            if status_response.status_code == 400:
                st.text(f"Error al hacer el bulk de Subtareas")
                st.text_area("Payload de la petición", json.dumps(issues), height=400)
            
    else:
        status_response, bulk_subtasks = jira_client_api.bulk_create_issues(subtasks)
        st.text(f"Status response bulk Subtask: {status_response}")
        if status_response.status_code == 400:
            st.text(f"Error al hacer el bulk de Subtareas")
            st.text_area("Payload de la petición", json.dumps(issues), height=400)
        


def bulk_create_issues_subtask(data_formarter, type):
    issues = []
    print("-----------------------------------------------------------")
    custom_fields = get_custom_fields()
    for issue in data_formarter.values():
        fields  = {
            "fields": {
                "project": {
                    "key": issue["Project_Key"]
                },
                "summary": issue["Issue_Summary"][:255] if issue["Issue_Summary"] else "",
                "description": issue["Issue_Summary"],
                "issuetype": {
                    "name": issue["Issue_Type"]
                }
            }
        }
        if issue["Issue_Type"] != "Task":
            fields[custom_fields["StoryPoints"]] = issue["Issue_Story_Points"]
        
        obj_issue = {
            "fields": fields
        }
        # print(obj_issue)
        issues.append(obj_issue)
    
    st.markdown(":blue-background[Inicia] proceso de creación de Issues")
    if len(issues) > 50:
        array_issues_bulk = get_array_for_bulk(issues)
        array_issues = get_array_for_bulk(data_formarter)
        
        for i, bulk in enumerate(array_issues_bulk): 
            status_response, bulk_issues = jira_client_api.bulk_create_issues(bulk)
            st.text(f"Status response bulk Issues: {status_response}")

            if status_response.status_code == 400:
                st.text(f"Error al hacer el bulk de Issues")
                st.text_area("Payload de la petición", json.dumps(bulk), height=400)
                st.text_area("Errors", json.dumps(bulk_issues), height=400)
            if status_response.status_code == 201:
                if type=="all":
                    for i, issue in enumerate(data_formarter):
                        data_formarter[issue]["Id"] = bulk_issues['issues'][i]['id']
                        data_formarter[issue]["Key"] = bulk_issues['issues'][i]['key']
                    create_bulk_subtasks(data_formarter)


    else:
        status_response,bulk_issues = jira_client_api.bulk_create_issues(issues)
        st.text(f"Status response bulk Issues: {status_response}")
        if status_response.status_code == 400:
            st.text(f"Error al hacer el bulk de Issues")
            st.text_area("Payload de la petición", json.dumps(issues), height=400)
            st.text_area("Errors", json.dumps(bulk_issues), height=400)
        if status_response.status_code == 201:
            if type=="all":    
                for i, issue in enumerate(data_formarter):
                    data_formarter[issue]["Id"] = bulk_issues['issues'][i]['id']
                    data_formarter[issue]["Key"] = bulk_issues['issues'][i]['key']
                create_bulk_subtasks(data_formarter)
            
    st.markdown(":blue-background[Fin] del proceso de creación de Issues son subtareas")
    if st.button("Limpiar textos de salida"):
        text_placeholder.empty()
    

