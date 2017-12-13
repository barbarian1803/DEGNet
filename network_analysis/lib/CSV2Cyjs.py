import json
import os.path
import pandas as pd
from django.conf import settings


def get_avail_network(username):
    networks = []

    # load default network
    metadata_default = open(settings.BASE_DIR+"/network_analysis/database/metadata.json", "r")
    default_networks = json.loads(metadata_default.read())["networks"]
    networks = networks + default_networks

    # load user network
    usr_metadata = settings.BASE_DIR+"/user_dir/" + username + "/network/metadata.json"
    if os.path.isfile(usr_metadata):
        metadata_user = open(usr_metadata, "r")
        user_networks = json.loads(metadata_user.read())["networks"]
        networks = networks + user_networks

    return networks

def loadnetwork(username, networkname, fulldata=False):

    networks = get_avail_network(username)

    main_file = ""
    pos_file = ""

    for n in networks:
        if n["id"] == networkname:
            basedir = ""
            if n["type"]=="default":
                basedir = settings.BASE_DIR+"/network_analysis/database/"
            elif n["type"]=="user":
                basedir = settings.BASE_DIR+"/user_dir/"+username+"/network/"

            main_file = basedir + n["main_file"]
            pos_file = basedir + n["pos_file"]
            break

    if main_file == "":
        return False

    return csv2cyjs(main_file, pos_file, fulldata)

def getNodeData(id, geneDB):
    retval = {"id": id, "name": id}

    row = geneDB.loc[(geneDB["symbol"] == id) | (geneDB["ensembl"] == id) | (str(geneDB["entrez"]) == str(id))]

    if not row.empty:
        retval["ensembl"] =row["ensembl"].max()
        retval["symbol"] = row["symbol"].max()
        retval["entrez"] = str(row["entrez"].max())
    else:
        retval["ensembl"] = id
        retval["symbol"] = id
        retval["entrez"] = id
    return retval


def csv2cyjs(network_file,network_pos_file,fulldata=False):
    gene_id_file = settings.BASE_DIR + "/network_analysis/external_database/all_gene_id_bak.csv"

    geneDB = pd.read_csv(gene_id_file, sep="\t", header=0)
    geneDB = geneDB.drop_duplicates(["ensembl", "symbol", "entrez"])

    nodes = []
    edges = []

    main = pd.read_csv(network_file, sep="\t", header=0)

    try:
        pos = pd.read_csv(network_pos_file, sep="\t", header=0)
        for index, row in pos.iterrows():

            obj_node = {"position": {"x": row[1], "y": row[2]}, "data": getNodeData(row[0], geneDB)}
            nodes.append(obj_node)
    except:
        nodeset = set()
        for index, row in main.iterrows():
            source = row["Source"]
            target = row["Target"]

            if source not in nodeset:
                nodeset.add(source)

                obj_node = {"data": getNodeData(source, geneDB)}
                nodes.append(obj_node)

            if target not in nodeset:
                nodeset.add(target)

                obj_node = {"data": getNodeData(target, geneDB)}
                nodes.append(obj_node)

    for index, row in main.iterrows():
        obj_edge = { "data": {"source": row["Source"], "interaction": row["Type"], "target": row["Target"], "name": row["Source"]+"-"+row["Target"], "id": row["Source"]+"-"+row["Target"]}}
        edges.append(obj_edge)

    cyjs_obj = {"nodes": nodes, "edges": edges}

    if fulldata:
        cyjs_obj = {"data": {"name": network_file}, "elements": cyjs_obj}
    return json.dumps(cyjs_obj)