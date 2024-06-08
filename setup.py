from setuptools import setup, find_packages

setup(
    name="shared_models",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "SQLAlchemy>=1.3.0",
        "python-dotenv>=0.10.0",
    ],
)
