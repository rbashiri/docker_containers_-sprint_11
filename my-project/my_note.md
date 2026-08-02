## step 1: Create folders 
# step 2 pull container from existing image
Pull = optional if image already exists
# step 3 Running Your Jupyter Container
Run = required to use it
`docker run --name ml-jupyter -p 8888:8888 -v ~/home/susan/Docker_sprint_11/my-project:/home/jovyan/work jupyter/base-notebook:x86_64-python-3.11`

# Step 4 : Adding code inside docker file:

 *Start with the base Jupyter image we used before*
FROM jupyter/base-notebook:x86_64-python-3.11

# *Copy our requirements file into the container*
COPY requirements.txt /tmp/requirements.txt

# *Install our Python libraries*
USER root
RUN pip install --no-cache-dir --upgrade pip && \
	pip install --no-cache-dir -r /tmp/requirements.txt
#*Reads package names from requirements.txt and installs them without keeping pip cache files.*

# *Create and prepare a susan user home/work directory*.
RUN useradd -m -s /bin/bash susan && \
	mkdir -p /home/susan/work && \
	mkdir -p /home/susan/.local/share/jupyter/runtime && \
	chown -R susan:susan /home/susan

# *Run as susan in the susan workspace.*
ENV HOME=/home/susan
ENV JUPYTER_RUNTIME_DIR=/home/susan/.local/share/jupyter/runtime
USER susan
WORKDIR /home/susan/work


# Step 5  build our custom image
stop and remove it 
docker stop ml-jupyter
docker rm ml-jupyter
docker run --name ml-jupyter2 -p 8888:8888 -v /home/susan/Docker_sprint_11/my-project:/home/jovyan/work jupyter/base-notebook:x86_64-python-3.11
`docker build -t my-ml-environment .` t stand for tage
# Step 6 Running Your Custom Container
docker run --name my-ml-project -p 8888:8888 -v "{your_file_path}:/home/jovyan/work" my-ml-environment

docker run --name my-ml-project -p 8888:8888 -v /home/susan/Docker_sprint_11/my-project:/home/jovyan/work my-ml-environment