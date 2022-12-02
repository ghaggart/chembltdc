import pytest
import os
import requests
import json
import prison
import pprint

class TestAPI:
    """TestAPI class. Tests the API connections
    """

    # TODO: Provide more API methods to retrieve nested objects

    def test_api_access(self):
        
        session = requests.session()
        response = session.post('http://localhost/api/v1/security/login',json={"username": os.environ['API_ADMIN_USER'],"password": os.environ['API_ADMIN_PASSWORD'],"provider": "db"})
        if response.status_code == 200:
            content = json.loads(response.content.decode('utf-8'))
            token = content['access_token']
            filters = [{"col": "canonical_smiles", "opr": "eq", "value":"Cc1cc(-n2ncc(=O)[nH]c2=O)ccc1C(=O)c1ccc(C#N)cc1"}]
            response = session.get(f"http://localhost/api/v1/compound_structure",
                                   params={"q":prison.dumps({"filters": filters})},
                                   headers={'Authorization': 'Bearer '+ token})
            assert response.status_code == 200
            content = json.loads(response.content.decode('utf-8'))
            assert content['count'] == 1
            pprint.pprint(content)