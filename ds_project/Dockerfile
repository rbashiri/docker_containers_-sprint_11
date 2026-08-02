# Start with the base Jupyter image we used before
FROM jupyter/base-notebook:x86_64-python-3.11

# Copy our requirements file into the container
COPY requirements.txt /tmp/requirements.txt

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