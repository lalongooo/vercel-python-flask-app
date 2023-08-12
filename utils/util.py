import json

class Util:

    @staticmethod
    def is_message(request) -> bool:
        try:
            json_data = json.loads(request.data)
            return json_data["entry"][0]["changes"][0]["value"]["messages"]
        except Exception:
            return False

    @staticmethod
    def get_author(request) -> str:
        try:
            json_data = json.loads(request.data)
            return json_data["entry"][0]["changes"][0]["value"]["metadata"]["phone_number_id"]
        except Exception:
            return None