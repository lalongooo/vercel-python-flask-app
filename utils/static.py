import json

@staticmethod
def is_message(request) -> bool:
    json_data = json.loads(request.data)
    
    if "entry" in json_data:
        if len(json_data["entry"]) > 0:
            if "changes" in json_data["entry"][0]:
                if len(json_data["entry"][0]["changes"]) > 0:
                    if "value" in json_data["entry"][0]["changes"][0]:
                        if "messages" in json_data["entry"][0]["changes"][0]["value"]:
                            return True
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False

@staticmethod
def is_hub_challenge(data: Dict[Any, Any]) -> bool:
    data = data["entry"][0]["changes"][0]["value"]
    if "messages" in data:
        return True
    return False