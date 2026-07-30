Docker Build Command
docker build -t flask-app .
docker build: Builds a Docker image.
-t flask-app: Names/tags the image flask-app.
.: Uses the current directory as the build context and looks there for the Dockerfile.

Main takeaway: 
This command builds a Docker image named flask-app using the Dockerfile and project 
files in the current folder. Note that flask-app is the image name, 
not the container name.
## docker run -d -p 5000:5000 --name my-flask-app flask-app ##
docker run tells Docker to create and start a container from an image
-d runs the container in "detached" mode, meaning it runs in the background
p 5000:5000 maps ports between your computer and the container
--name my-flask-app gives your running container a specific name
flask-app is the name of the image you built in the previous lesson.
## 
Verifying Your Container Is Running
To confirm your container is actually running, use the docker ps command:

# docker ps

# Accessing Your Flask API
Your Flask application is now running and accessible. 
Open your web browser and navigate to http://localhost:5000.
 You should see a JSON response like this:
 Viewing Container Logs
Even though your container runs in detached mode, it still generates logs. These logs show you what's happening inside the container such as Flask's startup messages, request logs,
 errors, and so on. To view your container's logs, run:
 docker logs my-flask-app
## Starting a Stopped Container
 docker start my-flask-app
This starts the existing container with all the same settings you used before. Check docker ps and you'll see it running again. Visit localhost:5000 and your API will respond again.

The difference between docker run and docker start is as follows:

docker run creates a new container from an image
docker start restarts an existing container that was stopped

Removing a Container
If you want to completely remove a container (not just stop it), first make sure it's stopped, then run:

docker rm -f my-flask-app
This deletes the container entirely.
 If you want to run a container again after removing it, you'll need to use docker run to create a new one from your image. The image itself (flask-app) still exists, you only removed the running container instance.