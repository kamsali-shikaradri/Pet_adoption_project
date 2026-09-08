from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import json
import os

app = FastAPI(
    title="PetConnect API",
    description="Pet Adoption and Matching System",
    version="1.0"
)

DATA_FILE = "petconnect_data.json"


# =========================================================
# DATA
# =========================================================

default_data = {
    "pets": [
        {
            "id": 1,
            "name": "Bruno",
            "species": "Dog",
            "breed": "Labrador",
            "age": 2,
            "gender": "Male",
            "location": "Hyderabad",
            "home": "House",
            "activity": "High",
            "status": "Available",
            "image": "https://images.unsplash.com/photo-1552053831-71594a27632d?w=800"
        },
        {
            "id": 2,
            "name": "Bella",
            "species": "Dog",
            "breed": "Golden Retriever",
            "age": 3,
            "gender": "Female",
            "location": "Bangalore",
            "home": "House",
            "activity": "Medium",
            "status": "Available",
            "image": "https://images.unsplash.com/photo-1552053831-71594a27632d?w=800"
        },
        {
            "id": 3,
            "name": "Rocky",
            "species": "Dog",
            "breed": "German Shepherd",
            "age": 4,
            "gender": "Male",
            "location": "Hyderabad",
            "home": "House",
            "activity": "High",
            "status": "Available",
            "image": "https://images.unsplash.com/photo-1568572933382-74d440642117?w=800"
        },
        {
            "id": 4,
            "name": "Coco",
            "species": "Dog",
            "breed": "Beagle",
            "age": 2,
            "gender": "Female",
            "location": "Hyderabad",
            "home": "Apartment",
            "activity": "Medium",
            "status": "Available",
            "image": "https://images.unsplash.com/photo-1507146426996-ef05306b995a?w=800"
        },
        {
            "id": 5,
            "name": "Milo",
            "species": "Cat",
            "breed": "Persian",
            "age": 1,
            "gender": "Male",
            "location": "Hyderabad",
            "home": "Apartment",
            "activity": "Low",
            "status": "Available",
            "image": "https://images.unsplash.com/photo-1518791841217-8f162f1e1131?w=800"
        },
        {
            "id": 6,
            "name": "Luna",
            "species": "Cat",
            "breed": "Siamese",
            "age": 2,
            "gender": "Female",
            "location": "Chennai",
            "home": "Apartment",
            "activity": "Medium",
            "status": "Available",
            "image": "https://images.unsplash.com/photo-1573865526739-10659fec78a5?w=800"
        }
    ],
    "applications": [],
    "users": []
}


def load_data():

    if not os.path.exists(DATA_FILE):

        with open(DATA_FILE, "w") as file:
            json.dump(default_data, file, indent=4)

        return default_data

    try:

        with open(DATA_FILE, "r") as file:
            return json.load(file)

    except:
        return default_data


data = load_data()


def save_data():

    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


# =========================================================
# MODELS
# =========================================================

class User(BaseModel):
    name: str
    email: str
    city: str
    species: str
    preferred_age: int
    gender_preference: str
    home: str
    activity: str


class Pet(BaseModel):
    name: str
    species: str
    breed: str
    age: int
    gender: str
    location: str
    home: str
    activity: str
    image: Optional[str] = None


class Application(BaseModel):
    pet_id: int
    applicant_name: str
    email: str
    phone: str
    city: str
    reason: str


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():

    return {
        "message": "PetConnect API is running successfully!"
    }


# =========================================================
# GET ALL PETS
# =========================================================

@app.get("/pets")
def get_pets():

    return data["pets"]


# =========================================================
# GET AVAILABLE PETS
# =========================================================

@app.get("/pets/available")
def available_pets():

    return [
        pet for pet in data["pets"]
        if pet["status"] == "Available"
    ]


# =========================================================
# GET SINGLE PET
# =========================================================

@app.get("/pets/{pet_id}")
def get_pet(pet_id: int):

    for pet in data["pets"]:

        if pet["id"] == pet_id:
            return pet

    raise HTTPException(
        status_code=404,
        detail="Pet not found"
    )


# =========================================================
# ADD USER
# =========================================================

@app.post("/users")
def add_user(user: User):

    new_user = user.model_dump()

    new_user["id"] = len(data["users"]) + 1

    data["users"].append(new_user)

    save_data()

    return {
        "message": "User profile created successfully",
        "user": new_user
    }


