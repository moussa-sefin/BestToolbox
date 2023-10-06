# utils.py

def jwt_response_payload_handler(token, user=None, request=None):
    print("jwt_response_payload_handler called")
    # Customize the response payload as needed
    return {
        'token': token,
        'user_id': user.id if user else None,
        # Include other user-related data if needed
    }
