import requests
import json

def test_query(query):
    url = "http://localhost:5000/query"
    headers = {'Content-Type': 'application/json'}
    data = {'query': query}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()

if __name__ == "__main__":
    query = input("Enter your question: ")
    response = test_query(query)
    print("Response:", response)
