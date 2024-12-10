from numpy import nan
import pandas
import json
import streamlit as st
import io
import random
import string

def generar_clave_aleatoria():
    caracteres = string.ascii_uppercase + string.digits  # Letras mayúsculas y números
    clave = ''.join(random.choices(caracteres, k=6))
    return clave

def get_json_from_excel(excel_file):
    # Read all sheets from Excel
    data_set = pandas.read_excel(excel_file, sheet_name=None)
    
    # Convert DataFrames to lists of dictionaries
    issues = data_set['Issues'].to_dict('records')
    templates = data_set['Templates'].to_dict('records')
    
    # Process each issue
    result = {}
    for issue in issues:
        # Find matching templates for this issue
        matching_subtasks = [
            template for template in templates 
            if template.get('Template') == issue.get('SubTask_Template')
        ]
        
        # Create issue object with subtasks
        issue_key = generar_clave_aleatoria()
        issue_obj = {
            "Project_Key": issue.get('Project_Key'),
            "Component": issue.get('Component'),
            "Version": issue.get('Version'),
            "Epic_External_Key": issue.get('Epic_External_Key'),
            "Epic_Summary": issue.get('Epic_Summary'),
            "Issue_Type": issue.get('Issue_Type'),
            "Issue_External_Key": issue.get('Issue_External_Key'),
            "Issue_Summary": issue.get('Issue_Summary'),
            "Issue_Story_Points": issue.get('Issue_Story_Points'),
            "SubTask_Template": issue.get('SubTask_Template'),
            "Id":issue.get('Id_Issue'),
            "Subtasks": matching_subtasks
        }
        result[issue_key] = issue_obj
    
    # print(result)
    # return result
    # print(type(result))
    json_dump = json.dumps(result, indent=2)
    json_object = json.loads(json_dump)
    # print(type(json_object))
    return json_dump, json_object