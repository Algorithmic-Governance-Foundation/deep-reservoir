# Use Ubuntu 22.04 LTS as base image
FROM ubuntu:22.04

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# Update package list and install essential packages
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    vim \
    nano \
    build-essential \
    software-properties-common \
    apt-transport-https \
    ca-certificates \
    gnupg \
    lsb-release \
    sudo \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user with sudo privileges
ARG USERNAME=dev
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Install Node.js (LTS version)
RUN curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash - \
    && apt-get install -y nodejs

# Install Claude Code globally
RUN npm install -g @anthropic-ai/claude-code

# Create workspace and config directories and set permissions
RUN mkdir -p /workspaces /home/$USERNAME/.claude && \
    chown -R $USERNAME:$USERNAME /workspaces /home/$USERNAME/.claude /usr/lib/node_modules

# Set working directory
WORKDIR /workspaces

# Switch to non-root user
USER $USERNAME

# Install uv (fast Python package manager) for the dev user
RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
    && echo "export PATH=\"/home/$USERNAME/.local/bin:\$PATH\"" >> /home/$USERNAME/.bashrc

# Set up a pretty shell prompt
RUN echo "export PS1=\"\\[\\033[01;32m\\]\\u\\[\\033[00m\\]:\\[\\033[01;34m\\]\\w\\[\\033[00m\\]\\$ \"" >> /home/$USERNAME/.bashrc \
    && echo 'alias ll="ls -alF"' >> /home/$USERNAME/.bashrc \
    && echo 'alias la="ls -A"' >> /home/$USERNAME/.bashrc \
    && echo 'alias l="ls -CF"' >> /home/$USERNAME/.bashrc

# Set default shell to bash
SHELL ["/bin/bash", "-c"]