# =========================================================
# ADD PET
# =========================================================

@app.post("/pets")
def add_pet(pet: Pet):

    new_pet = pet.model_dump()

    new_pet["id"] = (
        max([p["id"] for p in data["pets"]], default=0) + 1
    )

    new_pet["status"] = "Available"

    if not new_pet["image"]:
        new_pet["image"] = (
            "https://images.unsplash.com/"
            "photo-1552053831-71594a27632d?w=800"
        )

    data["pets"].append(new_pet)

    save_data()

    return {
        "message": "Pet added successfully",
        "pet": new_pet
    }


# =========================================================
# SEARCH PETS
# =========================================================

@app.get("/search")
def search_pets(
    species: Optional[str] = None,
    location: Optional[str] = None,
    breed: Optional[str] = None
):

    results = []

    for pet in data["pets"]:

        if pet["status"] != "Available":
            continue

        if species and pet["species"].lower() != species.lower():
            continue

        if location and location.lower() not in pet["location"].lower():
            continue

        if breed and breed.lower() not in pet["breed"].lower():
            continue

        results.append(pet)

    return results


# =========================================================
# PET MATCHING
# =========================================================

@app.post("/match")
def find_matches(user: User):

    matches = []

    for pet in data["pets"]:

        if pet["status"] != "Available":
            continue

        score = 0

        # Species - 30 points
        if pet["species"].lower() == user.species.lower():
            score += 30

        # Age - 20 points
        age_difference = abs(
            pet["age"] - user.preferred_age
        )

        if age_difference == 0:
            score += 20

        elif age_difference == 1:
            score += 15

        elif age_difference == 2:
            score += 10

        # Gender - 10 points
        if (
            user.gender_preference == "Any"
            or pet["gender"].lower()
            == user.gender_preference.lower()
        ):
            score += 10

        # Location - 10 points
        if pet["location"].lower() == user.city.lower():
            score += 10

        # Home - 15 points
        if pet["home"].lower() == user.home.lower():
            score += 15

        # Activity - 15 points
        if pet["activity"].lower() == user.activity.lower():
            score += 15

        pet_result = pet.copy()

        pet_result["match_score"] = score

        matches.append(pet_result)

    matches.sort(
        key=lambda x: x["match_score"],
        reverse=True
    )

    return matches


# =========================================================
# ADOPTION APPLICATION
# =========================================================

@app.post("/applications")
def create_application(application: Application):

    pet = None

    for p in data["pets"]:

        if p["id"] == application.pet_id:
            pet = p
            break

    if pet is None:

        raise HTTPException(
            status_code=404,
            detail="Pet not found"
        )

    if pet["status"] != "Available":

        raise HTTPException(
            status_code=400,
            detail="This pet is no longer available"
        )

    new_application = application.model_dump()

    new_application["id"] = (
        max(
            [a["id"] for a in data["applications"]],
            default=0
        ) + 1
    )

    new_application["status"] = "Pending"

    data["applications"].append(new_application)

    save_data()

    return {
        "message": "Application submitted successfully",
        "application": new_application
    }


# =========================================================
# GET APPLICATIONS
# =========================================================

@app.get("/applications")
def get_applications():

    return data["applications"]


# =========================================================
# SEARCH APPLICATION BY EMAIL
# =========================================================

@app.get("/applications/search")
def search_applications(email: str):

    return [
        application
        for application in data["applications"]
        if application["email"].lower() == email.lower()
    ]


# =========================================================
# APPROVE APPLICATION
# =========================================================

@app.put("/applications/{application_id}/approve")
def approve_application(application_id: int):

    application = None

    for a in data["applications"]:

        if a["id"] == application_id:
            application = a
            break

    if application is None:

        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    application["status"] = "Approved"

    for pet in data["pets"]:

        if pet["id"] == application["pet_id"]:
            pet["status"] = "Adopted"

    save_data()

    return {
        "message": "Application approved successfully"
    }


# =========================================================
# REJECT APPLICATION
# =========================================================

@app.put("/applications/{application_id}/reject")
def reject_application(application_id: int):

    application = None

    for a in data["applications"]:

        if a["id"] == application_id:
            application = a
            break

    if application is None:

        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    application["status"] = "Rejected"

    save_data()

    return {
        "message": "Application rejected"
    }


# =========================================================
# RUN FASTAPI
# =========================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8001
    )