# **Docker Compose: Complete Notes**

Docker Compose is a tool for defining and running multi-container Docker applications using a single **YAML file** (`docker-compose.yml`).

It simplifies running multiple containers with networks, volumes, and dependencies.

---

## **1️⃣ What is Docker Compose?**

* **Docker Compose** lets you define multiple containers (services) in a single file.
* You can configure **networks, volumes, environment variables, and dependencies**.
* Then, you can start all containers with **one command**:

```bash
docker compose up
```

✅ Think of Compose as a way to **orchestrate Docker containers locally**.

---

## **2️⃣ Docker Compose File Structure**

A `docker-compose.yml` file typically has three sections:

1. **services** → defines containers
2. **volumes** → defines persistent storage
3. **networks** → defines custom networks

**Basic example:**

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

**Explanation:**

* `web` → Flask container, binds host `./app` folder, exposes port 5000
* `db` → MySQL container, persists data in `db_data`
* `depends_on` → ensures `db` starts before `web`

---

## **3️⃣ Key Docker Compose Commands**

| Command                                   | Description                                         |
| ----------------------------------------- | --------------------------------------------------- |
| `docker compose up`                       | Starts all services defined in `docker-compose.yml` |
| `docker compose up -d`                    | Starts services in **detached mode** (background)   |
| `docker compose down`                     | Stops and removes containers, networks              |
| `docker compose down -v`                  | Removes **containers, networks, and volumes**       |
| `docker compose ps`                       | Lists running services                              |
| `docker compose logs`                     | Shows logs of all services                          |
| `docker compose logs -f`                  | Shows live logs (follow)                            |
| `docker compose restart`                  | Restarts services                                   |
| `docker compose stop`                     | Stops services without removing them                |
| `docker compose build`                    | Builds images defined in Compose file               |
| `docker compose exec <service> <command>` | Runs command inside a running container             |
| `docker compose run <service> <command>`  | Runs a one-time command in a new container          |
| `docker compose config`                   | Validates Compose file and shows final config       |

---

## **4️⃣ Running Conditions**

* **Docker Engine must be running**.
* **docker-compose.yml** must be in current directory.
* Use `depends_on` for **start order**, but note it **doesn’t wait for readiness**, only container start.
* Use **healthchecks** for waiting until services are ready.

**Example with healthcheck for MySQL:**

```yaml
services:
  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      retries: 5

  web:
    image: flask:latest
    depends_on:
      db:
        condition: service_healthy
```

✅ This ensures Flask starts **only after MySQL is healthy**.

---

## **5️⃣ Volumes in Docker Compose**

Volumes ensure **persistent data**.

* **Named volumes (Docker-managed)**

```yaml
volumes:
  db_data:
```

* **Bind mounts (host folder/file)**

```yaml
volumes:
  - ./app:/app
```

**Combined usage:**

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

---

## **6️⃣ Networks in Docker Compose**

By default, Compose creates a **bridge network** for all services.

* Containers can communicate using **service names as hostnames**.
* Custom networks example:

```yaml
networks:
  my_network:

services:
  web:
    image: flask:latest
    networks:
      - my_network
  db:
    image: mysql:8.0
    networks:
      - my_network
```

---

## **7️⃣ Example Full Stack Compose Setup**

**Services:** Flask + MySQL + Redis

```yaml
version: "3.9"

services:
  web:
    build: ./backend
    ports:
      - "5000:5000"
    volumes:
      - ./backend:/app
    environment:
      - REDIS_HOST=redis
      - DB_HOST=db
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - app_network

  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: mydb
    volumes:
      - db_data:/var/lib/mysql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      retries: 5
    networks:
      - app_network

  redis:
    image: redis:alpine
    networks:
      - app_network

volumes:
  db_data:

networks:
  app_network:
```

---

## **8️⃣ Full Flow Diagram**

```
        ┌───────────────────────────┐
        │       Host Machine        │
        │  ./backend (Flask code)  │
        │  ./init.sql (DB script)  │
        └─────────────┬─────────────┘
                      │
                      ▼
            ┌─────────┴─────────┐
            │   Docker Network   │
            │   app_network      │
            └───────┬───────────┘
                    │
       ┌────────────┼─────────────┐
       ▼            ▼             ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ Flask       │ │ MySQL       │ │ Redis       │
│ Container   │ │ Container   │ │ Container   │
│ web         │ │ db          │ │ redis       │
│ /app        │ │ /var/lib/mysql ││ /data     │
│ ports 5000  │ │ db_data vol │ │ ephemeral  │
└─────────────┘ └─────────────┘ └─────────────┘
```

**Flow Explanation:**

1. Flask container connects to MySQL using hostname `db`.
2. Flask container connects to Redis using hostname `redis`.
3. MySQL data persists in named volume `db_data`.
4. Custom network `app_network` allows communication between containers.

---

## **9️⃣ Tips & Best Practices**

* Use **`.env` file** for sensitive data (passwords, secrets)

```yaml
environment:
  MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
```

* Always **version your Compose file** (`version: "3.9"`)
* Use **named volumes** for databases and **bind mounts** for code in development
* Use **healthchecks** for service dependencies
* Use `docker compose logs -f` to debug containers
* Use `docker compose down -v` to reset database completely

---

✅ **Key Takeaways:**

* **Compose = multi-container orchestration**
* **Volumes = persistent storage**
* **Networks = container communication**
* **One command (`docker compose up`) = start everything**
* **Healthchecks & depends_on = reliable startup order**

---