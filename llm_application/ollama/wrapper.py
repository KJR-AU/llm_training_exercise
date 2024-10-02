import requests
import json
from trulens.apps.custom import instrument
import os
import json
import re

#AppServiceAuthSession = os.getenv("AppServiceAuthSession")

full_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
with open(full_path, 'r') as file:
    config_data = json.load(file)

class RAG_from_scratch:

    def split_curly_braces(self, string):
        #pattern = r'(\{.*?\})'
        pattern = re.compile(r'(\{(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*\})')
        matches = re.findall(pattern, string)
        return matches 
    
    def join_streamed_content(self,json_strings):
        content_list = []
        combined_response = None
    
        for json_str in json_strings:
            try:
                json_obj = json.loads(json_str)
                if "content" in json_obj and json_obj["content"] is not None:
                    content_list.append(json_obj["content"])
                    #print(content_list)
                if "data_points" in json_obj:
                    combined_response = json_obj
                    #print(combined_response)
            except json.JSONDecodeError:
                continue
    
        combined_content = ''.join(content_list)
    
        # Add the combined "content" as an "answer" element to the "details"
        if combined_response:
            combined_response["answer"] = combined_content
        print("combined_response", combined_response)
        return combined_response

    def __init__(self, config_data:dict = config_data):
        self.json_response = {}
        self.selected_folders:str = config_data.get('folders', "All") # All, check from the information assistant
        self.selected_tags:str = config_data.get('tags', "") # check from the information assistant
        self.url = config_data.get('url')
        self.approach = config_data.get('approach', 1) # 1 work only or 3 generative (ungrounded)
        #Note: When using generative (ungrounded) Ground truth and Groundedness cannot be evaluated.

    @instrument
    def ollama_chat_request(self, input):
        request_api = self.url

        headers = {"Authorization": "Bearer sk-0497c984a03344d19474d5100bd927c3",
                   "Content-Type": "application/json"}

        body = {
            "model": "mistral:7b",
            "messages": [
                {
                    "role": "user",
                    "content": input
                }
            ]
        }

        #cookies = {"AppServiceAuthSession": AppServiceAuthSession}
        cookies = ""

        #response = requests.post(request_api, json=body, cookies=cookies)
        print(request_api)
        print(headers)
        print(body)
        response = requests.post(request_api, headers=headers, json=body)
        if response.status_code == 401:
            raise Exception (response, "Check your authentication such as AppServiceAuthSession cookie may have expired")
        if response.status_code == 500:
            message = json.loads(response.content)
            if 'ValueError:' in message["detail"]:
                raise Exception (response, response.content, response.request.body)
        print(response.content)
        return response
    
    @instrument
    def retrieve(self, query: str) -> list:
        try:
            if not self.json_response["answer"]:
                raise Exception("none")
            matches = re.findall(r'\[File(\d)\]', self.json_response["answer"])
            matches = set(matches)
            used_list = [self.json_response["data_points"][int(x)] for x in matches]

            if used_list == []:
                whole_list = [item for item in self.json_response["data_points"]]
                return whole_list
            return used_list
        except Exception as e:
                print(f"Exception: retrieve {e}")
                # No return values recorded
                return ""
    @instrument
    def generate_completion(self, query: str, context_str: list) -> str:
        print("completion: ", self.json_response['choices'][0]['message']['content'])
        try:
            if not self.json_response["choices"][0]["message"]["content"]:
                raise Exception("none")
            
            return [self.json_response["choices"][0]["message"]["content"]]
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
        response = self.ollama_chat_request(query)
        json_strings = self.split_curly_braces(response.text)
        print("JSON Strings")
        for i, entry in enumerate(json_strings):
            print(f"Entry {i}: {entry}")
        
        #print(result[0])
        #print(response.text)
        #print("Processing Streamed Content")
        #combined_details = self.join_streamed_content(json_strings)
        combined_details = json.loads(json_strings[0])
        print("combined_details", json.dumps(combined_details, indent=2))



        self.json_response = json.loads(json.dumps(combined_details, indent=2))
        print("json_response", json.dumps(self.json_response, indent=2))

        try:
            if "detail" in self.json_response:
                print("Error for the query: ", query)
                print(self.json_response["detail"])
                raise Exception(self.json_response["detail"])
        except Exception as e:
            print(f"Exception: {e}")
            if self.approach == 3:
                completion = self.generate_completion(query, [])
                return ""
            #keyword = self.generate_keyword("")
            #context_list = self.retrieve("")
            completion = self.generate_completion(query, [])
            return ""
        
        if self.approach == 3:
            completion = self.generate_completion(query, [])
            return completion
        
        #keyword = self.generate_keyword(self.json_response["thought_chain"]["work_query"])
        #context_list = self.retrieve(keyword)
        #completion = self.generate_completion(query, context_list)
        completion = self.generate_completion(query, [])
        return completion
    