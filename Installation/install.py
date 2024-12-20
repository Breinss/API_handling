import subprocess
import sys
import os

# Define the location of your requirements.txt file
requirements_path = "requirements.txt"


# Function to install dependencies from requirements.txt
def install_requirements():
    if os.path.exists(requirements_path):
        print("Installing dependencies from requirements.txt...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", requirements_path]
        )
    else:
        print("requirements.txt not found.")


# Check if dependencies are installed by attempting to import them
def check_dependencies():
    try:
        # Try to import all the packages from requirements.txt
        with open(requirements_path, "r") as file:
            for line in file:
                package = line.strip().split("==")[
                    0
                ]  # Get the package name (ignores version)
                __import__(package)  # Try importing the package
        print("All dependencies are already installed.")
    except ModuleNotFoundError as e:
        print(f"Missing module: {e.name}")
        install_requirements()


if __name__ == "__main__":
    check_dependencies()
