def process_response(response_json):
    """
    Processes the response from the backend.
    """
    if "response" in response_json:
        return response_json["response"]
    return ""