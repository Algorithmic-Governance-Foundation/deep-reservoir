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

### Method 2: Docker (w/ vscode)
This will give you a full environment setup with `uv`, and [`claude-code`](https://www.anthropic.com/claude-code) installed

1. Have Docker or Docker Desktop Installed
2. Use vscode
3. CTRL + SHIFT + P and run `Dev Containers: Rebuild and Reopen in Container`
4. You should now have a fully set up environment, no other installations requried
5. `uv run deep-reservoir` to run the application


<!-- ## Installation

1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/)
2. Run `uv build --wheel`
3. Try `uv tool install ./dist/deep_reservoir-0.1.0-py3-none-any.whl`
4. If you see a warning about `PATH` run the recommended command: `uv tool update-shell`
5. You should now be able to run `deep-reservoir`

Note there's also `pip install -e .` as an option too for installing.
-->


