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
            if n["type"] == "default":
                basedir = settings.BASE_DIR+"/network_analysis/database/"
            elif n["type"] == "user":
                basedir = settings.BASE_DIR+"/user_dir/"+username+"/network/"

            main_file = basedir + n["main_file"]
            pos_file = basedir + n["pos_file"]
            break

    if main_file == "":
        return False

    return csv2cyjs(main_file, pos_file, fulldata)

def getNodeData(row):
    retval = {"id": row[0], "name": row[0]}
    key = {3: "ensembl", 4: "symbol", 5: "entrez"}
    for i in range(3, 6):
        if row[i] == row[i]:
            retval[key[i]] = row[i]
        else:
            retval[key[i]] = row[0]
    return retval


def csv2cyjs(network_file,network_pos_file,fulldata=False):
    # read gene id database
    gene_id_file = settings.BASE_DIR + "/network_analysis/external_database/all_gene_id.csv"

    geneDB = pd.read_csv(gene_id_file, sep="\t", header=0)

    # read network file
    main = pd.read_csv(network_file, sep="\t", header=0)

    nodes = []
    edges = []

    try:
        # read pos file if exists
        pos = pd.read_csv(network_pos_file, sep="\t", header=0)
    except:
        pos = pd.DataFrame(columns=["Node", "PosX", "PosY"])
        for index, row in main.iterrows():
            data = [{"Node": row["Source"], "PosX": 0, "PosY": 0}, {"Node": row["Target"], "PosX": 0, "PosY": 0}]
            pos = pos.append(data, ignore_index=True)

    # merge depend on the network gene identifier, now it is set to ensembl
    pos = pd.merge(pos, geneDB, how="left", left_on="Node", right_on="ensembl")
    pos = pos.drop_duplicates(subset=["Node", "PosX", "PosY"])

    for index, row in pos.iterrows():
        obj_node = {"position": {"x": row[1], "y": row[2]}, "data": getNodeData(row)}
        nodes.append(obj_node)

    for index, row in main.iterrows():

        obj_edge = { "data": {"source": row["Source"], "interaction": row["Type"], "target": row["Target"], "name": row["Source"]+"-"+row["Target"], "id": row["Source"]+"-"+row["Target"]}}
        edges.append(obj_edge)
    cyjs_obj = {"nodes": nodes, "edges": edges}

    if fulldata:
        cyjs_obj = {"data": {"name": network_file}, "elements": cyjs_obj}

    return json.dumps(cyjs_obj)