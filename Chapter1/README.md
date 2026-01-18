# Docker Basics

A beginner-friendly guide to **Docker images**, **containers**, **Dockerfile**, and commonly used **Docker commands and flags**.

---

## Table of Contents

1. What is Docker
2. Docker Architecture
3. Docker Images
4. Docker Containers
5. Dockerfile
6. Building Docker Images
7. Running Docker Containers
8. Docker Run Flags (Options)
9. Container Management Commands
10. Port Mapping
11. Volumes
12. Docker Ignore
13. Best Practices
14. Common Docker Commands Summary

---

## 1. What is Docker?

Docker is a containerization platform that allows developers to:

* Package applications and dependencies together
* Run applications consistently across environments
* Deploy faster and more reliably

---

## 2. Docker Architecture

Docker consists of:

* **Docker Client** – CLI used to interact with Docker
* **Docker Daemon** – Manages containers and images
* **Docker Image** – Blueprint for containers
* **Docker Container** – Running instance of an image

---

## 3. Docker Images

### What is a Docker Image?

A Docker image is a **read-only template** used to create containers.

### List Images

```bash
docker images
```

### Pull an Image

```bash
docker pull nginx
```

---

## 4. Docker Containers

### What is a Container?

A container is a **running instance of a Docker image**.

### List Running Containers

```bash
docker ps
```

### List All Containers

```bash
docker ps -a
```

---

## 5. Dockerfile

A **Dockerfile** is a text file that contains instructions to build a Docker image.

### Example Dockerfile (Python App)

```Dockerfile
# Pull base image for Python 3.13
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy all files to container
COPY . .

# Run the application
CMD ["python", "main.py"]
```

---

## 6. Building Docker Images

### Build Command

```bash
docker build -t python-app .
```

### Command Breakdown

* `docker build` → Build image
* `-t` → Tag the image
* `python-app` → Image name
* `.` → Current directory as build context

---

## 7. Running Docker Containers

### Basic Run

```bash
docker run python-app
```

### Run with Name

```bash
docker run --name my-python-container python-app
```

---

## 8. Docker Run Flags (Options)

### Common Flags Example

```bash
docker run -i -t -d --name app-container -p 8000:8000 python-app
```

### Indented View (Easy to Understand)

```text
docker run
  -i
  -t
  -d
  --name app-container
  -p 8000:8000
  python-app
```

### Flag Explanation

| Flag     | Long Form       | Description        |
| -------- | --------------- | ------------------ |
| `-i`     | `--interactive` | Keeps STDIN open   |
| `-t`     | `--tty`         | Allocates terminal |
| `-d`     | `--detach`      | Run in background  |
| `--name` | —               | Name the container |
| `-p`     | `--publish`     | Port mapping       |

---

## 9. Container Management Commands

### Stop a Container

```bash
docker stop container_name
```

### Start a Container

```bash
docker start container_name
```

### Restart a Container

```bash
docker restart container_name
```

### Remove a Container

```bash
docker rm container_name
```

---

## 10. Port Mapping

### Map Host Port to Container Port

```bash
docker run -p 8080:80 nginx
```

| Host   | Container |
| ------ | --------- |
| `8080` | `80`      |

Access application:

```
http://localhost:8080
```

---

## 11. Volumes

Volumes are used to **persist data**.

### Create Volume

```bash
docker volume create app-data
```

### Use Volume

```bash
docker run -v app-data:/app/data python-app
```

---

## 12. .dockerignore

Prevents unnecessary files from being copied into the image.

### Example `.dockerignore`

```dockerignore
__pycache__/
.env
.git
.gitignore
node_modules/
*.log
```

---

## 13. Best Practices

* Use lightweight base images (`slim`, `alpine`)
* Use `.dockerignore`
* Minimize layers
* Use explicit image tags
* Clean unused resources

### Cleanup Command

```bash
docker system prune
```

---

## 14. Common Docker Commands Summary

### Image Commands

```bash
docker build
docker images
docker rmi
docker pull
```

### Container Commands

```bash
docker run
docker ps
docker stop
docker start
docker rm
```

### System Commands

```bash
docker info
docker version
docker system prune
```

---

## 🎯 Conclusion

Docker simplifies application deployment by packaging code and dependencies into containers that run consistently across all environments.
