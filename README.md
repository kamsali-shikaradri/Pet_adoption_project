# 🐾 PetConnect – Pet Adoption & Matching Platform

## 📌 Project Overview

PetConnect is a pet adoption and matching platform developed using Python and FastAPI.

The project helps users find available pets and provides an API-based system for managing pet and user information.

## 🎯 Problem Statement

Finding suitable pets for adoption can be difficult because information is often scattered across different sources.

PetConnect provides a centralized system where users can manage pet information, search available pets, and find suitable matches.

## 🚀 Features

* User registration
* Add pet details
* View available pets
* Search pets
* Get pet details
* Update pet information
* Delete pet information
* Pet matching
* Interactive API documentation
* Streamlit interface

## 🛠️ Technologies Used

* Python
* FastAPI
* Uvicorn
* Streamlit
* REST API
* Swagger UI / OpenAPI
* Git
* GitHub

## 📡 API Endpoints

### User APIs

* `POST /users`
* `GET /users`
* `GET /users/{user_id}`

### Pet APIs

* `POST /pets`
* `GET /pets`
* `GET /pets/{pet_id}`
* `PUT /pets/{pet_id}`
* `DELETE /pets/{pet_id}`

### Matching

* `GET /match`

## 📚 Swagger UI

After starting the FastAPI server, open:

`http://127.0.0.1:8000/docs`

Swagger UI allows you to test and explore all available API endpoints.

## ▶️ How to Run

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Open the project

```bash
cd PetConnect
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

Windows:

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Start FastAPI

```bash
uvicorn main:app --reload
```

### 7. Open Swagger UI

```text
http://127.0.0.1:8000/docs
```

## 📊 Streamlit

Run the Streamlit application using:

```bash
streamlit run app.py
```

## 💡 What I Learned

Through this project, I learned:

* Building REST APIs using FastAPI
* Creating GET, POST, PUT and DELETE endpoints
* Request and response handling
* Data validation
* Swagger UI documentation
* Running applications using Uvicorn
* Connecting a frontend/dashboard with an API
* Git and GitHub version control
* Structuring a real-world Python project

## 🔮 Future Enhancements

* User authentication
* Database integration
* Advanced pet matching
* Image upload
* Location-based pet search
* Cloud deployment 
* Improved UI

## 👨‍💻 Author

Kamsali Shikaradri
