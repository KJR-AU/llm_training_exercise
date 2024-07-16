import requests
import json
from trulens_eval.tru_custom_app import instrument
import os
import json
import re

AppServiceAuthSession = os.getenv("AppServiceAuthSession")

full_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
with open(full_path, 'r') as file:
    config_data = json.load(file)

class RAG_from_scratch:

    def __init__(self, config_data:dict = config_data):
        self.json_response = {}
        self.selected_folders:str = config_data.get('selected_folders', "All") # All, check from the information assistant
        self.selected_tags:str = config_data.get('selected_tags', "") # check from the information assistant
        self.url = config_data.get('url')

    @instrument
    def az_inf_asst_acc_chat_request(self, input):
        request_api = self.url

        body = {
            "history": [{"user": input}],
            "approach": 1,
            "overrides": {
                "semantic_ranker": True,
                "semantic_captions": False,
                "top": 5,
                "suggest_followup_questions": False,
                "user_persona": "analyst",
                "system_persona": "an Assistant",
                "ai_persona": "",
                "response_length": 2048,
                "response_temp": 0.6,
                "selected_folders": self.selected_folders,
                "selected_tags": self.selected_tags
            },
            "citation_lookup": {},
            "thought_chain": {}
        }

        cookies = {"AppServiceAuthSession": AppServiceAuthSession}

        response = requests.post(request_api, json=body, cookies=cookies)
        if response.status_code == 401:
            raise Exception (response, "Check your authentication such as AppServiceAuthSession cookie may have expired")
        if response.status_code == 500:
            message = json.loads(response.content)
            if 'ValueError:' in message["detail"]:
                raise Exception (response, response.content, response.request.body)
        return response
    
    @instrument
    def retrieve(self, query: str) -> list:
        try:
            if not self.json_response["answer"]:
                raise Exception("none")
            matches = re.findall(r'\[File(\d)\]', self.json_response["answer"])
            matches = set(matches)
            used_list = [[self.json_response["data_points"][int(x)]] for x in matches]
            return used_list
        except Exception as e:
                print(f"Exception: retrieve {e}")
                # No return values recorded
                if self.json_response["data_points"]:
                    # If the answer does not refer to any context return all the retrieved context so that the users can check whether relevant or non-relevant contexts were returned.
                    whole_list = [[item] for item in self.json_response["data_points"]]
                    return whole_list
                else:
                    return ""
    @instrument
    def generate_completion(self, query: str, context_str: list) -> str:
        try:
            if not self.json_response["answer"]:
                raise Exception("none")
            return self.json_response["answer"]
        except Exception as e:
            print(f"Exception: completion {e}")
            return ""
    
    @instrument
    def generate_keyword(self, query: str) -> str:
        try:
            if not self.json_response["thought_chain"]["work_search_term"]:
                raise Exception("none")
            return self.json_response["thought_chain"]["work_search_term"]
        except Exception as e:
            print(f"Exception: keyword {e}")
            return ""
        

    @instrument
    def query(self, query: str) -> str:
        response = self.az_inf_asst_acc_chat_request(query)
        self.json_response = json.loads(response.text)

        try:
            if "detail" in self.json_response:
                print("Error for the query: ", query)
                print(self.json_response["detail"])
                raise Exception(self.json_response["detail"])
        except Exception as e:
            print(f"Exception: {e}")
            keyword = self.generate_keyword("")
            context_list = self.retrieve("")
            completion = self.generate_completion(query, [])
            return ""
        
        keyword = self.generate_keyword(self.json_response["thought_chain"]["work_query"])
        context_list = self.retrieve(keyword)
        completion = self.generate_completion(query, context_list)
        return completion

rag_chain = RAG_from_scratch()