import sys
import os
import json
# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from llm_application.azure_information_assistant_accelerator.wrapper import RAG_from_scratch
from kjr_llm.targets import CustomTarget
from kjr_llm.app import App
from kjr_llm.tests import TestSet
from kjr_llm.targets import Target

from typing import List

from kjr_llm.prompts import PromptSet
from trulens_eval import Select
from kjr_llm.metrics import (
    Groundedness, 
    AnswerRelevance,
    ContextRelevance,
    GroundTruthAgreement
)
current_file_dir = os.path.dirname(os.path.abspath(__file__))
full_path = os.path.join(current_file_dir, 'config-4a.json')
with open(full_path, 'r') as file:
    config_a = json.load(file)

full_path = os.path.join(current_file_dir, 'config-4b.json')
with open(full_path, 'r') as file:
    config_b = json.load(file)

rag_chain_a = RAG_from_scratch(config_data=config_a)
rag_chain_b = RAG_from_scratch(config_data=config_b)

# Set up the test application
app = App(app_name="RAG_Application", reset_database=True)
#app_b = App(app_name="RAG_Application B", reset_database=True)

# Define the target of our tests
target_a: Target = CustomTarget(rag_chain_a)
target_b: Target = CustomTarget(rag_chain_b)

# Load our custom inputs - change the name of this file if you have prepared another prompts.
full_path = os.path.join(current_file_dir, 'relevance-4a.json')
prompts_a = PromptSet.from_json_file(full_path)

full_path = os.path.join(current_file_dir, 'relevance-4b.json')
prompts_b = PromptSet.from_json_file(full_path)

# Import and instantiate feedback metrics
query_path = Select.Record.app.query.args.query
context_path = Select.Record.app.retrieve.rets[:]

# Using custom TestSet
# comment and uncomment the feedback you wish to evaluate
feedbacks_a = [
    Groundedness(context_path),
    ContextRelevance(query_path, context_path),
    AnswerRelevance(),
    GroundTruthAgreement(prompts_a)
]

feedbacks_b = [
    Groundedness(context_path),
    ContextRelevance(query_path, context_path),
    AnswerRelevance(),
    GroundTruthAgreement(prompts_b)
]

# Define our test set
custom_test_a = TestSet(prompts_a, feedbacks_a, name="Exercise4a-openai", default_provider="openai")
custom_test_b = TestSet(prompts_b, feedbacks_b, name="Exercise4b-openai", default_provider="openai")

# Evaluate our test set
result_a = custom_test_a.evaluate(target_a, "Exercise4a")
result_b = custom_test_b.evaluate(target_b, "Exercise4b")

# Run the test dashboard to evaluate results
app.run_dashboard()

# To stop the dashboard you can use close the terminal or ctrl + c to interrupt the terminal.
app.export_result_to_file()
