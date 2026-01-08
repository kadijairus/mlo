# Start from the same consistent base image
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS base

# Install necessary system build tools
RUN apt update && \
    apt install --no-install-recommends -y build-essential gcc && \
    apt clean && rm -rf /var/lib/apt/lists/*

# Set a working directory inside the container
WORKDIR /app

# Copy the dependency definition files
COPY uv.lock uv.lock
COPY pyproject.toml pyproject.toml

# Install all Python dependencies from the lock file
# This ensures a reproducible environment
RUN uv sync --locked --no-cache --no-install-project \
    --extra-index-url https://download.pytorch.org/whl/cpu \
    --index-strategy unsafe-best-match

# Copy your source code into the container
COPY src/ /app/src

# --- IMPORTANT ---
# Copy the PROCESSED TEST DATA into the image.
# Your evaluate.py script depends on this data being at a fixed location.
# This makes the evaluation image self-contained and reproducible.
COPY data/processed/ /app/data/processed/

# The command to run when the container starts.
# It calls your evaluate script as a module.
# The model checkpoint path will be passed as an argument to this command.
ENTRYPOINT ["uv", "run", "python", "-m", "src.mlo_model.evaluate"]