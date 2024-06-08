# Shared SQLAlchemy Models

This repository contains shared SQLAlchemy models used across multiple projects, such as the `quart_backend` and `postgres_db` repositories. By centralizing these models, we ensure consistency and maintainability across different components of our system.

## Repository Structure

```
shared_models/
├── setup.py
└── shared_models/
    ├── __init__.py
    └── models.py
```

## Installation

To include the shared models in your project, install the repository as an editable package. You can do this by including the following in your `requirements.txt` or by installing directly.

### Installing Directly

1. Clone the `shared_models` repository next to your project repositories:

   ```sh
   git clone https://github.com/your-username/shared_models.git
   ```

2. Install the shared models package:

   ```sh
   pip install -e ../shared_models
   ```

### Adding to `requirements.txt`

Add the following line to your `requirements.txt`:

```plaintext
-e ../shared_models
```

## Defining Models

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

## Setting Up the Repository

### Step 1: Create the Repository Structure

```sh
mkdir shared_models
cd shared_models
mkdir shared_models
touch setup.py shared_models/__init__.py shared_models/models.py
```

### Step 2: Define `setup.py`

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

### Step 3: Define Your Models

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

## Usage in Other Projects

### In `quart_backend`

1. Ensure `shared_models` is installed:

   ```sh
   pip install -e ../shared_models
   ```

2. Import the models in your backend code:

   ```python
   from shared_models.models import User
   ```

### In `postgres_db`

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
