# Diabetes ML Project - Personal Notes

## Goal

Use this page as a simple reminder for my real project folder: `my-project`.

## My Docker Hub Username

Replace `yourusername` with my real Docker Hub username.

## Training Environment

```bash
docker pull rbashiri1974/ml-diabetes-training:v1.0
mkdir -p ~/my-project
docker run --name my-diabetes-work \
	-p 8000:8000 \
	-v ~/my-project:/home/jovyan/work \
	rbashiri1974/ml-diabetes-training:v1.0
```

## What These Parts Mean

- `~/my-project` is my local folder.
- `-p 8888:8888` is for Jupyter Lab.
- `-v ~/my-project:/home/jovyan/work` shares my files with the container.
- `yourusername/ml-diabetes-training:v1.0` is the image name I must replace with my own Docker Hub username.

## Reminder

`8888:8888` is for the training/Jupyter notebook flow.
If I only want the FastAPI app, I should use port `8000:8000` instead.