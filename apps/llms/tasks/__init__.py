import json


def parse_json_response(response_text: str) -> dict:
    try:
        data = json.loads(response_text)
        if not isinstance(data, dict):
            raise ValueError("Parsed JSON is not an object.")
        return data
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON response from OpenAI: {str(e)}")
