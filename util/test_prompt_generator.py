import os
import json
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from trulens_eval.generate_test_set import GenerateTestSet

class GenerateTestPrompts:
    def __init__(self, llm=None, chain=None, model="gpt-3.5-turbo", temperature=0, prompt_file=''):
        # Initialize the class with optional parameters
        self.llm = llm if llm else ChatOpenAI(temperature=temperature, model=model)
        self.simple_chain = chain if chain else self.llm | StrOutputParser()
        self.prompt_file = prompt_file
        self.prompts = self._load_prompts()
        self.example_inputs = self._extract_inputs()

    def _load_prompts(self):
        # Load prompts from a JSON file
        if self.prompt_file == '':
            return [{}]
        current_file_dir = os.path.dirname(os.path.abspath('__file__'))
        full_path = os.path.join(current_file_dir, self.prompt_file + '.json')
        with open(full_path, 'r') as file:
            return json.load(file)

    def _extract_inputs(self):
        # Extract input values from the loaded prompts
        example_inputs = []
        for input in self.prompts:
            for key, value in input.items():
                if key == 'input':
                    example_inputs.append(value)
        return example_inputs

    def generate_test_prompts(self, test_breadth, test_depth, examples=None):
        # Generate test prompts using the specified parameters
        test = GenerateTestSet(app_callable=self.simple_chain.invoke)
        test_set = test.generate_test_set(
            test_breadth=test_breadth,
            test_depth=test_depth,
            examples=examples if examples else self.example_inputs
        )
        self.test_set = test_set
        return test_set
    
    def filter_categories(self, test_set = None):
        if test_set is None:
            test_set = self.test_set
        categories = [category for category in test_set]
        print("Here's list of categories: ", categories)
        categories_to_keep = []
        while True:
            user_input = input("Enter a category you wish to keep, put in exact word, capital and lowercase sensitive (or type 'done' to finish): ")
            if user_input.lower() == 'done':
                break
            categories_to_keep.append(user_input)

        categories_to_keep = set(categories_to_keep)
        categories_to_keep.discard('')
        categories_to_keep = [value for value in categories if value in categories_to_keep]
        print("Your list:", categories_to_keep)
        if categories_to_keep == []:
            print("No existing categories selected so, no filter applied")
            return test_set
        filtered_data = {category: test_set[category] for category in categories_to_keep}
        return filtered_data

    def export_to_json_file(self, test_set=None, filename="generated_prompts"):
        # Export the generated prompts to a JSON file
        if test_set is None:
            test_set = self.test_set
        json_prompt = []
        for category in test_set:
            for i in test_set[category]:
                string = '{"input": "' + i + '", "expected_output": null}'
                new_data = json.loads(string)
                json_prompt.append(new_data)

        with open(filename + '.json', "w") as outfile:
            outfile.write(json.dumps(json_prompt, indent=4))
        return json_prompt

    
# How to use
# generator = GenerateTestPrompts()
# generated_prompts = generator.generate_test_prompts(test_breadth=2,test_depth=1)
# print(generated_prompts)
# Generate a file "generated_prompts.json" with the generated prompts formatted.
# generator.export_to_json_file(generated_prompts)