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
import warnings
warnings.filterwarnings("ignore")
from kjr_llm.prompts import PromptSet
from trulens.core.schema import Select
from kjr_llm.metrics import (
    Groundedness, 
    AnswerRelevance,
    ContextRelevance,
    GroundTruthAgreement,
)

from kjr_llm.tests.lib import (
    Hate,
    Harassment,
    Violence,
    Criminality, 
    Maliciousness, 
    SelfHarm, 
    Insensitivity
)

from trulens.providers.huggingface import Huggingface
from trulens.core import Feedback

hugs = Huggingface()

# Define a pii_detection feedback function using HuggingFace.
f_pii_detection = Feedback(hugs.pii_detection_with_cot_reasons).on_output()
# By default this will check language match on the main app input


current_file_dir = os.path.dirname(os.path.abspath(__file__))
full_path = os.path.join(current_file_dir, 'config-5.json')
with open(full_path, 'r') as file:
    config = json.load(file)

rag_chain = RAG_from_scratch(config_data=config)

# Set up the test application
app = App(app_name="RAG_Application", reset_database=True)

# Define the target of our tests
target: Target = CustomTarget(rag_chain)

# Load our custom inputs - change the name of this file if you have prepared another prompts.
full_path = os.path.join(current_file_dir, 'privacy-5b.json')
prompts = PromptSet.from_json_file(full_path)

# Import and instantiate feedback metrics
query_path = Select.Record.app.query.args.query
context_path = Select.Record.app.retrieve.rets[:]


# Using predefined test set
#tests: List[TestSet] = [
#    Criminality,
#    Hate,
#    Insensitivity
#     Hate
#]

# run predefined tests
#test_provider = "openai"
#for test in tests:
#    test.default_provider = test_provider
#test_results = [test.evaluate(target, app_id=f"{app.app_name}-{test.name}") for test in tests]


# Using custom TestSet
# comment and uncomment the feedback you wish to evaluate
feedbacks = [
    f_pii_detection,
    Groundedness(context_path),
    ContextRelevance(query_path, context_path),
    AnswerRelevance(),
    GroundTruthAgreement(prompts)
]

# Define custom test set
custom_test = TestSet(prompts, feedbacks, name="Exercise5b-openai", default_provider=OpenAIProvider(model_name="gpt-3.5-turbo"))

# Evaluate custom test set
result = custom_test.evaluate(target, "Exercise5b")

# Run the test dashboard to evaluate results
app.run_dashboard()

# To stop the dashboard you can use close the terminal or ctrl + c to interrupt the terminal.
app.export_result_to_file([result])
