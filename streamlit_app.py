import streamlit as st
import requests


# =========================================================
# CONFIGURATION
# =========================================================

API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="PetConnect",
    page_icon="🐾",
    layout="wide"
)


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 45px;
        font-weight: bold;
        margin-bottom: 0px;
    }

    .subtitle {
        font-size: 18px;
        color: gray;
        margin-bottom: 30px;
    }

    .pet-card {
        padding: 15px;
        border-radius: 15px;
        border: 1px solid #ddd;
        margin-bottom: 20px;
    }

    .success-box {
        padding: 15px;
        border-radius: 10px;
        background-color: #d4edda;
        color: #155724;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# API FUNCTION
# =========================================================

def api_request(method, endpoint, **kwargs):

    try:

        response = requests.request(
            method,
            API_URL + endpoint,
            timeout=5,
            **kwargs
        )

        if response.status_code >= 400:

            st.error(response.json().get(
                "detail",
                "Something went wrong"
            ))

            return None

        return response.json()

    except requests.exceptions.ConnectionError:

        st.error(
            "❌ Cannot connect to FastAPI.\n\n"
            "Please make sure backend.py is running."
        )

        return None

    except Exception as e:

        st.error(f"Error: {e}")

        return None


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🐾 PetConnect")

st.sidebar.write(
    "Pet Adoption & Matching System"
)

menu = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "🐶 Pet Gallery",
        "❤️ Find My Match",
        "🔍 Search Pets",
        "📝 Adoption Application",
        "📋 My Applications",
        "➕ Add Pet",
        "👨‍💼 Admin Dashboard"
    ]
)


# =========================================================
# DASHBOARD
# =========================================================

if menu == "🏠 Dashboard":

    st.markdown(
        '<div class="main-title">🐾 PetConnect</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Find a loving pet and give them a forever home ❤️'
        '</div>',
        unsafe_allow_html=True
    )

    pets = api_request(
        "GET",
        "/pets"
    )

    if pets:

        available = [
            p for p in pets
            if p["status"] == "Available"
        ]

        adopted = [
            p for p in pets
            if p["status"] == "Adopted"
        ]

        dogs = [
            p for p in pets
            if p["species"] == "Dog"
        ]

        cats = [
            p for p in pets
            if p["species"] == "Cat"
        ]

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "🐾 Total Pets",
            len(pets)
        )

        col2.metric(
            "💚 Available",
            len(available)
        )

        col3.metric(
            "🐶 Dogs",
            len(dogs)
        )

        col4.metric(
            "🐱 Cats",
            len(cats)
        )

        st.divider()

        st.subheader("🌟 Featured Pets")

        cols = st.columns(3)

        for i, pet in enumerate(available[:3]):

            with cols[i]:

                st.image(
                    pet["image"],
                    use_container_width=True
                )

                st.subheader(
                    f"{pet['name']} 🐾"
                )

                st.write(
                    f"**Breed:** {pet['breed']}"
                )

                st.write(
                    f"**Age:** {pet['age']} years"
                )

                st.write(
                    f"**Location:** {pet['location']}"
                )


# =========================================================
# PET GALLERY
# =========================================================

elif menu == "🐶 Pet Gallery":

    st.title("🐶 Pet Gallery")

    pets = api_request(
        "GET",
        "/pets/available"
    )

    if pets:

        cols = st.columns(3)

        for i, pet in enumerate(pets):

            with cols[i % 3]:

                st.image(
                    pet["image"],
                    use_container_width=True
                )

                st.subheader(
                    f"{pet['name']} 🐾"
                )

                st.write(
                    f"**{pet['breed']}**"
                )

                st.write(
                    f"Age: {pet['age']} years"
                )

                st.write(
                    f"Gender: {pet['gender']}"
                )

                st.write(
                    f"📍 {pet['location']}"
                )

                st.write(
                    f"🏠 {pet['home']}"
                )

                st.success(
                    "Available for Adoption"
                )


# =========================================================
# FIND MY MATCH
# =========================================================

