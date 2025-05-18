from azure.identity import DefaultAzureCredential, ClientSecretCredential
import requests
import json
from dotenv import load_dotenv
import os

class FabricClient:
    """
    A class to interact with the Microsoft Fabric REST API.
    """
    _base_url = "https://api.fabric.microsoft.com/v1"

    def __init__(self):
        """
        Initializes the FabricClient instance with Azure Active Directory credentials.
        """
        self._token = self.__authenticate()
        self.headers = {
            "Authorization": f"Bearer {self._token}",
            "Content-Type": "application/json"
        }

    def __authenticate(self):
        """
        Authenticates using Azure AD credentials and retrieves an OAuth2 token 
        for Microsoft Fabric API requests. Falls back to DefaultAzureCredential 
        if secrets are not available.

        Returns:
            str: The authentication token for API access.
        """
        load_dotenv(override=True)
        tenant_id = os.getenv("TenantId")
        client_id = os.getenv("ClientId")
        client_secret = os.getenv("ClientSecret")
        
        if tenant_id and client_id and client_secret:
            print("Using client secret authentication")
            credential = ClientSecretCredential(tenant_id, client_id, client_secret)
        else:
            print("Using default Azure credential authentication")
            credential = DefaultAzureCredential()

        token = credential.get_token("https://api.fabric.microsoft.com/.default").token

        return token

    def list_workspaces(self):
        """
        Lists all workspaces accessible by the authenticated user in Microsoft Fabric.

        Returns:
            list: A list of workspace metadata dictionaries.
        """
        url = f"{self._base_url}/workspaces"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            return response.json()['value']
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

# Execution starts here
if __name__ == "__main__":

    fabric_client = FabricClient()
    print(fabric_client.list_workspaces())
