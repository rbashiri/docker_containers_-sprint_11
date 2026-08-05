# What is Docker Compose?
Docker Compose is like the conductor leading an orchestra. Instead of individually telling each musician (container) when to play, the conductor (Docker Compose) coordinates them all using sheet music (a YAML file).

flowchart LR
    Browser["Browser<br>localhost:5000"] --> App["Flask app<br>container port 5000"]
    App -->|"database:5432"| DB["PostgreSQL<br>container port 5432"]