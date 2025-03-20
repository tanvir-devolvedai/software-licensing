import requests

def check_subscription_status(user_id):
    try:
        response = requests.get(
            f"https://api.your-service.com/validate/{user_id}",
            timeout=3
        )
        return response.json()["active"]
    except:
        return True  # Graceful degradation