# Docker Learning Repository

Welcome to my Docker Learning Repository! 🐳

This repository contains notes, examples, and practical tips for learning Docker from scratch. The content is divided into chapters, covering everything from Docker basics to advanced topics like networking, volumes, and Docker Compose.

---

## **Table of Contents**

- [Chapter 1: Docker Basics](#Chapter1)
- [Chapter 2: Port Forwarding](#Chapter2)
- [Chapter 3: Network Adapters](#Chapter3)
- [Chapter 4: Docker Compose](#Chapter4)
- [Chapter 5: Volumes](#Chapter5)

---

## **Chapter 1: Docker Basics**

Docker is a platform for developing, shipping, and running applications inside lightweight containers.  

**Key Concepts:**

- **Container:** Lightweight, portable, isolated environment for running apps.  
- **Image:** Blueprint for a container; contains the app and its dependencies.  
- **Docker Engine:** Core service that runs containers.  
- **Docker Hub:** Repository of public Docker images.  

**Basic Commands:**

```bash
docker --version         # Check Docker version
docker pull <image>      # Download an image
docker images            # List images
docker ps                # List running containers
docker run <image>       # Run a container
docker stop <container>  # Stop a running container
docker rm <container>    # Remove a container
docker rmi <image>       # Remove an image
````

---

## **Chapter 2: Port Forwarding**

Port forwarding allows your host machine to access services running inside a container.

**Example:**

```bash
docker run -p 5000:5000 flask-app
```

* `5000:5000` → `host_port:container_port`
* Allows access via `http://localhost:5000`

**Tips:**

* Always map container ports you need to expose.
* Useful for web servers, APIs, and databases.

---

## **Chapter 3: Network Adapters**

Docker provides **network isolation** for containers.

**Default Networks:**

* **bridge** → default for standalone containers
* **host** → container shares host network
* **none** → no networking

**Custom Networks:**

```bash
docker network create my_network
docker run --network my_network <image>
```

* Containers in the same network can communicate using **container names as hostnames**.
* Essential for multi-container apps like Flask + MySQL.

---

## **Chapter 4: Docker Compose**

Docker Compose lets you define and run **multi-container applications** using a `docker-compose.yml` file.

**Example: Flask + MySQL:**

```yaml
version: "3.9"

services:
  web:
    image: flask:latest
    ports:
      - "5000:5000"
    volumes:
      - ./app:/app
    depends_on:
      - db

  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: mydb
    volumes:
      - db_data:/var/lib/mysql

volumes:
  db_data:
```

**Commands:**

```bash
docker compose up          # Start services
docker compose up -d       # Start in detached mode
docker compose down        # Stop and remove containers
docker compose logs -f     # Follow logs
docker compose ps          # List services
```

**Benefits:**

* One command starts **all containers**
* Simplifies **networks and volumes**
* Supports **service dependencies**

---

## **Chapter 5: Volumes**

Volumes provide **persistent storage** for Docker containers.

**Types:**

1. **Named Volumes (Docker-managed):**

```yaml
volumes:
  db_data:
```

2. **Bind Mounts (host folder mapped):**

```yaml
volumes:
  - ./DATABASE/init.sql:/docker-entrypoint-initdb.d/init.sql
```

**Example: MySQL with persistent data**

```yaml
services:
  db:
    image: mysql:8.0
    volumes:
      - db_data:/var/lib/mysql
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql

volumes:
  db_data:
```

**Volume Commands:**

```bash
docker volume ls           # List volumes
docker volume inspect db_data
docker volume rm db_data   # Delete volume
docker volume prune        # Remove unused volumes
```

**Key Takeaways:**

* **Bind mounts** → for code/config or initial scripts
* **Named volumes** → for persistent database storage
* **Volumes ensure data survives container deletion**

---

## **Conclusion**

This repository is a structured guide to learn Docker step by step:

* Start with basics → containers, images, commands
* Learn **port mapping** to expose services
* Explore **networks** for container communication
* Master **Docker Compose** for multi-container apps
* Use **volumes** for persistent data

Docker makes development, testing, and deployment consistent and portable. 🚀

---

**Happy Dockerizing!** 🐳

```
