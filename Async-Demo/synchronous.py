import requests
import time

def fetch_user(user_id):
    print(f"Fetching data for user: {user_id}")
    response = requests.get(
        f"https://jsonplaceholder.typicode.com/users/{user_id}"
    )
    return response.json()

start = time.time()
r1 = fetch_user(1)
r2 = fetch_user(2)
r3 = fetch_user(3)
end = time.time()

print(f"Total time: {end-start:.2f} seconds")