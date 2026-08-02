# Example for Your Case
## 0. Clean old containers from previous tries
Run:
`docker rm -f ml-jupyter my-ml-project my-ml-project-2 2>/dev/null || true`
## 1. Pull the image
Run:
`docker pull jupyter/base-notebook:x86_64-python-3.11`

## 2. Find where Docker saved it
Run:
`docker info | grep "Docker Root Dir"`

Example output on Linux:
`Docker Root Dir: /var/lib/docker`

This means Docker stores downloaded images under:
`/var/lib/docker`

## 3. Verify your image exists
Run:
`docker images | grep jupyter/base-notebook`

If you see `jupyter/base-notebook` with tag `x86_64-python-3.11`, the pull was successful.

## 4. (Optional) Get full details of this image
Run:
`docker image inspect jupyter/base-notebook:x86_64-python-3.11`

## 5. Running Jupyter container

Before running it, move to your project folder:
`cd /home/susan/Docker_sprint_11/docker_files/docker_ml_application`
Use this command (recommended):
`docker run -p 8888:8888 -v "$(pwd)":/home/jovyan/work jupyter/base-notebook:x86_64-python-3.11`


What this means:
- `-p 8888:8888` maps Jupyter port to your machine.
- `-v "$(pwd)":/home/jovyan/work` shares your current folder with the container.
- `jupyter/base-notebook:x86_64-python-3.11` is the image name and tag.

After the container starts, open the URL shown in terminal (usually `http://127.0.0.1:8888/...`).

If you prefer absolute path instead of `$(pwd)`, use:
`docker run -p 8888:8888 -v /home/susan/Docker_sprint_11/docker_files/docker_ml_application:/home/jovyan/work jupyter/base-notebook:x86_64-python-3.11`

# Buliding custom Ds_project container :
####   Structure the folder in the following way: 

ds-project/
├── Dockerfile
├── requirements.txt
├── data/
├── notebooks/
└── models/
# repo is short for repository.



# Dockerfile Notes for ds_project

## Current Dockerfile

```dockerfile
# Start with the base Jupyter image we used before
FROM jupyter/base-notebook:x86_64-python-3.11

# Copy our requirements file into the container
COPY requirements.txt /tmp/requirements.txt

# Install our Python libraries
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Set the working directory
WORKDIR /home/jovyan/work
```

## What each line means

### FROM jupyter/base-notebook:x86_64-python-3.11
Uses a prebuilt Jupyter image as the starting point.

### COPY requirements.txt /tmp/requirements.txt
Copies requirements.txt from your project folder into the container.
- Source path: requirements.txt
- Destination path: /tmp/requirements.txt

### What /tmp means
/tmp is a temporary directory inside the container filesystem. It is commonly used as a temporary place to copy install files.

### RUN pip install --no-cache-dir -r /tmp/requirements.txt
Installs Python packages listed in requirements.txt.
- -r reads package names from the file.
- --no-cache-dir avoids keeping pip cache, which helps keep image size smaller.

### WORKDIR /home/jovyan/work
Sets the default working directory inside the container.
This works like setting a permanent cd for the next Dockerfile steps and when opening a shell.

## Why jovyan appears in the path
The base image jupyter/base-notebook uses a default non-root user named jovyan, with home directory /home/jovyan.

## Common errors to avoid
- Wrong image tag formatting:
  - Wrong: FROM jupyter/base-notebook: x86_64-python-3.11
  - Correct: FROM jupyter/base-notebook:x86_64-python-3.11
- Incomplete COPY command:
  - Wrong: COPY requirements.txt
  - Correct: COPY requirements.txt /tmp/requirements.txt

## If you create your own project Dockerfile (root-based)

```dockerfile
FROM python:3.11-slim

USER root
WORKDIR /app

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
# Create susan user and home/work directory
RUN useradd -m -s /bin/bash susan && \
    mkdir -p /home/susan/work && \
    chown -R susan:susan /home/susan

# Switch to susan
USER susan
WORKDIR /home/susan/work

COPY . /app
CMD ["python", "app.py"]
```

Build and run example:

```bash
docker build -t my-project .
docker run --rm -p 8000:8000 my-project
```

Security note: root works, but best practice is to run app as a non-root user when possible.

## Build command note (important)

If you are already inside the ds_project folder, use:

```bash
docker build -f Dockerfile.db -t ds-db .
```

Why the dot matters:
- The last argument is the build context.
- `.` means use the current folder as context.

Common mistake:
- Running `docker build -f Dockerfile.db ds_project -t ds-db` while already in ds_project.
- This makes Docker look for `ds_project/ds_project`, which does not exist.

Equivalent command from the parent folder (`Docker_sprint_11`):

```bash
docker build -f ds_project/Dockerfile.db -t ds-db ds_project
```