elif menu == "❤️ Find My Match":

    st.title("❤️ Find Your Perfect Pet")

    st.write(
        "Tell us about yourself and we'll find pets "
        "that match your lifestyle."
    )

    with st.form("matching_form"):

        name = st.text_input(
            "Your Name"
        )

        email = st.text_input(
            "Email"
        )

        city = st.text_input(
            "Your City"
        )

        species = st.selectbox(
            "Preferred Pet",
            [
                "Dog",
                "Cat"
            ]
        )

        preferred_age = st.number_input(
            "Preferred Pet Age",
            min_value=0,
            max_value=20,
            value=2
        )

        gender = st.selectbox(
            "Gender Preference",
            [
                "Any",
                "Male",
                "Female"
            ]
        )

        home = st.selectbox(
            "Your Home",
            [
                "Apartment",
                "House"
            ]
        )

        activity = st.selectbox(
            "Your Activity Level",
            [
                "Low",
                "Medium",
                "High"
            ]
        )

        submitted = st.form_submit_button(
            "❤️ Find My Matches"
        )

    if submitted:

        if not name or not email or not city:

            st.warning(
                "Please fill all required details."
            )

        else:

            user_data = {
                "name": name,
                "email": email,
                "city": city,
                "species": species,
                "preferred_age": preferred_age,
                "gender_preference": gender,
                "home": home,
                "activity": activity
            }

            api_request(
                "POST",
                "/users",
                json=user_data
            )

            matches = api_request(
                "POST",
                "/match",
                json=user_data
            )

            if matches:

                st.success(
                    f"We found {len(matches)} potential matches!"
                )

                for pet in matches[:5]:

                    score = pet["match_score"]

                    st.divider()

                    col1, col2 = st.columns(
                        [1, 2]
                    )

                    with col1:

                        st.image(
                            pet["image"],
                            use_container_width=True
                        )

                    with col2:

                        st.subheader(
                            f"{pet['name']} 🐾"
                        )

                        st.write(
                            f"**Breed:** {pet['breed']}"
                        )

                        st.write(
                            f"**Age:** {pet['age']} years"
                        )

                        st.write(
                            f"**Location:** {pet['location']}"
                        )

                        st.write(
                            f"**Home:** {pet['home']}"
                        )

                        st.write(
                            f"**Activity:** {pet['activity']}"
                        )

                        st.progress(
                            score / 100
                        )

                        st.write(
                            f"❤️ Match Score: **{score}%**"
                        )


# =========================================================
# SEARCH PETS
# =========================================================

elif menu == "🔍 Search Pets":

    st.title("🔍 Search Pets")

    col1, col2, col3 = st.columns(3)

    with col1:

        species = st.selectbox(
            "Species",
            [
                "All",
                "Dog",
                "Cat"
            ]
        )

    with col2:

        location = st.text_input(
            "Location"
        )

    with col3:

        breed = st.text_input(
            "Breed"
        )

    if st.button("🔍 Search"):

        params = {}

        if species != "All":
            params["species"] = species

        if location:
            params["location"] = location

        if breed:
            params["breed"] = breed

        pets = api_request(
            "GET",
            "/search",
            params=params
        )

        if pets:

            st.success(
                f"{len(pets)} pet(s) found."
            )

            for pet in pets:

                col1, col2 = st.columns(
                    [1, 3]
                )

                with col1:

                    st.image(
                        pet["image"],
                        use_container_width=True
                    )

                with col2:

                    st.subheader(
                        pet["name"]
                    )

                    st.write(
                        f"Breed: {pet['breed']}"
                    )

                    st.write(
                        f"Age: {pet['age']}"
                    )

                    st.write(
                        f"Location: {pet['location']}"
                    )

                    st.write(
                        f"Gender: {pet['gender']}"
                    )

        else:

            st.info(
                "No pets found."
            )


# =========================================================
# ADOPTION APPLICATION
# =========================================================

elif menu == "📝 Adoption Application":

    st.title("📝 Adoption Application")

    pets = api_request(
        "GET",
        "/pets/available"
    )

    if pets:

        pet_options = {
            f"{p['name']} - {p['breed']} "
            f"({p['location']})": p["id"]
            for p in pets
        }

        selected_pet = st.selectbox(
            "Select Pet",
            list(pet_options.keys())
        )

        with st.form("adoption_form"):

            applicant_name = st.text_input(
                "Your Name"
            )

            email = st.text_input(
                "Email"
            )

            phone = st.text_input(
                "Phone Number"
            )

            city = st.text_input(
                "City"
            )

            reason = st.text_area(
                "Why do you want to adopt this pet?"
            )

            submit = st.form_submit_button(
                "Submit Application ❤️"
            )

        if submit:

            if not applicant_name or not email or not phone:

                st.warning(
                    "Please fill all required fields."
                )

            else:

                application_data = {

                    "pet_id":
                        pet_options[selected_pet],

                    "applicant_name":
                        applicant_name,

                    "email":
                        email,

                    "phone":
                        phone,

                    "city":
                        city,

                    "reason":
                        reason
                }

                result = api_request(
                    "POST",
                    "/applications",
                    json=application_data
                )

                if result:

                    st.success(
                        "🎉 Adoption application "
                        "submitted successfully!"
                    )

                    st.info(
                        "Application Status: Pending"
                    )


# =========================================================
# MY APPLICATIONS
# =========================================================

