# Role: Start from an image containing Python 3.11

FROM python:3.11-slim

# Role: Set /app as the working directory inside the image
WORKDIR /app

# Role: Copy the dependency list into the image
COPY requirements.txt .

# Role: Install the Python packages
RUN pip install -r requirements.txt

# Role: Copy the Flask application into the image
COPY app.py .

# Role: Start the application when the container runs
CMD ["python", "app.py"]