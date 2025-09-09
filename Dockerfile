# Install uv
FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Change the working directory to the `app` directory
WORKDIR /app

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project

# Copy the project into the image
ADD . /app

# Sync the project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

# Set environment variables from Hugging Face secrets
RUN --mount=type=secret,id=PERPLEXITY_API_KEY,mode=0444,required=true \
    --mount=type=secret,id=OPENAI_API_KEY,mode=0444,required=true \
    --mount=type=secret,id=GRADIO_PASSWORD,mode=0444,required=true \
    export PERPLEXITY_API_KEY=$(cat /run/secrets/PERPLEXITY_API_KEY) && \
    export OPENAI_API_KEY=$(cat /run/secrets/OPENAI_API_KEY) && \
    export GRADIO_PASSWORD=$(cat /run/secrets/GRADIO_PASSWORD) && \
    uv run gradio-reservoir