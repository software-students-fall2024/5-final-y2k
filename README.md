[![Test web-app on Pull Request](https://github.com/software-students-fall2024/5-final-y2k/actions/workflows/testing.yml/badge.svg)](https://github.com/software-students-fall2024/5-final-y2k/blob/main/.github/workflows/testing.yml)
[![Publish Docker Image and Deploy to DigitalOcean](https://github.com/software-students-fall2024/5-final-y2k/actions/workflows/publishing.yml/badge.svg)](https://github.com/software-students-fall2024/5-final-y2k/blob/main/.github/workflows/publishing.yml)

# Final Project

An exercise to put to practice software development teamwork, subsystem communication, containers, deployment, and CI/CD pipelines. See [instructions](./instructions.md) for details.

## Project Name

Y2K

## Table of Contents

1. [Project Description](#project-description)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [Setup Instructions](#setup-instructions)
5. [Usage](#usage)
6. [Project Structure](#project-structure)
7. [Task Board](#task-board)
8. [Team Members](#team-members)
9. [Acknowledgements](#acknowledgements)

### Project Description

An Audio Recording & Transcription App

Record and save your audio files, share them with friends, and get automatic transcriptions. Perfect for notes, interviews, or anything you need!

### Features

- **Audio Recording & Storage**: Record and save audio files directly within the app.
- **Speech-to-Text Transcription**: Automatically transcribe recordings into text for easy accessibility.
- **File Privacy Options**: Set recordings as public or private to manage visibility.
- **File Management**: Edit, rename, or delete audio files and transcriptions.
- **User Authentication**: Secure registration and login system with password hashing.
- **File Sharing**: Share public audio files with others seamlessly.
- **Metadata Tracking**: Store detailed metadata, including upload time and user information.
- **Environment: Runs** Run Seamlessly in containerized environments using Docker

### Technologies Used

- **Languages**: Python (Flask for backend), JavaScript, HTML/CSS.
- **Frameworks & Libraries**: Flask, Flask-Login, PyMongo, GridFS, Pydub, SpeechRecognition.
- **Databases**: MongoDB (GridFS for audio file storage).
- **Tools**: Docker for containerized deployment, pipenv for dependency management.
- **CI/CD**: GitHub Actions for automated testing and deployment workflows.

## Wireframes

The wireframes for this project, designed in Figma, outline the structure and user interface.

[**Figma Wireframes**](https://www.figma.com/design/yLFRMQmg38yyakEGCcKE0K/Final-SWE-project?node-id=0-1&t=mGMPcWYwOiU1suvv-1)

## Setup Instructions

### 1. Clone the Repository

```
git clone https://github.com/software-students-fall2024/5-final-y2k.git
cd 5-final-y2k
```

### 2. Install pipenv

```
pip install pipenv
```

### 3. Install dependencies

```
pipenv install
```

### 4. Activate the shell

```
pipenv shell
```

### 5. Secure a Google Cloud Service account key.

A tutorial for this step can be found [here](https://cloud.google.com/iam/docs/service-accounts-create).

After completing it, you should have a key file in `.json` format. For easiest use, place it at the root of the project.

### 6. Create a .env file

Example of .env file. 

It must include the mongodb user and password, a flask secret, and the path to the api credentials secured in the previous step.

```
MONGODB_USERNAME= abc123
MONGODB_PASSWORD= abc123
FLASK_SECRET= abc123
GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json
```

***NOTE***: If the credentials file was placed at the root of the project, it is enough to only include its name in the `.env`.

### 7. Build and run docker containers

```
docker compose build
docker compose up
```

***NOTE***: In order for the database to mount correctly, make sure a `data` folder is created at the root of the project. This can be done with `mkdir data` on Linux/MacOS. This also ensures data persists between sessions.

### 8. Stop docker containers

```
docker compose down
```

### Usage

1. Build and launch app using instructions above for setup
2. Access at http://localhost:8080/
3. Start session and record through the web app
4. View the public and private session details

### Container Image on DockerHub

This project utilizes a Docker container to streamline deployment and functionality.  
The container image for this project is available on DockerHub:

[**Container Image on DockerHub**](https://hub.docker.com/r/lucaignatescu/y2k-final-project)

### Deployment

This web app is deployed at https://www.finalproject-y2k.net/

## Project Structure

```text
.
├── __pycache__
├── .github
│   ├── workflows
│   │   ├── event-logger.yml
│   │   ├── publishing.yml
│   │   └── testing.yml
├── data
├── static
│   ├── grid.css
│   ├── record-player.png
│   ├── recording.js
│   ├── styles.css
│   └── Welcome.png
├── templates
│   ├── edit_transcription.html
│   ├── index.html
│   ├── login.html
│   ├── public_files.html
│   ├── record.html
│   ├── register.html
│   └── user_files.html
├── test
│   └── test_test.py
├── .gitignore
├── app.py
├── docker-compose.yml
├── Dockerfile
├── instructions.md
├── LICENSE
├── pipfile.
├── pipfile.lock
├── pyproject.toml
└── README.md
```

## Task Boards

[The Task board for our team](https://github.com/orgs/software-students-fall2024/projects/153)

## Team Members

- [Luca Ignatescu (li2058)](https://github.com/LucaIgnatescu)
- [Neha Magesh (nm3818)](https://github.com/nehamagesh)
- [Nuzhat Bushra(ntb5562)](https://github.com/ntb5562)
- [Tamara Bueno (tb2803)](https://github.com/TamaraBuenoo)

## Notes

This project is meant to be run on Google Chrome. Additionally, for an accurate transcription, please wait 10 seconds before and between starting the recording. [Pro Tip: Wait for all the Docker Containers to Run]

## Acknowledgements

We used online tutorials and forums.
