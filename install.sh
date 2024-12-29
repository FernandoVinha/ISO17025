#!/bin/bash

# Update the repository and ensure we are on the main branch
echo "Updating the main branch..."
git pull origin main

# Ask the user if they want to configure the server IP
read -p "Do you want to configure the server IP? (y/N): " CONFIGURE_IP
if [[ "$CONFIGURE_IP" =~ ^[Yy]$ ]]; then
    read -p "Enter the server IP (default: 0.0.0.0): " SERVER_IP
    SERVER_IP=${SERVER_IP:-0.0.0.0}
else
    SERVER_IP="0.0.0.0"
fi

# Ask the user if they want to configure the server port
read -p "Do you want to configure the server port? (y/N): " CONFIGURE_PORT
if [[ "$CONFIGURE_PORT" =~ ^[Yy]$ ]]; then
    read -p "Enter the server port (default: 80): " SERVER_PORT
    SERVER_PORT=${SERVER_PORT:-80}
else
    SERVER_PORT="80"
fi

# Create and activate the virtual environment
echo "Creating a virtual environment..."
python3 -m venv venv

echo "Activating the virtual environment..."
source venv/bin/activate

# Install dependencies from requirements.txt
echo "Installing dependencies..."
pip install -r requirements.txt

# Run Django migrations
echo "Running makemigrations..."
python manage.py makemigrations

echo "Running migrate..."
python manage.py migrate

# Create superuser
echo "Creating a superuser..."
python manage.py createsuperuser

# Create the Django startup script
echo "Creating the startup script..."
PROJECT_DIR=$(pwd)
SERVICE_NAME="ISO17025"

echo "#!/bin/bash
cd $PROJECT_DIR
source venv/bin/activate
python manage.py runserver $SERVER_IP:$SERVER_PORT" > start_django.sh

# Make the startup script executable
chmod +x start_django.sh

# Create the systemd service file
SERVICE_FILE="/etc/systemd/system/$SERVICE_NAME.service"

echo "[Unit]
Description=Start Django Server on boot

[Service]
ExecStart=$PROJECT_DIR/start_django.sh
User=root
Restart=always
WorkingDirectory=$PROJECT_DIR
Environment=PATH=$PROJECT_DIR/venv/bin

[Install]
WantedBy=multi-user.target" | sudo tee $SERVICE_FILE

# Reload systemd daemons, enable, and start the service
echo "Configuring and starting the systemd service..."
sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME
sudo systemctl start $SERVICE_NAME

# Final confirmation
echo "Setup complete! The Django server will automatically start on IP $SERVER_IP and port $SERVER_PORT."
