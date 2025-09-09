# Install uv
FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Change the working directory to the `app` directory
WORKDIR /app

# For devmode
RUN useradd -m -u 1000 user

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

# This is so jank but I can't think of an easier way
RUN --mount=type=secret,id=PERPLEXITY_API_KEY,mode=0444,required=true \
    --mount=type=secret,id=OPENAI_API_KEY,mode=0444,required=true \
    --mount=type=secret,id=GRADIO_PASSWORD,mode=0444,required=true \
    echo "PERPLEXITY_API_KEY=$(cat /run/secrets/PERPLEXITY_API_KEY)" > .env && \
    echo "OPENAI_API_KEY=$(cat /run/secrets/OPENAI_API_KEY)" >> .env && \
    echo "GRADIO_PASSWORD=$(cat /run/secrets/GRADIO_PASSWORD)" >> .env

RUN uv run gradio-reservoir