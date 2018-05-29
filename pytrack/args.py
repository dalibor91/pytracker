class Arguments:

    def __init__(self, arguments):
        self.arg = arguments

    def get(self, name, values=1, default=None):
        found = False
        cnt_found  = 0
        data = []
        for i in self.arg:
            if cnt_found == values:
                break

            if found:
                cnt_found+=1
                data.append(i)
                continue

            if i == ("--%s" % name) or i == ("-%s" % name):
                found = True

        while len(data) < values:
            data.append(default)

        return data

    def has(self, name):
        for i in self.arg:
            if i == ("--%s" % name) or i == ("-%s" % name):
                return True

        return False
