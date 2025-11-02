# 🐍 Python Generators — Database Stream Project (ALX ProDev)

## Overview

This project demonstrates how to integrate **Python generators** with a **MySQL database** for efficient, memory-safe data streaming.
It is part of the **ALX Backend Python: Advanced Generators Module**, showcasing how to build real-world data pipelines that connect to and stream rows from relational databases.

By completing this project, you will:

- Learn to create generators for streaming database rows.
- Work with MySQL databases and tables.
- Implement batch processing to minimize memory usage.
- Practice modular, maintainable Python coding.

---

### **🧱 Project Structure**

```folder
└── 📁python-generators-0x00
    ├── .env
    ├── 0-main.py
    ├── docker-compose.yml
    ├── my.cnf
    ├── README.md
    ├── seed.py
    └── user_data.csv
```

---

### **🚀 Getting Started**

#### **1. Clone the Repository**

```bash
git clone https://github.com/D0nG4667/alx-backend-python.git
cd alx-backend-python
```

#### **2. Environment Setup**

##### Install Dependencies with uv

```bash
uv sync
```

Create a `.env` file in the project root:

```bash
cd python-generators-0x00
```

```.env
MYSQL_ROOT_PASSWORD=alx_root_pass
MYSQL_DATABASE=ALX_prodev
MYSQL_USER=alx_user
MYSQL_PASSWORD=alx_pass
```

> ⚙️ These credentials are automatically loaded by Docker through `docker-compose.yml`.

---

### **🐬 Running MySQL with Docker**

#### **Start the Database**

```bash
docker-compose up -d
```

This spins up a MySQL 8.4.7 instance using:

- Port **3309** on the host → **3306** inside the container
- Volume persistence via `alx-mysql-data`
- Custom configuration via `my.cnf`

#### **Verify the Service**

```bash
docker ps
```

Look for the container named `alx-mysql`.

---

### **🧩 Running the Python Seeder**

#### **Run the Script**

```bash
python3 0-main.py
```

**Expected Output:**

```bash
connection successful
Table user_data created successfully
Database ALX_prodev is present 
[('00234e50...', 'Dan Altenwerth Jr.', 'Molly59@gmail.com', 67), ...]
```

---

### **📦 Docker Services**

```yaml
services:
  mysql:
    image: mysql:8.4.7
    container_name: alx-mysql
    env_file:
      - .env
    ports:
      - "3309:3306"
    volumes:
      - alx-mysql-data:/var/lib/mysql
      - ./my.cnf:/etc/mysql/conf.d/my.cnf:ro
    restart: unless-stopped

volumes:
  alx-mysql-data:
```

---

### **⚙️ MySQL Configuration (my.cnf)**

```ini
[mysqld]
bind-address = 0.0.0.0
default_authentication_plugin = mysql_native_password
```

---

### **📘 Key Learning Goals**

- Use **Python generators** to handle large datasets efficiently.
- Connect Python applications to **MySQL** using best practices.
- Seed, stream, and verify data using **structured SQL schemas**.
- Deploy a reproducible **Dockerized development environment**.

---

### **🪄 Example Generator Use Case**

```python
def stream_user_data(connection):
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")
    for row in cursor:
        yield row
```

---

### **🧹 Cleanup**

```bash
docker-compose down -v
```

## Benefits of Using Generators

- **Memory Efficiency:** Only yields one row at a time instead of loading the entire table.
- **Lazy Evaluation:** Rows are processed as needed.
- **Batch Processing:** Supports `fetchmany(batch_size)` for large datasets.
- **Modular and Maintainable:** Clear separation of database setup, insertion, and streaming logic.
