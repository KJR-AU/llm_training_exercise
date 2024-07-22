# https://github.com/devcontainers/images/tree/main/src/python

# [Choice] Python version (use -bookworm or -bullseye variants on local arm64/Apple Silicon): 3, 3.12, 3.11, 3.10, 3.9, 3.8, 3-bookworm, 3.12-bookworm, 3.11-bookworm, 3.10-bookworm, 3.9-bookworm, 3.8-bookworm, 3-bullseye, 3.12-bullseye, 3.11-bullseye, 3.10-bullseye, 3.9-bullseye, 3.8-bullseye, 3-buster, 3.12-buster, 3.11-buster, 3.10-buster, 3.9-buster, 3.8-buster
ARG VARIANT=3.10-bullseye
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

# Poetry and other dependencies
RUN pip install ipykernel && \
    pip install langchain-openai && \
    pip install scikit-learn

# [Optional] Uncomment this section to install additional OS packages.
RUN apt update && export DEBIAN_FRONTEND=noninteractive \
    && apt -y install --no-install-recommends libsm6 libxext6 libssl-dev libffi-dev libxml2-dev libxslt1-dev zlib1g-dev ffmpeg exiftool
