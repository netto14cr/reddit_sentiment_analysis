from dotenv import load_dotenv
import os
import subprocess
import time
import json
import signal

def main():
    # Initialize the program
    print(" * Initializing Program...\n")

    # Load environment variables from the .env file in the parent directory
    print(" * Loading environment variables from ../.env file...\n")
    load_dotenv(dotenv_path='../.env')

    # Print loaded environment variables for debugging
    print(" * Environment variables loaded:\n")
    for key, value in os.environ.items():
        print(f"\t{key}: {value}")

    # Get ngrok authentication token from environment variables
    print("\n * Fetching ngrok authentication token...\n")
    ngrok_auth_token = os.getenv('NGROK_AUTH_TOKEN')

    if not ngrok_auth_token:
        print(" * Error: NGROK_AUTH_TOKEN not found in ../.env file.\n")
        return

    # Authenticate with ngrok
    print(" * Authenticating with ngrok...\n")
    try:
        subprocess.run(['ngrok', 'authtoken', ngrok_auth_token], check=True)
        print(" * ngrok authentication successful.\n")
    except subprocess.CalledProcessError as e:
        print(f"Error during ngrok authentication: {e}\n")
        return

    # Start ngrok
    print(" * Starting ngrok...\n")
    ngrok_process = subprocess.Popen(['ngrok', 'http', '5000'])

    # Wait for ngrok to initialize
    print(" * Waiting for ngrok to initialize...\n")
    time.sleep(10)

    # Get the public URL of ngrok
    print(" * Retrieving ngrok public URL...\n")
    try:
        result = subprocess.run(['curl', '-s', 'http://127.0.0.1:4040/api/tunnels'], capture_output=True, text=True, check=True)
        tunnels_info = json.loads(result.stdout)
        ngrok_url = tunnels_info['tunnels'][0]['public_url']
        print(f" * Ngrok public URL: {ngrok_url}\n")
    except subprocess.CalledProcessError as e:
        print(f" * Error retrieving ngrok URL: {e}\n")
        ngrok_process.terminate()
        return
    except (json.JSONDecodeError, KeyError) as e:
        print(f" * Error parsing ngrok response: {e}\n")
        ngrok_process.terminate()
        return

    # Update the .env file in the parent directory with the new URL
    print(" * Updating ../.env file with new REACT_APP_NGROK_URL...\n")
    if update_env_file('REACT_APP_NGROK_URL', ngrok_url):
        print(f" * ../.env file updated successfully with REACT_APP_NGROK_URL: {ngrok_url}\n")
    else:
        print(" * Error updating ../.env file.\n")

    # Wait for user interruption to stop ngrok
    print(" * ngrok is running. Press Ctrl+C to stop it.\n")

    # Handle keyboard interruption
    def signal_handler(sig, frame):
        print("\n * Interruption received. Stopping ngrok...\n")
        ngrok_process.terminate()
        exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    # Wait indefinitely until interrupted
    while True:
        time.sleep(1)

def update_env_file(key, value):
    env_file_path = '../.env'
    temp_file_path = '../.env.tmp'

    print(f" * Reading {env_file_path}...\n")
    env_vars = {}

    # Read the .env file and store variables in a dictionary
    if os.path.exists(env_file_path):
        with open(env_file_path, 'r') as file:
            for line in file:
                if '=' in line:
                    k, v = line.strip().split('=', 1)
                    env_vars[k] = v
        print(" * Environment variables read from ../.env file:\n")
        for k, v in env_vars.items():
            print(f"\t{k}: {v}")
    else:
        print(f" * Error: The file {env_file_path} does not exist.\n")
        return False

    # Update the dictionary with the new variable
    env_vars[key] = value
    print(f" * Updating {key} to {value}\n")

    # Write the updated dictionary back to a temporary file
    try:
        with open(temp_file_path, 'w') as file:
            for k, v in env_vars.items():
                file.write(f'{k}={v}\n')
        # Replace the .env file with the temporary file
        os.replace(temp_file_path, env_file_path)
        print(" * The ../.env file has been updated successfully.\n")
        return True
    except IOError as e:
        print(f" * Error writing to the ../.env file: {e}\n")
        return False

if __name__ == "__main__":
    main()
