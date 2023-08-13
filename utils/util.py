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
            return json_data["entry"][0]["changes"][0]["value"]["messages"][0]["from"].replace("521", "52")
        except Exception:
            return None

    @staticmethod
    def is_interactive_list_reply(request) -> bool:
        try:
            json_data = json.loads(request.data)
            if (json_data["entry"][0]["changes"][0]["value"]["messages"][0]["interactive"]["type"] == "list_reply"):
                return True
            return False
        except Exception:
            return False

    @staticmethod
    def get_interactive_reply(request) -> str | None:
        try:
            json_data = json.loads(request.data)
            return json_data["entry"][0]["changes"][0]["value"]["messages"][0]["interactive"]
        except Exception:
            return None