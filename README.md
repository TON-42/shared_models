# Postgres DB

This repository manages the PostgreSQL database schema using Alembic for migrations. It uses shared SQLAlchemy models from the `shared_models` repository.

## Repository Structure

```plaintext
postgres_db/
│
├── migrations/                # Database migration scripts
│   ├── V1__initial_setup.sql
│   ├── V2__add_users_table.sql
│   └── ...
├── docker-compose.yml         # Docker setup for local development
├── init_db.sh                 # Initialization script
├── README.md                  # Documentation
└── config/                    # Database configuration files
```

## Installation and Setup

### Step 1: Clone the Repositories

Clone the `postgres_db` and `shared_models` repositories:

```sh
git clone https://github.com/TON-42/shared_models.git
git clone https://github.com/TON-42/postgres_db.git
cd postgres_db
```

### Step 2: Set Up Virtual Environment

Create and activate a virtual environment:

```sh
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

Install the required dependencies:

```sh
pip install -r requirements.txt
```

### Step 4: Install Shared Models

Install the shared models package:

```sh
pip install -e ../shared_models
```

### Step 5: Create a .env File

Create a `.env` file in the `postgres_db` directory with the following content:

```env
POSTGRES_USER=devuser
POSTGRES_PASSWORD=devpassword
POSTGRES_DB=mydatabase
DATABASE_URL=postgresql://devuser:devpassword@localhost:5432/mydatabase
```

### Step 6: Start PostgreSQL with Docker

Start the PostgreSQL database using Docker:

```sh
docker-compose up -d
```

### Step 7: Initialize the Database

Run the initialization script to set up the database:

```sh
./init_db.sh
```

### Step 8: Run Alembic Migrations

Create and apply the initial migration:

```sh
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## Explanation

### What is Alembic?

Alembic is a lightweight database migration tool for use with SQLAlchemy, the Python SQL toolkit. It provides a system for managing changes to your database schema, allowing you to version control your database schema changes and apply them in a controlled manner.

### Understanding the Connection String

The connection string format for SQLAlchemy typically looks like this:

```plaintext
dialect+driver://username:password@host:port/database
```

For example, a PostgreSQL connection string might look like this:

```plaintext
postgresql://devuser:devpassword@localhost:5432/mydatabase
```

### Using Environment Variables

We use environment variables to keep sensitive information secure and make the configuration more flexible.

#### .env File

The `.env` file stores your PostgreSQL credentials:

```env
POSTGRES_USER=devuser
POSTGRES_PASSWORD=devpassword
POSTGRES_DB=mydatabase
DATABASE_URL=postgresql://devuser:devpassword@localhost:5432/mydatabase
```

#### docker-compose.yml

The `docker-compose.yml` file loads environment variables from the `.env` file:

```yaml
version: "3.8"

services:
  postgres:
    image: postgres
    env_file:
      - .env
    ports:
      - "5432:5432"
    volumes:
      - ./sql:/docker-entrypoint-initdb.d
```

### Alembic Configuration

#### alembic.ini

Set a placeholder in the `alembic.ini` file:

```ini
sqlalchemy.url = driver://user:pass@host/dbname
```

#### env.py

Update `alembic/env.py` to load the environment variables and set the `sqlalchemy.url` dynamically:

```python
from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from shared_models.models import Base  # Import your Base from the shared models package

config = context.config

# Override the sqlalchemy.url setting in alembic.ini with the DATABASE_URL from .env
config.set_main_option('sqlalchemy.url', os.getenv('DATABASE_URL'))

fileConfig(config.config_file_name)
target_metadata = Base.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

### Summary

By following these steps, backend developers should have a fully functional local environment to work with the PostgreSQL database. If there are any issues, ensure the dependencies are correctly installed, and the Docker container is running without errors.

## Shared SQLAlchemy Models

This repository contains shared SQLAlchemy models used across multiple projects, such as the `quart_backend` and `postgres_db` repositories. By centralizing these models, we ensure consistency and maintainability across different components of our system.

### Repository Structure

```plaintext
shared_models/
├── setup.py
└── shared_models/
    ├── __init__.py
    └── models.py
```

### Installation

To include the shared models in your project, install the repository as an editable package. You can do this by including the following in your `requirements.txt` or by installing directly.

#### Installing Directly

1. Clone the `shared_models` repository next to your project repositories:

   ```sh
   git clone https://github.com/your-username/shared_models.git
   ```

2. Install the shared models package:

   ```sh
   pip install -e ../shared_models
   ```

#### Adding to `requirements.txt`

Add the following line to your `requirements.txt`:

```plaintext
-e ../shared_models
```

### Defining Models

Define your SQLAlchemy models in `shared_models/models.py`:

```python
# shared_models/models.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(100), unique=True)
```

### Setting Up the Repository

#### Step 1: Create the Repository Structure

```sh
mkdir shared_models
cd shared_models
mkdir shared_models
touch setup.py shared_models/__init__.py shared_models/models.py
```

#### Step 2: Define `setup.py`

**setup.py**:

```python
from setuptools import setup, find_packages

setup(
    name='shared_models',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'sqlalchemy',
    ],
)
```

#### Step 3: Define Your Models

**shared_models/models.py**:

```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(100), unique=True)
```

### Usage in Other Projects

#### In `quart_backend`

1. Ensure `shared_models` is installed:

   ```sh
   pip install -e ../shared_models
   ```

2. Import the models in your backend code:

   ```python
   from shared_models.models import User
   ```

#### In `postgres_db`

1. Ensure `shared_models` is installed:

   ```sh
   pip install -e ../shared_models
   ```

2. Configure Alembic to use the shared models in `env.py`:

   **alembic/env.py**:

   ```python
   from alembic import context
   from sqlalchemy import engine_from_config, pool
   from logging.config import fileConfig
   import os
   from dotenv import load_dotenv

   # Load environment variables from .env file
   load_dotenv()

   from shared_models.models import Base  # Import your Base from the shared models package

   config = context.config

   # Override the sqlalchemy.url setting in alembic.ini with the DATABASE_URL from .env
   config.set_main_option('sqlalchemy.url', os.getenv('DATABASE_URL'))

   fileConfig(config.config_file_name)
   target_metadata = Base.metadata

   def run_migrations_offline():
       url = config.get_main_option("sqlalchemy.url")
       context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

       with context.begin_transaction():
           context.run_migrations()

   def run_migrations_online():
       connectable = engine_from_config(
           config.get_section(config.config_ini_section),
           prefix="sqlalchemy.",
           poolclass=pool.NullPool,
       )

       with connectable.connect() as connection:
           context.configure(connection=connection, target_metadata=target_metadata)

           with context.begin_transaction():
               context.run_migrations()

   if context.is_offline_mode():


       run_migrations_offline()
   else:
       run_migrations_online()
   ```