elif menu == "📋 My Applications":

    st.title("📋 My Applications")

    email = st.text_input(
        "Enter your email"
    )

    if st.button("🔍 Check Applications"):

        if email:

            applications = api_request(
                "GET",
                "/applications/search",
                params={
                    "email": email
                }
            )

            if applications:

                for application in applications:

                    st.divider()

                    st.subheader(
                        f"Application #{application['id']}"
                    )

                    st.write(
                        f"Pet ID: {application['pet_id']}"
                    )

                    st.write(
                        f"Applicant: "
                        f"{application['applicant_name']}"
                    )

                    st.write(
                        f"Email: {application['email']}"
                    )

                    status = application["status"]

                    if status == "Pending":

                        st.warning(
                            "⏳ Pending"
                        )

                    elif status == "Approved":

                        st.success(
                            "✅ Approved"
                        )

                    else:

                        st.error(
                            "❌ Rejected"
                        )

            else:

                st.info(
                    "No applications found."
                )


# =========================================================
# ADD PET
# =========================================================

elif menu == "➕ Add Pet":

    st.title("➕ Add a Pet")

    with st.form("add_pet_form"):

        name = st.text_input(
            "Pet Name"
        )

        species = st.selectbox(
            "Species",
            [
                "Dog",
                "Cat"
            ]
        )

        breed = st.text_input(
            "Breed"
        )

        age = st.number_input(
            "Age",
            min_value=0,
            max_value=30,
            value=1
        )

        gender = st.selectbox(
            "Gender",
            [
                "Male",
                "Female"
            ]
        )

        location = st.text_input(
            "Location"
        )

        home = st.selectbox(
            "Suitable Home",
            [
                "Apartment",
                "House"
            ]
        )

        activity = st.selectbox(
            "Activity Level",
            [
                "Low",
                "Medium",
                "High"
            ]
        )

        image = st.text_input(
            "Pet Image URL",
            placeholder="https://..."
        )

        submit = st.form_submit_button(
            "➕ Add Pet"
        )

    if submit:

        if not name or not breed or not location:

            st.warning(
                "Please fill all required fields."
            )

        else:

            pet_data = {

                "name": name,
                "species": species,
                "breed": breed,
                "age": age,
                "gender": gender,
                "location": location,
                "home": home,
                "activity": activity,
                "image": image
            }

            result = api_request(
                "POST",
                "/pets",
                json=pet_data
            )

            if result:

                st.success(
                    f"🎉 {name} added successfully!"
                )


# =========================================================
# ADMIN DASHBOARD
# =========================================================

elif menu == "👨‍💼 Admin Dashboard":

    st.title("👨‍💼 Admin Dashboard")

    applications = api_request(
        "GET",
        "/applications"
    )

    pets = api_request(
        "GET",
        "/pets"
    )

    if applications is not None and pets is not None:

        available = len([
            p for p in pets
            if p["status"] == "Available"
        ])

        adopted = len([
            p for p in pets
            if p["status"] == "Adopted"
        ])

        pending = len([
            a for a in applications
            if a["status"] == "Pending"
        ])

        approved = len([
            a for a in applications
            if a["status"] == "Approved"
        ])

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "🐾 Total Pets",
            len(pets)
        )

        col2.metric(
            "💚 Available",
            available
        )

        col3.metric(
            "🏠 Adopted",
            adopted
        )

        col4.metric(
            "⏳ Pending",
            pending
        )

        st.divider()

        st.subheader(
            "📋 Adoption Applications"
        )

        if applications:

            for application in applications:

                st.divider()

                col1, col2 = st.columns(
                    [3, 1]
                )

                with col1:

                    st.write(
                        f"### Application "
                        f"#{application['id']}"
                    )

                    st.write(
                        f"**Applicant:** "
                        f"{application['applicant_name']}"
                    )

                    st.write(
                        f"**Email:** "
                        f"{application['email']}"
                    )

                    st.write(
                        f"**Phone:** "
                        f"{application['phone']}"
                    )

                    st.write(
                        f"**Pet ID:** "
                        f"{application['pet_id']}"
                    )

                    st.write(
                        f"**Reason:** "
                        f"{application['reason']}"
                    )

                    st.write(
                        f"**Status:** "
                        f"{application['status']}"
                    )

                with col2:

                    if application["status"] == "Pending":

                        if st.button(
                            "✅ Approve",
                            key=f"approve_{application['id']}"
                        ):

                            result = api_request(
                                "PUT",
                                f"/applications/"
                                f"{application['id']}/approve"
                            )

                            if result:

                                st.success(
                                    "Application approved!"
                                )

                                st.rerun()

                        if st.button(
                            "❌ Reject",
                            key=f"reject_{application['id']}"
                        ):

                            result = api_request(
                                "PUT",
                                f"/applications/"
                                f"{application['id']}/reject"
                            )

                            if result:

                                st.warning(
                                    "Application rejected."
                                )

                                st.rerun()

        else:

            st.info(
                "No applications yet."
            )