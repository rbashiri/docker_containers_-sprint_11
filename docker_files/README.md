# Project description
This repository documents my learning and practical exercises with Docker and containerization as part of the TripleTen Data Science Bootcamp. It includes Dockerfiles, image-building commands, container management, port mapping, dependency installation, and examples of packaging Python and machine-learning applications into reproducible environments.

## Containers:
    Containers offer a more efficient way to package and run your applications with all their dependencies. 

    Each container is a standardized package that can hold any application and its dependencies.
**How containers work:**
 They share the core part of an operating system (called the "kernel") but run in completely isolated environments.

## Docker: 
   The container management system is called `Docker`. Docker serves as the management layer between containers and the host operating system. 

# Understanding  Project Files

* `app.py` is  main Python application code. This is where the actual logic of program lives. 

*  `requirements.txt`file lists all the external Python packages your project needs to run.

* `README.md` serves as the front page of  project. It's written in Markdown format (that's what the .md extension means) and typically explains what your project does, how to install it, and how to use it. 

* `.gitignore`: file tells Git which files to ignore when tracking changes. Files that start with a dot are hidden by default on many systems.

### Docker Terminology:
* A Docker host is `a computer (such as yours)` on which Docker is installed.

* `A Docker daemon` is a program that serves as a `runtime environment` for Docker containers. It starts containers, provides them with the required resources, and controls their operation.
* A Docker client is a program that passes user commands to the Docker daemon. The client can be a command line or a graphical interface.
### Docker installation
1- install docker desktop
2- install docker in venv: 
    - sudo apt update
    - sudo apt install curl  ( a package we need)
    docker --version
docker compose version
sudo systemctl status docker
docker run hello-world
## Docker Hub 
 ### Pull Process:
    When you "pull" an image from Docker Hub, you're downloading the container image to your local computer. 
    
 TEST DOCKER
  Run this code: `docker pull hello-world`
 *Using default tag: latest: Docker images can have different versions, called "tags." When you don't specify a version, Docker automatically uses "latest," which is typically the most recent stable version.*

*latest: Pulling from library/hello-world: This confirms Docker is downloading the hello-world image from the official library on Docker Hub.*

*c1ec31eb5944: Pull complete: This cryptic string is the ID of an image layer. The hello-world container is so simple it only has one layer, which is now downloaded.*

*Digest: sha256:...: This is a unique fingerprint for this exact version of the image, ensuring you got the authentic, unmodified version.*

*Status: Downloaded newer image: Confirms the download was successful.*

*docker.io/library/hello-world:latest: This is the full name of what you just downloaded. "docker.io" is Docker Hub's official registry, "library" indicates it's an official image, and "hello-world" is the image name.*

### Viewing downloaded images : Having image on your computer
    By :docker images
### Running Your First Container :
Having the image on your computer is just the first step. Now let's actually run it:
 `Run this:` docker run hello-world
### Pulling a More Practical Image
   `Run this:` docker pull nginx
*Note* : nginx (pronounced "engine-x") is a popular web server. This download will take longer than hello-world because it's a more complete application.

 To check the image: docker images
 ### To pull specific version
 docker pull nginx:alpine  `add the tag after a colon:`
 ### Remove images which no longer needed
 docker rmi  -f hello-world
 ### Search for removed images 
docker search python

## Running Containers in the Background
Earlier, when we ran nginx, it took over our terminal. Most of the time, you want containers to run in the background. You can do this with the -d flag (which stands for "detached"):`docker run -d nginx`
This will start nginx in the background and return you to your command prompt. You'll see a long string of characters (this is the container ID).

*To see the currently running containers, use this command:* docker ps
docker ps = show running containers
docker ps -a = show all containers (running + stopped)

# To stop a running container:
docker stop `id number`

## Understanding the Docker Run Command Structure
Before diving into specific arguments, let's understand the basic structure of the docker run command:

docker run [OPTIONS] IMAGE [COMMAND] [ARGUMENTS]
docker run: The base command
[OPTIONS]: Various flags that modify how the container runs (this is what we'll focus on)
IMAGE: The Docker image you want to run
[COMMAND]: An optional command to run inside the container
[ARGUMENTS]: Arguments for that command
For example:

docker run -d -p 8080:80 --name my-web nginx

#### The p or -publish Flag
The basic syntax for port mapping is as follows:
`docker run -p HOST_PORT:CONTAINER_PORT image`

### Interactive Mode: The it Flags
#### Understanding i and t
These are actually two separate flags that are commonly used together:

i or -interactive: Keeps the standard input (STDIN) open, allowing you to send input to the container.
t or -tty: Allocates a pseudo-terminal (TTY), which makes the interaction feel like a normal terminal session.
Using Interactive Mode
Running a shell in a container:

`docker run -it ubuntu bash`

Now you can run any Linux commands inside the container:

ls
pwd
whoami
apt update
apt install curl
To exit the container, type exit or press Ctrl+D.

### Automatic Cleanup: The --rm Flag
When to Use --rm
Use --rm for:

One-time tasks and testing
Temporary containers you don't need to keep
Development and experimentation
Scripts that run containers
Don't use --rm for:

Containers with important data
Services you might want to restart
Containers you need to debug later
Production services
Let’s look at this common pattern for testing:  docker run -it --rm ubuntu bash , donot use it 

Used --memory and --cpus to prevent a container from consuming too many system resources.
Learned how restart policies improve application reliability:
always: restart whenever possible.
unless-stopped: restart except after a manual stop.
on-failure: restart only after an error.
no: do not restart automatically.
Used -w or --workdir to select where commands run inside a container.
Used -h or --hostname to give a container an identifiable hostname.
Used --user to run an application without root privileges for better security.
Combined ports, resource limits, restart policies, and other options in one command.
Learned that Docker images define what an application contains, while docker run options control how its container operates.
Application to This Project

For my battery RUL application, I can limit its resources, expose the Streamlit port, and configure automatic restarting:

`docker run -d \
  --name battery-rul-app \
  --restart=unless-stopped \
  -p 8501:8501 \
  --memory=1g \
  --cpus=1 \
  battery-rul-app:latest`
  This command:

Runs the application in the background.
maps port 8501 from the computer to the container.
Limits the container to 1 GB of memory and one CPU core.
Restarts it after a failure or system reboot, unless I intentionally stop it.

