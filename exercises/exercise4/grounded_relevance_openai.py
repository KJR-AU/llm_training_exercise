import sys
import os
# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from llm_application.azure_information_assistant_accelerator.wrapper import rag_chain
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


# Set up the test application
app = App(app_name="RAG_Application", reset_database=True)

# Define the target of our tests
target: Target = CustomTarget(rag_chain)

# Load our custom inputs - change the name of this file if you have prepared another prompts.
# Load our custom inputs - change the name of this file if you have prepared another prompts.
current_file_dir = os.path.dirname(os.path.abspath(__file__))
full_path = os.path.join(current_file_dir, 'relevance_and_groundedness_prompts.json')
prompts = PromptSet.from_json_file(full_path)

# Import and instantiate feedback metrics
query_path = Select.Record.app.query.args.query
context_path = Select.Record.app.retrieve.rets[:]

# Using custom TestSet
# comment and uncomment the feedback you wish to evaluate
feedbacks = [
    Groundedness(context_path),
    ContextRelevance(query_path, context_path),
    AnswerRelevance(),
    GroundTruthAgreement(prompts)
]

# Define our test set
custom_test = TestSet(prompts, feedbacks, name="Exercise4-openai", default_provider="openai")

# Evaluate our test set
result = custom_test.evaluate(target)

# Run the test dashboard to evaluate results
app.run_dashboard()

# To stop the dashboard you can use close the terminal or ctrl + c to interrupt the terminal.
app.export_result_to_file()