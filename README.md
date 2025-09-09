---
title: Deep Reservoir
emoji: 🏛️
colorFrom: blue
colorTo: purple
sdk: docker
app_file: app.py
app_port: 7860
---

# Deep Reservoir

A CLI Tool for researching policies

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
Comes with [Claude Code (paid)](https://www.anthropic.com/claude-code) and [Gemini CLI (free)](https://google-gemini.github.io/gemini-cli/) as terminal assistants.

1. Have Docker or Docker Desktop Installed
2. Use vscode
3. CTRL + SHIFT + P and run `Dev Containers: Rebuild and Reopen in Container`
4. You should now have a fully set up environment, no other installations required
5. `uv run deep-reservoir` to run the application


## Installation (TODO)

### Via pip
You might be able to `pip install -e .` as an option too for installing. 

### Via uv
1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/)
2. Run `uv build --wheel`
3. Try `uv tool install ./dist/deep_reservoir-0.1.0-py3-none-any.whl`
4. If you see a warning about `PATH` run the recommended command: `uv tool update-shell`
5. You should now be able to run `deep-reservoir`


## Deploying to Hugging Spaces

We need an `app.py`

Also run `uv pip compile pyproject.toml -o requirements.txt` to generate a `requirements.txt`

