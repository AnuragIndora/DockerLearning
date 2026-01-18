## Learning Docker Networking (The Right Way)

This setup is a **perfect example** for properly understanding **Docker networking adapters**.

The Dockerfiles and application code are already correct.
What usually confuses people is **how to run containers in the right order and connect them using a shared network**.

Below is the **proper, production-style way** to do it — **without docker-compose** — so you actually understand what’s happening.

---

## Mental Model (How the System Works)

```
Browser
   |
localhost:5000
   |
[ backend container ]
        |
        |  (Docker bridge network + DNS)
        |
[ mysql container ]
```

### Important rule to remember

> Containers talk to each other using **container names**,
> not IP addresses and **never `localhost`**.

That’s why the backend code uses:

```python
host='mysql_cont'
```

This is correct.

---

## Step-by-Step: Running Everything Correctly

### 1. Create a Docker Network (Required)

```bash
docker network create app-net
```

This network gives us:

* Internal container DNS
* Stable name resolution
* Behavior that matches real production setups

---

### 2. Build the MySQL Image

From the project root:

```bash
cd database
docker build -t my-mysql .
```

Confirm it exists:

```bash
docker images | grep my-mysql
```

---

### 3. Run the MySQL Container (Always Start This First)

```bash
docker run -d \
  --name mysql_cont \
  --network app-net \
  -p 3306:3306 \
  my-mysql
```

Why this matters:

* The database must be running before the backend connects
* `mysql_cont` becomes the **DNS hostname** inside the Docker network

Check the logs:

```bash
docker logs mysql_cont
```

Wait until you see something like:

```
ready for connections
```

---

### 4. Build the Backend Image

```bash
cd ../backend
docker build -t flask-backend .
```

---

### 5. Run the Backend Container

```bash
docker run -d \
  --name backend_cont \
  --network app-net \
  -p 5000:5000 \
  flask-backend
```

---

### 6. Test the Application

#### Home endpoint

Open in your browser:

```
http://localhost:5000/
```

Expected output:

```
Docker Network Adapters Tutorial ...
```

---

#### Insert data (Database test)

```
http://localhost:5000/insert_data
```

Expected response:

```
Data Inserted Successfully!
```

---

### 7. Verify Data in MySQL (Optional but Important)

```bash
docker exec -it mysql_cont mysql -u root -p
```

Password:

```
12345678
```

Then run:

```sql
USE demodb;
SELECT * FROM users;
```

You should see the row that was inserted by the backend.

---

## Why This Works (Key Concepts)

### 1. Docker DNS

Inside the backend container:

```text
host='mysql_cont'
```

Docker automatically resolves this name because **both containers are on the same user-defined network (`app-net`)**.

---

### 2. Why `localhost` Does NOT Work

Inside a container:

```text
localhost = that same container
```

So if the backend tries to connect to `localhost`, it’s just talking to itself — not MySQL.

This is the **most common Docker networking mistake**.

---

### 3. Ports vs Networks (Different Purposes)

* `-p 5000:5000` → lets **your browser** access the backend
* `--network app-net` → lets **containers talk to each other**

They solve **two completely different problems**.

---

## Common Problems and Fixes

### Backend starts before MySQL is ready

Error looks like:

```
pymysql.err.OperationalError
```

Simple fix:

```bash
docker restart backend_cont
```

(Proper solutions like retries or health checks come later.)

---

### Tables not created

Reason:

* MySQL volume already exists
* Init scripts only run on the first startup

Fix:

```bash
docker rm -f mysql_cont
docker volume prune
```

Then start MySQL again.

---
