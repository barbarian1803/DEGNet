class GeneralUtil:

    @staticmethod
    def readGeneIDDatabase(fileName, key):
        key_db = {"ensembl": 0, "symbol": 1, "entrez": 2, "uniprot": 3}
        data = {}
        csv1 = open(fileName)



        for line in csv1:
            if "ensembl" in line:
                continue

            array = line.strip().split("\t")

            id = array[key_db[key]]

            if id not in data:
                data[id] = {}

            data[id] = {"ensembl": array[0], "symbol": array[1], "entrez": array[2]}

            try:
                data[id]["uniprot"] = array[3]
            except:
                data[id]["uniprot"] = ""
        return data