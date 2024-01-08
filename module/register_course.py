from colorama import Style, Fore
import json


def register_course(session, url_regist_class_id):
    print(Style.RESET_ALL)
    response = session.get(url_regist_class_id)
    text = response.text
    json_server = json.loads(text)
    msg = json_server["Msg"]
    print(Fore.GREEN + Style.BRIGHT + f"{msg}")
