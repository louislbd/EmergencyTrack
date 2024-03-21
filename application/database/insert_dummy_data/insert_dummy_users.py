import requests


# Function to fetch data from the API
def get_data(url):
    response = requests.get(url)
    data = response.json()
    return data


# Function to register dummy users
def register_users(departments_data):
    for department in departments_data:
        email = f"{int(department['county'])}_{department['department_id']}@officer-dummy.com"
        password = "password"
        first_name = f"{department['county_name'].strip()}{department['department_name']}"
        last_name = "Officer"

        user_data = {
            "email": email,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "account_type": "1"
        }

        register_url = "http://localhost:8000/api/register"
        response = requests.post(register_url, json=user_data)

        if response.status_code == 201:
            print(f"User {email} registered successfully")
        else:
            print(f"Failed to register user {email}")


if __name__ == '__main__':
    # api urls
    departments_api_url = "http://localhost:8000/api/departments"

    # Fetch data from the API
    departments_data = get_data(departments_api_url)

    # Register dummy users
    register_users(departments_data)
