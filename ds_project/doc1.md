# .gitkeep
*.gitkeep should be created in data , notebooks, model*
`.gitkeep is a placeholder file to keep an empty folder in Git.`

*Why needed:*
* it tracks files, not empty directories.
* If a folder has no files, Git ignores it.
* Adding .gitkeep makes the folder non-empty, so Git can track it.

`In current case:`

data/.gitkeep keeps the data folder structure.
notebooks/.gitkeep keeps the notebooks folder structure.

===============================================================================================
**Step 1: Go into your new clean folder and add requirment**
`Remember add .venv-clean`
Clean method you can reuse

1- Start from a fresh environment
    cd /home/susan/Docker_sprint_11/rep_ds_project
    python -m venv .venv-clean
    source .venv-clean/bin/activate
    python -m pip install --upgrade pip

2- Install only the libraries you really need

    pip install pandas scikit-learn numpy matplotlib seaborn jupyter jupyterlab joblib
===========================================================================================    

# Step 2: Add requirements manually
##  Export professional requirements files
Keep only top-level packages (recommended)
Run:
python -m pip install pip-chill
pip-chill > requirements.in
This avoids dumping every transitive dependency.

Generate from imports instead of environment
Run:
python -m pip install pipreqs
pipreqs . --force

4- Verify dependency health
pip check

===============================================================================================
Step 3: Add Dockerfile manually
Open Dockerfile and paste:

FROM jupyter/base-notebook:x86_64-python-3.11
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
WORKDIR /home/jovyan/work
===============================================================================================
Step 4: Build image
Command:
docker build -t rep-ml-environment .
===============================================================================================
Step 5: Run container
Command:
docker rm -f rep-ml-project 2>/dev/null || true
docker run --name rep-ml-project -p 8888:8888 -v "$(pwd)":/home/jovyan/work rep-ml-environment
==============================================================================================
Step 6: Open Jupyter
Copy the URL from terminal that starts with:
http://127.0.0.1:8888/lab?token=

========================================================================================
# In the previous lesson we run prerebuilt image directly
# in the new lesson we try to bulid our own images first and the run it 
#  It is teaching the transition from “user of image” to “builder of image.”