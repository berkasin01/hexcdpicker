# Hex Colour Picker

Upload an image and get the top 10 most common hex colour codes from it. Built with Flask, NumPy, and Matplotlib.

## What It Does

Upload a .png or .jpg image through the browser. The app analyses every pixel, counts colour frequency, and returns the 10 most dominant colours as hex codes.

## How It Works

1. Upload image through Flask web form
2. Reads pixel data with Matplotlib
3. Counts unique RGB values with NumPy
4. Sorts by frequency and converts top 10 to hex codes
5. Displays results on a new page

## Usage
```
python main.py
```

## Requirements
```
pip install flask flask-bootstrap flask-wtf matplotlib numpy werkzeug
```
