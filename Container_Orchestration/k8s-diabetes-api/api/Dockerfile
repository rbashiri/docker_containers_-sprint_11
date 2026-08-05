# Use a lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

## Copy our requirements file into the container
COPY api/requirements.txt /tmp/requirements.txt

# Install our Python libraries
USER root
RUN pip install --no-cache-dir --upgrade pip && \
	pip install --no-cache-dir -r /tmp/requirements.txt
# Reads package names from requirements.txt and installs them without keeping pip cache files.

# Create and prepare a susan user home/work directory.
RUN useradd -m -s /bin/bash susan && \
	mkdir -p /home/susan/work && \
	mkdir -p /home/susan/.local/share/jupyter/runtime && \
	chown -R susan:susan /home/susan

# Run as susan in the susan workspace.
ENV HOME=/home/susan
ENV JUPYTER_RUNTIME_DIR=/home/susan/.local/share/jupyter/runtime
USER susan
WORKDIR /home/susan/work

# Copy API code and model artifacts into the runtime workspace.
COPY --chown=susan:susan api/app.py ./
COPY --chown=susan:susan models/ ./models/

# FastAPI default port.
EXPOSE 8000

# Start the API server.
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]