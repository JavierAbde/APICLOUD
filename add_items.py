import requests
import json

# Create a new item
def add_item(name, description=""):
    url = "http://127.0.0.1:5000/items"
    data = {
        "name": name,
        "description": description
    }
    
    try:
        response = requests.post(url, json=data)
        if response.status_code == 201:
            print(f"✅ Item created successfully!")
            print(f"📋 Response: {response.json()}")
            return response.json()
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure Flask server is running!")
    except Exception as e:
        print(f"❌ Error: {e}")

# Example usage
if __name__ == "__main__":
    print("🚀 Adding items to Flask API...\n")
    
    # Add some example items
    add_item("Laptop", "Dell XPS 13 laptop")
    add_item("Coffee Mug", "Blue ceramic coffee mug")
    add_item("Book", "Python programming guide")
    
    # Get all items to verify
    try:
        response = requests.get("http://127.0.0.1:5000/items")
        if response.status_code == 200:
            items = response.json()
            print(f"\n📋 All items in database:")
            for item in items:
                print(f"  ID {item['id']}: {item['name']} - {item['description']}")
        else:
            print(f"❌ Error getting items: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
