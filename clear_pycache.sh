#!/bin/bash
# Script to clear all __pycache__ directories and .pyc files in the project

find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
echo "All __pycache__ directories and .pyc files have been removed."
