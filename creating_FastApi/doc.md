## FastAPi
FastAPI literally describes what it is: a "Fast" framework for building "Application Programming Interfaces" (APIs).

-   Application: A software program or app.
-   Programming: The code used to build software
-   Interface: The bridge that allows two applications to talk to each other.
`FastAPI, which is a modern, fast web framework for building APIs with Python.`

# Writing the FastAPI Application
*app.py content is our entire API application*

This FastAPI application provides several useful endpoints:

GET /: Basic health check
POST /predict: Make a single prediction
POST /predict-batch: Make multiple predictions at once
GET /model-info: Get information about the model

# stop/remove/build/run a container
- docker stop diabetes-api-container
- docker rm diabetes-api-container
- docker build -t diabetes-api .
- docker run --name diabetes-api-container -p 8000:8000 diabetes-api

# Saving and Sharing Your Containers
Understanding Container Distribution Methods
There are several ways to save and share containers:

Save as archive files (.tar) for local sharing or backup
Push to Docker Hub for public sharing
# Save your ML training environment
docker save my-ml-environment:latest -o ml-training-env.tar

# Save your API deployment container
docker save diabetes-api:latest -o diabetes-api.tar
These commands create .tar files that contain everything needed to recreate your containers. 
# To load these containers on another machine:
# Load the ML training environment
docker load -i ml-training-env.tar

# Load the API container
docker load -i diabetes-api.tar
Let's test this process. First, remove one of your images, then reload it:

# Remove the image (don't worry, we'll get it back)
docker rmi -f diabetes-api:latest

# Verify it's gone
docker images

# Load it back from the archive
docker load -i diabetes-api.tar

# Verify it's back
docker images

# The work follow : 
Use this order instead:

Build the image
docker build -t diabetes-api .
Save it to a tar file
docker save -o diabetes-api.tar diabetes-api:latest
Remove the image
docker rmi -f diabetes-api:latest
Load it back
docker load -i diabetes-api.tar
# Method 2: Sharing via Docker Hub (Public Registry)
hub.docker.com
Tagging Images for Docker Hub
Before pushing to Docker Hub, you need to tag your images with your username. The format is {your_username}/repository-name:tag.

# Setting Up Docker Hub
Once you have an account, log in from your terminal:

`docker login`
Enter your Docker Hub username and password when prompted and submit the browser device code at https://login.docker.com/activate if prompted.
# Tag your ML training environment
rbashiri1974
docker tag my-ml-environment:latest {yourusername}/ml-diabetes-training:v1.0
docker tag my-ml-environment:latest rbashiri1974/ml-diabetes-training:v1.0


# Tag your API container
docker tag diabetes-api:latest {yourusername}/diabetes-prediction-
docker tag diabetes-api:latest rbashiri1974/ml-diabetes-training:v1.0
# Pushing to Docker Hub
Now you can share your containers with the world:

# Push the ML training environment
docker push rbashiri1974/ml-diabetes-training:v1.0

# Push the API container
docker push rbashiri1974/diabetes-prediction-api:v1.0

# Creating Repository Documentation:
Documenting your containers is a good practice. To that end, on Docker Hub, you can add README files to explain all of the following:

What the container does
How to run it
What ports it uses
Example commands
Requirements or dependencies
# Creating a Shared Development Environment
Let's create a practical example of sharing your development setup. Create a new file called team-setup.md in your ds-project folder: