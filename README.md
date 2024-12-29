
# ISO17025 Setup Script

This repository contains the necessary scripts and configurations to set up the ISO17025 Django project with automatic service initialization using systemd. The setup script automates tasks such as virtual environment creation, dependency installation, database migrations, and service configuration.

## How to Use the Setup Script

To set up the ISO17025 project, follow these steps:

1. Clone the repository and navigate to the project directory:
   ```bash
   git clone https://github.com/FernandoVinha/ISO17025.git
   cd ISO17025
   ```

2. If the script is not already in the repository or you need the latest version, download it directly:
   ```bash
   wget https://raw.githubusercontent.com/FernandoVinha/ISO17025/main/install.sh
   ```

3. Make the script executable by running:
   ```bash
   chmod +x install.sh
   ```

4. Execute the script to set up the environment:
   ```bash
   ./install.sh
   ```

5. During execution, follow the prompts to configure the server's IP and port. If no configuration is provided, the default values will be used:
   - **Default IP:** `0.0.0.0`
   - **Default Port:** `80`

The script will handle the following tasks:
- Create a Python virtual environment.
- Install all dependencies from `requirements.txt`.
- Run database migrations for the Django project.
- Create a `systemd` service to ensure the Django server starts automatically on system boot.

## Managing the Django Service

After the setup, the service named `ISO17025` will be installed and configured to start automatically. Use the following commands to manage the service:

- To start the service:
  ```bash
  sudo systemctl start ISO17025
  ```

- To stop the service:
  ```bash
  sudo systemctl stop ISO17025
  ```

- To restart the service:
  ```bash
  sudo systemctl restart ISO17025
  ```

- To check the status of the service:
  ```bash
  sudo systemctl status ISO17025
  ```

## How to Remove the Setup Script

If you want to delete the setup script after installation, follow these steps:

1. Ensure you are in the project directory:
   ```bash
   cd ISO17025
   ```

2. Delete the setup script:
   ```bash
   rm install.sh
   ```

3. Verify the deletion:
   ```bash
   ls
   ```
   The script `install.sh` should no longer be listed.

## Default Configuration

By default, the server will run on:
- **IP Address:** `0.0.0.0`
- **Port:** `80`

You can change these settings by editing the file `start_django.sh` generated during the setup:
```bash
nano start_django.sh
```

## Prerequisites

Before running the setup script, make sure your system meets the following requirements:
- Python 3 installed
- pip and virtualenv installed
- Sudo privileges to configure the `systemd` service

## Troubleshooting

If you encounter issues during or after the setup, try the following steps:

1. Ensure all Python dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```

2. Check the status of the Django service:
   ```bash
   sudo systemctl status ISO17025
   ```

3. Review the service logs for any errors:
   ```bash
   journalctl -u ISO17025
   ```

If you continue to face issues, feel free to open an issue in this repository with a detailed description of the problem.