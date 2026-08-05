# What is Docker Compose?
Docker Compose is like the conductor leading an orchestra. Instead of individually telling each musician (container) when to play, the conductor (Docker Compose) coordinates them all using sheet music (a YAML file).
## Main idea
Docker Compose starts and connects several containers using one YAML file.

*The most important point is:*

From your computer, the application is `localhost:5000`.
From inside the app container, PostgreSQL is `database:5432`.
database works because it is the service name in the Compose file. Compose automatically creates a network and lets services find each other by service name. Docker Compose networking

### 1. Why use multiple containers?

Each container has one main responsibility:

| Container                 | Responsibility                    |
| ------------------------- | --------------------------------- |
| `app`                     | Runs the Flask application        |
| `database`                | Stores data with PostgreSQL       |
| Possible future container | Frontend, cache, monitoring, etc. |

## A useful comparison:

Dockerfile describes how to build one image.
compose.yaml describes how multiple services work together.

3. Understanding YAML

This example defines one service:

# Role: Define all containers managed by Compose
services:

  # Role: Name this service "hello"
  hello:

#  Role: Create the container from the hello-world image
    image: hello-world

Important YAML rules:

Indentation controls structure.
Use spaces, not tabs.
key: value represents a setting.
A dash - represents an item in a list.

You can keep multiple YAML Compose files in the same folder.

Common pattern:

Keep original file, for example: docker-compose.yml
Add lesson file, for example: docker-compose.lesson.yml
How to run especific file
docker compose -f docker-compose.yml up
docker compose -f docker-compose.lesson.yml up

# To see which Compose projects are running:
docker compose ls
# stop /rm/ check
docker stop `ports`   
docker rm `ports`
docker ps

# # Role: Define all containers managed by Compose
  # Role: Name this service "hello"
services:
  hello:
    image: hello-world
 # Role: Create the container from the hello-world image

 adding the scond docker:
  services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"

  database:
    image: postgres:15
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432 

# Run 
`docker-compose up`
### Connecting to Your Database

# Run
# Connect to the running database container
docker-compose exec database psql -U user -d myapp
The parts mean:

docker-compose exec: run a command inside a running Compose container.
database: the service name in docker-compose.yml.
psql: open PostgreSQL’s command line.
-U user: connect as the user named user.
-d myapp: connect to the database named myapp.

What does Docker Compose do?

Your answer is almost correct:

Docker Compose manages and connects several containers.

For example:

One container runs your Python prediction application.
Another container runs PostgreSQL.
Docker Compose starts both using one command.
# Role: Build and start all services in docker-compose.yml
docker-compose up --build
2. How do you define multiple services?

Multiple services are defined inside docker-compose.yml, not by creating app.py.

# Role: Define the containers required by the project
services:

  # Role: Define the PostgreSQL container
  database:
    image: postgres:15

  # Role: Define the Python application container
  app:
    build: ./app

Here, there are two services:

database
app

app.py contains your Python application logic. It does not create or connect the containers.

3. How do ports connect your computer to a container?

Ports are mapped in docker-compose.yml.

# Role: Connect computer port 5000 to app-container port 5000
ports:
  - "5000:5000"

The format is:

computer port : container port

The complete connection is:

Browser → localhost:5000 → app container:5000

Inside app.py, this line makes Flask listen on container port 5000:

# Role: Start Flask on port 5000 inside the container
app.run(host="0.0.0.0", port=5000, debug=True)

Therefore:

app.py tells Flask which internal port to use.
docker-compose.yml connects your computer to that port.
4. How do containers communicate using service names?

The application uses the database service name as the hostname:

# Role: Identify the database container by its Compose service name
DB_HOST = "database"

This name comes from:

# Role: Define the service name used by the app to find PostgreSQL
services:
  database:

The internal connection is:

app container → database:5432 → PostgreSQL container

The app should not use localhost for this connection. Inside the app container, localhost means the app container itself—not the database container.

5. How does Python read and write database records?
Reading records

The /users route performs this workflow:

Request /users
    ↓
Connect to PostgreSQL
    ↓
Run SELECT
    ↓
Retrieve rows with fetchall()
    ↓
Convert rows to dictionaries
    ↓
Return JSON

Important Python operations:

# Role: Send a query that reads records from the users table
cur.execute("SELECT id, name, email, created_at FROM users ORDER BY id")

# Role: Retrieve all records returned by the query
users = cur.fetchall()
Writing a record

The /add-user route performs this workflow:

Receive name and email
    ↓
Connect to PostgreSQL
    ↓
Run INSERT
    ↓
Commit the change
    ↓
Return confirmation

Important Python operations:

# Role: Insert a new record using safe SQL parameters
cur.execute(
    "INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id",
    (name, email)
)

# Role: Permanently save the inserted record
conn.commit()

commit() is necessary after adding, changing, or deleting database records.

Workflow for your own ML project

Suppose your MOF project eventually predicts CO₂ uptake.