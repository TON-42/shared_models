import sys
import os

# Add the shared_models path to sys.path
shared_models_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../shared_models")
)
sys.path.append(shared_models_path)

print("PYTHONPATH:", sys.path)

from shared_models.models import Base, User

print("Imported shared_models successfully.")
