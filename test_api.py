import requests
import json

# Base URL for the API
base_url = "http://localhost:5000"

print("=== Testing Flask API ===\n")

try:
    # Test 1: Get all items (should be empty initially)
    print("1. Getting all items:")
    response = requests.get(f"{base_url}/items")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

    # Test 2: Create a new item
    print("2. Creating a new item:")
    new_item = {"name": "Test Item", "description": "This is a test item"}
    response = requests.post(f"{base_url}/items", json=new_item)
    print(f"Status Code: {response.status_code}")
    created_item = response.json()
    print(f"Response: {created_item}")
    item_id = created_item["id"]
    print()

    # Test 3: Get all items again (should show the new item)
    print("3. Getting all items after creation:")
    response = requests.get(f"{base_url}/items")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

    # Test 4: Get specific item
    print(f"4. Getting item with ID {item_id}:")
    response = requests.get(f"{base_url}/items/{item_id}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

    # Test 5: Update the item
    print(f"5. Updating item with ID {item_id}:")
    updated_item = {"name": "Updated Test Item", "description": "This item has been updated"}
    response = requests.put(f"{base_url}/items/{item_id}", json=updated_item)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

    # Test 6: Get the updated item
    print(f"6. Getting updated item with ID {item_id}:")
    response = requests.get(f"{base_url}/items/{item_id}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

    # Test 7: Delete the item
    print(f"7. Deleting item with ID {item_id}:")
    response = requests.delete(f"{base_url}/items/{item_id}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

    # Test 8: Try to get the deleted item (should return 404)
    print(f"8. Trying to get deleted item with ID {item_id}:")
    response = requests.get(f"{base_url}/items/{item_id}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

except requests.exceptions.ConnectionError:
    print("Error: Could not connect to the API. Make sure the Flask server is running on http://localhost:5000")
except Exception as e:
    print(f"Error: {e}")
