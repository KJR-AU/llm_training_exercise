# KJR LLM Testing Exercises
This repository contains exercises to supplement the material delivered in KJR's LLM-testing training course. 

## Instructions
The exercises are intended to be completed in a `Github Codespace`, a vscode-based containerised development environment which can be accessed from a browser and will enable you to run the required code examples. 

The environment will come preinstalled with relevant `vscode extensions`, a compatible version of the `Python` programming language and suite of `Python packages` required to run the exercises.  

### Creating a Codespace
1. Ensure that you are on the `main` branch, click the `Code` button, then the `Codespaces` tab and finally press the `+` to spin up a new codespace. 

2. The codespace will automatically open in a new tab in your browser and take a few minutes to build.

3. Navigate to https://platform.openai.com/api-keys and create a new Open AI API key, it should looking something like this:

`sk-XXXXXXXXXXXXXXXXXXXXXXXX`

4. Open the `.env` file and paste the key you just created into the quote marks next to `OPENAI_API_KEY`, once done the file should look like this:
```
OPENAI_API_KEY="sk-XXXXXXXXXXXXXXXXXXXXXXXX" 
```
