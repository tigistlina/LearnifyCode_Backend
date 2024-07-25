# LearnifyCode_Backend

## Project Overview

LearnifyCode Backend is a RESTful API built with Flask that interacts with the OpenAI API and Firebase Firestore to provide curated coding lessons. The backend handles user authentication, token verification, and access control to ensure secure access to the lessons and other features.

## Features

- Interacts with the OpenAI API to generate coding lessons.
- Stores and retrieves lessons from Firebase Firestore.
- User authentication and token verification.
- Access control based on user roles and permissions.

## Prerequisites

Before you begin, ensure you have met the following requirements:
- Firebase account and project setup
- OpenAI account and API key

## Setup

Follow these steps to set up the project locally:
  1- choose a directory and git clone <code>
  2 - cd learnifycode-backend
  3 - python3 -m venv venv(to create virtual environment)
  4 - source venv/bin/activate (to activate environment)
  5 - pip install -r requirements.txt (to install dependencies)
  6 - Set up Firebase credentials
        - Generate a private key from your Firebase project and save it as firebase_credentials.json in the root of your project.
        - Add the Firebase credentials to your environment variables or use a .env file
  7 - flask run