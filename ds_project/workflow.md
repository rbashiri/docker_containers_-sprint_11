# Practical Docker Workflow for Practice

This is a simple, repeatable workflow for your own machine.
Use this guide instead of mixing lesson commands from different folders.

## 1) Keep one active folder
Active folder:
- ds_project/

Main files:
- Dockerfile
- requirements.txt
- data_db/
- model_db/
- notebook_db/

## 2) One-time cleanup when confused
Run from /home/susan/Docker_sprint_11:

    docker ps -a
    docker rm -f my-ml-project my-ml-project-2 2>/dev/null || true

Optional full cleanup of stopped containers only:

    docker container prune -f

## 3) Naming standard for your own practice
Use the same names every time:
- Image: my-ml-environment
- Container: my-ml-project

This avoids duplicate and conflicting names.

## 4) Build workflow
From project folder:

    cd /home/susan/Docker_sprint_11/ds_project
    docker build -t my-ml-environment .

Notes:
- The dot at the end means current folder is the build context.
- If Dockerfile is not found, build from parent with explicit path:

    cd /home/susan/Docker_sprint_11
    docker build -f ds_project/Dockerfile -t my-ml-environment ds_project

## 5) Run workflow
Start Jupyter:

    cd /home/susan/Docker_sprint_11/ds_project
    docker run --name my-ml-project -p 8888:8888 -v "$(pwd)":/home/susan/work my-ml-environment

If name conflict appears:

    docker rm -f my-ml-project
    docker run --name my-ml-project -p 8888:8888 -v "$(pwd)":/home/susan/work my-ml-environment

## 6) Verify container state
Running containers:

    docker ps

See this specific container:

    docker ps -a -f name=my-ml-project

Check logs:

    docker logs my-ml-project

## 7) Stop and restart
Stop:

    docker stop my-ml-project

Start same container again:

    docker start -ai my-ml-project

## 8) Requirements troubleshooting
If build fails with No matching distribution found:
- A pinned version is not available for Python 3.11 in the base image.

Check available versions:

    python -m pip index versions PACKAGE_NAME

Then edit requirements.txt to a compatible version and rebuild.

## 9) Keep empty folders in Git
Add these files once:

    touch data_db/.gitkeep model_db/.gitkeep notebook_db/.gitkeep

## 10) Daily quick sequence

    cd /home/susan/Docker_sprint_11/ds_project
    docker build -t my-ml-environment .
    docker rm -f my-ml-project 2>/dev/null || true
    docker run --name my-ml-project -p 8888:8888 -v "$(pwd)":/home/susan/work my-ml-environment
