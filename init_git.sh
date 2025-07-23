#!/bin/bash

# Initialize Git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit"

# Instructions for adding a remote repository
echo ""
echo "Repository initialized successfully!"
echo ""
echo "To push to GitHub, run the following commands:"
echo "  git remote add origin https://github.com/yourusername/investment-portfolio-allocation.git"
echo "  git branch -M main"
echo "  git push -u origin main"
echo ""
echo "Replace 'yourusername' with your GitHub username."