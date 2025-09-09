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
RUN --mount=type=secret,id=perplexity_api_key,mode=0444,required=true \
    --mount=type=secret,id=openai_api_key,mode=0444,required=true \
    --mount=type=secret,id=gradio_password,mode=0444,required=true \
    echo "PERPLEXITY_API_KEY=$(cat /run/secrets/perplexity_api_key)" > .env && \
    echo "OPENAI_API_KEY=$(cat /run/secrets/openai_api_key)" >> .env && \
    echo "GRADIO_PASSWORD=$(cat /run/secrets/gradio_password)" >> .env

RUN uv run gradio-reservoir