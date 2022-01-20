import base64
config = {
    "serverHostName": "localhost",
    "serverPort": 5000,
    "timeOut": 60,
    "managers": {
        "adam": b'ZXZl'
    }
}


def getConfig(x: str):
    if(x in config):
        return config[x]
    else:
        return


def isManager(username: str, password: str) -> bool:
    return (username in config["managers"]
            and
            base64.b64decode(config["managers"][username]) == password.encode())
