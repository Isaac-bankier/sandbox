class config(object):
    """docstring for config."""
    def __init__(self, fileName):
        #open file and store lines in variable
        configFile = open(fileName, "r")
        lines = configFile.readlines()
        configFile.close()

        #filter out invalid options
        validLines = []
        for line in lines:
            if line == "":
                continue
            if ";" not in line[1:-2]:
                continue
            validLines.append(line)

        #extract the settings
        self.settings = {}
        for line in validLines:
            line = line.split(";")
            self.settings[line[0]]=line[1][0:-1]

    def getOption(self, option):
        return self.settings[option]

    def setOption(self, option, value):
        self.settings[option] = value
