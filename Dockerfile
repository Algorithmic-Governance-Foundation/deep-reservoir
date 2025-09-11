# Install uv
FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Create user early to avoid chown issues
RUN useradd -m -u 1000 user

# Set environment variables for user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Change the working directory to the user's home app directory
WORKDIR $HOME/app

# Switch to user before any file operations
USER user

# Create cache directory for user
RUN mkdir -p /home/user/.cache/uv

# Install dependencies
RUN --mount=type=cache,target=/home/user/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project

# Copy the project into the image with proper ownership
COPY --chown=user:user . .

# Sync the project
RUN uv sync --locked

# This is so jank but I can't think of an easier way
# References:
# https://huggingface.co/docs/hub/en/spaces-sdks-docker#buildtime
# https://docs.astral.sh/uv/concepts/configuration-files/#env
RUN --mount=type=secret,id=PERPLEXITY_API_KEY,mode=0444,required=true \
    --mount=type=secret,id=OPENAI_API_KEY,mode=0444,required=true \
    --mount=type=secret,id=GRADIO_PASSWORD,mode=0444,required=true \
    echo "PERPLEXITY_API_KEY=$(cat /run/secrets/PERPLEXITY_API_KEY)" > .env && \
    echo "OPENAI_API_KEY=$(cat /run/secrets/OPENAI_API_KEY)" >> .env && \
    echo "GRADIO_PASSWORD=$(cat /run/secrets/GRADIO_PASSWORD)" >> .env

ENV GRADIO_SERVER_NAME="0.0.0.0"

EXPOSE 7860

CMD ["uv", "run", "gradio-reservoir"]