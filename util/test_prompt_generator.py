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
        self.prompts = self.load_prompts()
        self.example_inputs = self.extract_inputs()

    def load_prompts(self):
        # Load prompts from a JSON file
        if self.prompt_file == '':
            return [{}]
        current_file_dir = os.path.dirname(os.path.abspath('__file__'))
        full_path = os.path.join(current_file_dir, self.prompt_file + '.json')
        with open(full_path, 'r') as file:
            return json.load(file)

    def extract_inputs(self):
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