import requests
from requests.auth import HTTPBasicAuth
import json
import streamlit as st
class JiraApiService:
    def __init__(self, jira_url, email, api_token):
        self.base_url = jira_url
        self.auth = HTTPBasicAuth(email, api_token)
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    def get_custom_fields(self):
        """
        Retrieve custom fields for a specific Jira project
        """
        endpoint = f"{self.base_url}/rest/api/2/field"
        
        try:
            response = requests.get(
                endpoint,
                headers=self.headers,
                auth=self.auth
            )
            response.raise_for_status()
            
            # Filter only custom fields
            all_fields = response.json()
            custom_fields = [field for field in all_fields if field.get('custom', False)]
            
            return custom_fields
            
        except requests.exceptions.RequestException as e:
            print(f"Error retrieving custom fields: {str(e)}")
            return None
        
    def bulk_create_issues(self, issues_data):
        """
        Create multiple Jira issues in bulk
        Returns:
            dict: Response containing created issues data
        """
        endpoint = f"{self.base_url}/rest/api/2/issue/bulk"
        
        payload = {
            "issueUpdates": issues_data
        }
        
        try:
            response = requests.post(
                endpoint,
                headers=self.headers,
                auth=self.auth,
                data=json.dumps(payload)
            )
            return response,response.json() 
            
        except requests.exceptions.RequestException as e:
            print(f"Error creating bulk issues: {str(e)}")
            print(f"Error Type: {type(e).__name__}")
            print(f"Error Details: {str(e)}")
            print(f"Payload: {json.dumps(payload, indent=2)}")
        
            return None