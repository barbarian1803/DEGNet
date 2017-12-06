import re

class GOAFParser:

    def __init__(self,fname):
        self.fname = fname
        self.file = open(fname)
        self.data = {}


    def parse(self):
        print "Parsing goaf file "+self.fname+"..."
        for line in self.file:
            if line[0]=="!":
                ##skip header
                continue

            array_data = re.split('; |, |\t',line.strip())
            if array_data[1] not in self.data:
                self.data[array_data[1]] = []
            self.data[array_data[1]].append(array_data)
        return self.data