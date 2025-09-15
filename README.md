---
title: Deep Reservoir
emoji: 🏛️
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
---

# Deep Reservoir

A LLM powered tool for researching policies

## Running
1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/)
2. Put in `countries.csv` and `policies.csv` inside `/inputs/`
3. Run `uv run deep-reservoir`
4. The results should be found at `/results/output.csv`

## Developing

All the code can be found within `/src/`.
Inputs are at `/inputs/`
Outputs are at `/results/`

### Method 1: Standard
1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/)
2. You can run the application via `uv run deep-reservoir`

### Method 2: Docker Devcontainers (w/ vscode)
[Devcontainer](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) setup for easily reproducible dev environments.
Comes with [Claude Code](https://www.anthropic.com/claude-code) and some default extensions.

1. Have Docker or Docker Desktop Installed
2. Use vscode
3. CTRL + SHIFT + P and run `Dev Containers: Rebuild and Reopen in Container`
4. You should now have a fully set up environment, no other installations required
5. `uv run deep-reservoir` or `uv run gradio-reservoir` to run the application


## Installation (TODO)

### Via pip
You might be able to `pip install -e .` as an option too for installing. 

### Via uv
1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/)
2. Run `uv build --wheel`
3. Try `uv tool install ./dist/deep_reservoir-0.1.0-py3-none-any.whl`
4. If you see a warning about `PATH` run the recommended command: `uv tool update-shell`
5. You should now be able to run `deep-reservoir` from anywhere in any terminal


## Deploying to Hugging Spaces

We're using the Dockerfile to set up the Gradio App.

