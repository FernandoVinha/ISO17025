#!/bin/bash

# Clone the repository with the main branch
git clone -b main https://github.com/FernandoVinha/ISO17025.git
cd ISO17025 || exit

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

# Final confirmation
echo "All branches have been merged into main. Check for conflicts and resolve them if needed."

