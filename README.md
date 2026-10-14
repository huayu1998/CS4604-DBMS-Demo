# CS 4604 DBMS Connection Demo

**Author: Huayu Liang, GTA**

**Date: 10/15/2026**

**Slides for the Demo**: [DBMS_Demo_Slides_Fall26.pdf](./DBMS_Demo_Slides_Fall26.pdf).

This repository contains the step-by-step workflow of a minimal app to demo connecting a database to an application and running CRUD operations on a `students` table (`studentID`, `name`, `major`, `gpa`).

## Tech Stack

| Layer            | Tool                    |
| ---------------- | ----------------------- |
| Frontend         | React JS (Vite)         |
| Backend          | Flask REST API (Python) |
| Database         | MySQL                   |
| DB visualization | phpMyAdmin (Docker)     |
| OS               | macOS                   |

## Demo Workflow

0. [Prerequisites](#step-0---prerequisites)
1. [Create the Flask API (backend)](#step-1---flask-api-backend)
2. [Create the React app (frontend)](#step-2---react-app-frontend)
3. [Install MySQL locally](#step-3---install-mysql-locally)
4. [Create the DB, populate sample data, and run CRUD via SQL](#step-4---create-the-db-and-run-crud)
5. [Connect Flask ↔ MySQL](#step-5---connect-flask--mysql)
6. [Connect React ↔ Flask](#step-6---connect-react--flask)
7. [phpMyAdmin setup](#step-7---phpmyadmin-setup)
8. [Share the DB server and phpMyAdmin with the team](#step-8---share-with-the-team)

---

## Step 0 - Prerequisites

Install Node.js and Python.

```bash
brew install node 
brew install python
node -v && python3 --version
```

Create the project folder.

```bash
mkdir DBMS_Demo && cd DBMS_Demo
```

## Step 1 - Flask API (backend)

Create the backend folder and virtual environment.

```bash
mkdir backend && cd backend
python3 -m venv venv
source venv/bin/activate
```

Install Flask.

```bash
pip install flask flask-cors
```

Create `backend/app.py` with a `/` route and a `/api/students` route, then run and test it.

```bash
touch app.py
python app.py
curl http://127.0.0.1:5001/api/students
```

- `flask-cors` lets React (port 5173) call Flask (port 5001).

## Step 2 - React app (frontend)

From the project root directory, create a React app & follow the steps to finish the app initialization (e.g. the linter).

```bash
npm create vite@latest frontend -- --template react
```

Change directory, start the server and run the app:

```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:5173/](http://localhost:5173/).

## Step 3 - Install MySQL locally

```bash
brew install mysql
brew services start mysql
mysql --version
```

Create a database with the username `demo`and grant it the access to create database.

```bash
mysql -u root -p -e "CREATE USER 'demo'@'localhost'; GRANT ALL PRIVILEGES ON *.* TO 'demo'@'localhost';"
```

Check all the users and hosts on the MySQL server.

```bash
mysql -u root -e "SELECT user, host FROM mysql.user;"
```

Launches the MySQL database connecting as the user `demo`.

```bash
mysql -u demo -p
```

## Step 4 - Create the DB and run CRUD

### 4.1 Create the DB and `students` table

Inside the `mysql` prompt:

Check existing databases and create a new one.

```sql
SHOW DATABASES;
CREATE DATABASE student_demo;
```

Select the database and confirm the current db.

```sql
USE student_db;
SELECT DATABASE();
```

Create a simple`STUDENT`table.

```sql
CREATE TABLE students (
  studentID INT PRIMARY KEY AUTO_INCREMENT,
  name      VARCHAR(100) NOT NULL,
  major     VARCHAR(50),
  gpa       DECIMAL(3,2)
);
```

List tables in the selected DB.

```sql
SHOW TABLES;
```

### 4.2 Run the basic CRUD operations

```sql
-- Create
INSERT INTO students (name, major, gpa) VALUES ('Alice', 'CS', 3.80);
-- Read
SELECT * FROM students;
-- Update
UPDATE students SET gpa = 3.90 WHERE studentID = 1;
-- Delete
DELETE FROM students WHERE studentID = 1;
```

Always use `WHERE` with `UPDATE` and `DELETE`.

Type `exit` to leave the MySQL prompt.

## Step 5 - Connect Flask ↔ MySQL

## 5.1 Install connector and Store credentials

Install the MySQL connector and dotenv (inside the `backend/`)

```bash
cd backend
source venv/bin/activate
pip install mysql-connector-python python-dotenv
touch .env
```

To check all the credentials information.

```
mysql -u demo -p -e "SELECT @@port AS DB_PORT, SUBSTRING_
INDEX(USER(), '@', 1) AS DB_USER; SHOW DATABASES;"
```

Store the credentials inside the `backend/.env`.

```
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=<Database User>
DB_PASSWORD=<Database Password>
DB_NAME=<Database Name>
```

Add to `.gitignore`(never commit it):

```
.env
venv/
```

### 5.2 Update `app.py` and test each endpoint

Update `backend/app.py` with the DB-backed version (CRUD endpoints), then run it.

| CRUD   | HTTP   | Endpoint               |
| ------ | ------ | ---------------------- |
| Create | POST   | `/api/students`      |
| Read   | GET    | `/api/students`      |
| Update | PUT    | `/api/students/<id>` |
| Delete | DELETE | `/api/students/<id>` |

```bash
python app.py
```

```bash
# Read
curl http://127.0.0.1:5001/api/students

# Create
curl -X POST http://127.0.0.1:5001/api/students \
  -H "Content-Type: application/json" \
  -d '{"name":"Alex","major":"ECE","gpa":3.5}'

# Update (use the studentID returned by Create)
curl -X PUT http://127.0.0.1:5001/api/students/2 \
  -H "Content-Type: application/json" \
  -d '{"name":"Bob","major":"CS","gpa":3.9}'

# Delete
curl -X DELETE http://127.0.0.1:5001/api/students/2
```

Confirm the DB changed:

```bash
mysql -u demo -e "SELECT * FROM student_demo.students;"
```

## Step 6 - Connect React ↔ Flask

Update `frontend/src/App.jsx` so React calls the Flask API with `fetch()` (Read, Create, Update, Delete), then run both servers in two terminals.

```bash
# Terminal 1: backend
cd backend && source venv/bin/activate && python app.py

# Terminal 2: frontend
cd frontend && npm run dev
```

Execute: add, edit and delete a student at [http://localhost:5173/](http://localhost:5173/), then verify:

```bash
mysql -u demo -e "SELECT * FROM student_demo.students;"
```

## Step 7 - phpMyAdmin setup

Install Docker Desktop and run phpMyAdmin.

```bash
brew install --cask docker-desktop
docker --version
```

Open Docker Desktop & Setup and run the phpMyAdmin

```bash
open -a Docker
```

```bash
docker run -d --name phpmyadmin -p 8080:80 \
  -e PMA_HOST=host.docker.internal -e PMA_PORT=3306 \
  phpmyadmin:latest
```

Open [http://localhost:8080](http://localhost:8080) and log in as `demo` user with the MySQL demo user password (if any).

- If the phpMyAdmin rejects an empty password and the `demo` user has none, set one and update `DB_PASSWORD` in `backend/.env`:

  ```bash
  mysql -u root -e "ALTER USER 'demo'@'localhost' IDENTIFIED BY '<new_password>';"
  ```
- Manage the container:

  ```bash
  docker ps                 # is it running?
  docker logs phpmyadmin    # see errors
  docker stop phpmyadmin    # stop
  docker start phpmyadmin   # start again
  docker rm -f phpmyadmin   # remove (re-create with docker run)
  ```

## Step 8 - Share with the team

Only a **cloud** MySQL server can be shared; a local one is reachable only from your own machine.

1. On the cloud server, create one user per teammate (limited to `student_db`):

   ```sql
   CREATE USER 'teammate1'@'%' IDENTIFIED BY '<strong_password>';
   GRANT ALL PRIVILEGES ON student_db.* TO 'teammate1'@'%';
   ```
2. Send each teammate the host, port, user, password and CA certificate (`ca.pem`) privately, never through git.
3. Each teammate clones the repo and fills in `backend/.env`:

   ```
   DB_HOST=<cloud-host>
   DB_PORT=<port>
   DB_USER=<user>
   DB_PASSWORD=<password>
   DB_NAME=student_db
   DB_SSL_CA=/path/to/ca.pem
   ```
4. Each teammate runs the backend and frontend as in Step 6, and phpMyAdmin with a free server field:

   ```bash
   docker run -d --name phpmyadmin -p 8080:80 \
     -e PMA_ARBITRARY=1 -e PMA_SSL=1 phpmyadmin:latest
   ```

   Log in with Server `<host>:<port>` and their own user.

---

## Quick Docs Ref

| Topic               | Links                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Prereq              | [Node.js Install &amp; Download](https://nodejs.org/en/download) · [Python venv](https://docs.python.org/3/library/venv.html)                                                                                                                                                                                                                                                                                                                            |
| Backend & Frontend  | [Flask: Quick Start](https://flask.palletsprojects.com/en/stable/quickstart/) & [Flask: CORS](https://flask-cors.readthedocs.io/) · [Vite: Getting Started](https://vite.dev/guide/) · [React: Start a New Project](https://react.dev/learn/creating-a-react-app) & [Quick Start](https://react.dev/learn)                                                                                                                                                 |
| MySQL               | [Install MySQL on macOS](https://dev.mysql.com/doc/refman/8.4/en/macos-installation.html) & [Install with Homebrew](https://formulae.brew.sh/formula/mysql) · Request a Cloud MySQL: [Aiven](https://aiven.io/free-mysql-database) or [Azure](https://azure.microsoft.com/en-us/pricing/purchase-options/azure-account?icid=mysql) · [Data Manipulation Statements (MySQL)](https://dev.mysql.com/doc/refman/8.4/en/sql-data-manipulation-statements.html) |
| MySQL-Flask Connect | [Connect with Connector](https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html) · [Python-dotenv](https://pypi.org/project/python-dotenv/) · [Flask: HTTP methods](https://flask.palletsprojects.com/en/stable/quickstart/#http-methods)                                                                                                                                                                                |
| React-Flask Connect | [MDN: Using Fetch](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch) · [React Doc](https://react.dev/learn)                                                                                                                                                                                                                                                                                                                        |
| phpMyAdmin          | [Docker Desktop for Mac](https://docs.docker.com/desktop/setup/install/mac-install/) · [phpMyAdmin Docker image](https://hub.docker.com/_/phpmyadmin)                                                                                                                                                                                                                                                                                                    |

## Resources

**DBMS Servers (Relational)**

- PostgreSQL: [https://www.postgresql.org/](https://www.postgresql.org/)
- SQLite: [https://www.sqlite.org/](https://www.sqlite.org/)
- Microsoft SQL Server: [https://www.microsoft.com/en-us/sql-server](https://www.microsoft.com/en-us/sql-server)

**DBMS Visualization Tools**

- DBeaver: [https://dbeaver.io/](https://dbeaver.io/)
- MySQL Workbench: [https://www.mysql.com/products/workbench/](https://www.mysql.com/products/workbench/)
- pgAdmin: [https://www.pgadmin.org/](https://www.pgadmin.org/)
- TablePlus: [https://tableplus.com](https://tableplus.com)

**Cloud MySQL Servers**

- AZure: [azure.microsoft.com/en-us/pricing/purchase-options/azure-account?icid=mysql](https://azure.microsoft.com/en-us/pricing/purchase-options/azure-account?icid=mysql)
- Aiven: [aiven.io/free-mysql-database](https://aiven.io/free-mysql-database)
