# Start with the base Jupyter image we used before
FROM jupyter/base-notebook:x86_64-python-3.11

# Copy our requirements file into the container
COPY requirements.txt /tmp/requirements.txt

# Install our Python libraries
USER root
RUN pip install --no-cache-dir --upgrade pip && \
	pip install --no-cache-dir -r /tmp/requirements.txt
# Reads package names from requirements.txt and installs them without keeping pip cache files.

# Use the base image default unprivileged user and workspace path.
USER jovyan
WORKDIR /home/jovyan/work