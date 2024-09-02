import sys
import os
import json
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from llm_application.azure_information_assistant_accelerator.wrapper import RAG_from_scratch
from kjr_llm.targets import CustomTarget
from kjr_llm.app import App
from kjr_llm.tests import TestSet
from kjr_llm.targets import Target
from kjr_llm.provider import OpenAIProvider

from typing import List

from trulens.core.schema import Select

from kjr_llm.tests.lib import (
    Hate
)

current_file_dir = os.path.dirname(os.path.abspath(__file__))
full_path = os.path.join(current_file_dir, 'config-5.json')
with open(full_path, 'r') as file:
    config = json.load(file)

rag_chain = RAG_from_scratch(config_data=config)

# Set up the test application
app = App(app_name="RAG_Application", reset_database=True)

# Define the target of our tests
target: Target = CustomTarget(rag_chain)

# Import and instantiate feedback metrics
query_path = Select.Record.app.query.args.query
context_path = Select.Record.app.retrieve.rets[:]


# Using predefined test set
tests: List[TestSet] = [
     Hate
]

# run predefined tests
test_provider = OpenAIProvider(model_name="gpt-3.5-turbo")
for test in tests:
    test.default_provider = test_provider
test_results = [test.evaluate(target, app_id=f"{app.app_name}-{test.name}") for test in tests]

# Run the test dashboard to evaluate results
app.run_dashboard()

# To stop the dashboard you can use close the terminal or ctrl + c to interrupt the terminal.
app.export_result_to_file(test_results)
