import os
import subprocess
import sys
import platform

def create_and_activate_venv():
    # Determine the path of the virtual environment in the root directory
    root_dir = os.path.dirname(os.path.dirname(__file__))
    venv_dir = os.path.join(root_dir, 'env')

    # Check the operating system to define the path to the Python executable in the virtual environment
    if platform.system() == 'Windows':
        venv_python = os.path.join(venv_dir, 'Scripts', 'python')
    else:
        venv_python = os.path.join(venv_dir, 'bin', 'python')

    # Check if the virtual environment exists
    if not os.path.exists(venv_dir):
        print(" * Virtual environment not detected. Creating the virtual environment")
        subprocess.run([sys.executable, "-m", "venv", venv_dir])
        print(" * Virtual environment created successfully.")
    else:
        print(" * Virtual environment detected.")

    # Check if requirements.txt exists in the root directory and install dependencies
    requirements_path = os.path.join(root_dir, 'requirements.txt')
    if os.path.exists(requirements_path):
        print(" * Checking libraries")
        result = subprocess.run([venv_python, "-m", "pip", "install", "-r", requirements_path], capture_output=True, text=True)

        if result.returncode == 0:
            print(" * Libraries complete.")
        else:
            print(" * Dependencies missing. Installing required libraries")
            print(result.stdout)  # Display output of the pip install command
    else:
        print(" * No requirements.txt found. Skipping dependency installation.")

    print(" * Environment Setup Complete")
    # Return the path to the Python executable in the virtual environment
    return venv_python

def run_app(venv_python):
    print(" * Starting Application Execution")
    
    # Change the working directory to the root of the project
    root_dir = os.path.dirname(os.path.dirname(__file__))
    os.chdir(root_dir)
    
    # Path to app.py (located in the root directory)
    app_path = os.path.join(root_dir, 'app.py')
    
    # Run the application
    print(" * Running Flask app")
    subprocess.run([venv_python, app_path])
    
    print(" * Program Execution Completed Successfully")

if __name__ == "__main__":
    print(" * Initializing Program")
    # Create and activate the virtual environment
    venv_python = create_and_activate_venv()
    
    # Run the application
    run_app(venv_python)
