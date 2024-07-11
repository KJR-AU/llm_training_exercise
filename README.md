# llm_training_exercise

# Set up
Python >= 3.10 (recommended)

# For how to use Azure information assistant wrapper to integrate with llm_test_framework:
1. clone the git repository
```
git clone https://github.com/KJR-AU/llm_training_exercise.git
```

2. Fill in .env file like below:
```
Create new secret key from here: https://platform.openai.com/api-keys and paste the key here
OPENAI_API_KEY = "" 

```
3. Create .venv and install requirements
```bash
python -m venv .venv
```

```bash
.venv\Scripts\activate
```

```bash
pip install git+https://github.com/KJR-AU/llm_test_framework
pip install -r requirements.txt
```

4. Install jupyter notebook extension and python extension
Name: Jupyter
Id: ms-toolsai.jupyter
Description: Jupyter notebook support, interactive programming and computing that supports Intellisense, debugging and more.
Version: 2024.6.0
Publisher: Microsoft
VS Marketplace Link: https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter

and 

Name: Python
Id: ms-python.python
Description: Python language support with extension access points for IntelliSense (Pylance), Debugging (Python Debugger), linting, formatting, refactoring, unit tests, and more.
Version: 2024.10.0
Publisher: Microsoft
VS Marketplace Link: https://marketplace.visualstudio.com/items?itemName=ms-python.python