from typing import List

from app.flagSchedule import FlagSchedule

FLAGS = {
    "-f": 1
}

CONSOLE_OPTIONS = {}
REQUIRED_FLAGS = ["-f"]


class Console:
    def __init__(self, args: List[str]):
        self.args = args[1:]

    def getData(self):
        builder = Abstract().start()
        for arg in self.args:
            builder = builder.add_attr(arg)

    def canRun(self):
        self.getData()
        for rq_flags in REQUIRED_FLAGS:
            if rq_flags not in CONSOLE_OPTIONS.keys():
                raise SystemExit(f"Required flags: {REQUIRED_FLAGS}")
        FlagSchedule(CONSOLE_OPTIONS).getDataFromConfig()
        return True


class Abstract:
    def start(self):
        return Flag()

    def add_attr(self, attr):
        pass


class Flag(Abstract):
    def add_attr(self, attr):
        CONSOLE_OPTIONS.update({attr: []})
        if attr not in FLAGS:
            raise SystemExit(f"Wrong flag: {attr}")
        if FLAGS.get(attr) > 0:
            return Args(attr)
        else:
            return Flag()


class Args(Abstract):
    def __init__(self, flag):
        self.flag = flag

    def add_attr(self, attr):
        if attr in FLAGS:
            raise SystemExit(f"Wrong options for {self.flag} flag!")
        args_array = CONSOLE_OPTIONS.get(self.flag)
        args_array.append(attr)
        CONSOLE_OPTIONS.update({self.flag: args_array})
        if FLAGS.get(self.flag) > len(args_array):
            return Args(self.flag)
        else:
            return Flag()
