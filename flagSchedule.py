import json
from sett import Settings


def getAtt(file_path):
    with open(file=file_path[0], mode='r') as f:
        return json.load(f)


FLAGS_OPERS = {
    "-f": getAtt
}


class FlagSchedule:
    def __init__(self, console_options: {}):
        self.console_options = console_options

    def getDataFromConfig(self) -> None:
        data = FLAGS_OPERS.get("-f")(self.console_options.get("-f"))
        sett = Settings
        for attr, val in data.items():
            setattr(sett, attr, val)


if __name__ == '__main__':
    FlagSchedule({"-f": "config.json"}).getDataFromConfig()
    print("a")
