# Android Permission Risk Analyzer

A web-based tool that analyzes Android application permissions and estimates the potential privacy and security risk associated with an app.

## Overview

Android applications often request permissions that allow access to sensitive device resources such as contacts, location, camera, microphone, storage, and SMS. This project analyzes an app's requested permissions and generates a risk assessment to help users better understand the potential privacy implications.

The project is powered by a large Android permissions dataset containing information from approximately 2.2 million Android applications collected from the Google Play Store.

## Features

* Analyze Android app permissions
* Calculate permission-based risk scores
* Identify potentially sensitive permissions
* Simple web interface
* Fast local analysis

## Dataset

This repository does **not** include the dataset because it exceeds GitHub's file size limits.

Download the dataset from Kaggle:

https://www.kaggle.com/datasets/gauthamp10/app-permissions-android

Dataset source: Android Permissions Dataset by Gautham Prakash. The dataset contains permission information for approximately 2.2 million Android applications collected from the Google Play Store.

### Setup Dataset

After downloading, place the dataset file in the project root directory:

```text
Android-Permission-Risk-Analyzer/
├── apps.json
├── backend.py
├── risk.py
├── static/
│   ├── script.js
│   └── style.css
└── templates/
    └── index.html
```

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/greeshg6/Android-Permission-Risk-Analyzer.git
cd Android-Permission-Risk-Analyzer
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

If you do not have a requirements file, install the required packages manually.

### 3. Download the Dataset

Download the dataset from Kaggle and place `apps.json` in the project root directory.

### 4. Run the Application

```bash
python backend.py
```

Open your browser and navigate to:

```text
http://localhost:5000
```

## Project Structure

```text
Android-Permission-Risk-Analyzer/
├── apps.json
├── backend.py
├── risk.py
├── static/
│   ├── script.js
│   └── style.css
├── templates/
│   └── index.html
├── .gitignore
└── README.md
```

## Tech Stack

* Python
* Flask
* HTML
* CSS
* JavaScript

## Disclaimer

This tool provides a permission-based risk estimate and should not be considered a complete security audit. Actual application behavior may differ from what permissions alone suggest.

## Dataset Attribution

Gautham Prakash, Android Permissions Dataset (Google Play Store applications).

Kaggle Dataset:
https://www.kaggle.com/datasets/gauthamp10/app-permissions-android

## License

This project is released under the MIT License.
