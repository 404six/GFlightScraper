import requests

from gflightscraper.config import DEFAULT_HEADERS

def make_post_request(url, payload):
    """
    Makes a POST request to the specified URL with the given payload.

    :param url: The URL to send the POST request to.
    :param payload: The payload to send in the request body.
    :param headers: Optional headers for the request.
    :return: The response text from the API.
    """
    
    try:
        response = requests.post(url, data=payload, headers=DEFAULT_HEADERS)
        response.raise_for_status()
        return response.text.strip().replace(")]}'", "")

    except requests.exceptions.RequestException as e:
        print(f"Error making POST request: {e}")
        return None