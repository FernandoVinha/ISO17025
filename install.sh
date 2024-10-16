#!/bin/bash

# Navegar para o diretório do projeto, caso necessário
# cd /caminho/para/seu/projeto

# Fetch all remote branches
git fetch origin

# Checkout the main branch
git checkout main

# Merge other branches into main
echo "Merging origin/maintenance into main..."
git merge origin/maintenance -m "Merge branch 'maintenance' into main"

echo "Merging origin/accounts into main..."
git merge origin/accounts -m "Merge branch 'accounts' into main"

echo "Merging origin/config into main..."
git merge origin/config -m "Merge branch 'config' into main"

echo "Merging origin/inventory into main..."
git merge origin/inventory -m "Merge branch 'inventory' into main"

echo "Merging origin/locations into main..."
git merge origin/locations -m "Merge branch 'locations' into main"

# Create and activate virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies from requirements.txt
echo "Installing dependencies..."
pip install -r requirements.txt

# Run makemigrations and migrate
echo "Running makemigrations..."
python manage.py makemigrations

echo "Running migrate..."
python manage.py migrate

# Create superuser
echo "Creating superuser..."
python manage.py createsuperuser

# Final confirmation
echo "All branches have been merged into main, dependencies installed, migrations applied, and superuser created. Check for any issues."
