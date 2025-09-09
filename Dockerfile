FROM python:3.12-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Create user with ID 1000 for HF Spaces compatibility
RUN useradd -m -u 1000 user
USER user

# Set environment variables
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Set working directory
WORKDIR $HOME/app

# Copy dependency files with proper ownership
COPY --chown=user pyproject.toml uv.lock ./

# Install dependencies (excluding the project itself for better caching)
RUN --mount=type=cache,target=/home/user/.cache/uv \
    uv sync --locked --no-install-project

# Copy the rest of the project
COPY --chown=user . .

# Install the project
RUN --mount=type=cache,target=/home/user/.cache/uv \
    uv sync --locked

# Expose the required port for HF Spaces
EXPOSE 7860

# Use CMD instead of RUN for application startup
CMD ["uv", "run", "gradio-reservoir"]