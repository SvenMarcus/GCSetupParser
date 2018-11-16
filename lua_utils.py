class LuaTable:

    def __init__(self):
        self.__table = dict()
        self.__index = 0


    def add(self, key=None, value=None):
        if isinstance(value, str):
            value = "\"" + value + "\""

        if key is None:
            self.__index += 1
            key = self.__index
        
        self.__table[key] = value

    def get(self, key):
        return self.__table[key]

    def __str__(self):
        result = "{"

        for k, v in self.__table.items():
            if isinstance(k, int):
                result += "\n\t" + str(v).replace("\n", "\n\t") + ","
                continue

            result += "\n\t" + str(k) + "=" + str(v).replace("\n", "\n\t") + ","

        if len(result) > 1:
            result += "\n"

        result += "}"

        return result


class FunctionCall:

    def __init__(self, name, *args):
        self.name = name
        self.args = args

    def __str__(self):
        result = self.name + "("
        resultLength = len(result)
        for arg in self.args:
            if isinstance(arg, str):
                arg = "\"" + arg + "\""

            result += str(arg) + ","
        
        if len(result) > resultLength:
            partition = result.rpartition(",")
            result = partition[0]

        result += ")"

        return str(result)