
import os
import requests
import json

os. chdir("/home/dora/work/thesis/mammals/")
with open("d_orthodb_gname_mammals_fastas.txt", "r") as f:
    d_p_fasta = json.load(f)

l=list(d_p_fasta.keys())

# # # get pdbfiles
os. chdir("/home/dora/work/thesis/mammals/")
with open("d_mammals_geneNames.txt", "r") as f:
    d_gname_pbd = json.load(f)

pdb_list=[]
for gname in l:
    if gname in d_gname_pbd:
        pdb_list.append(d_gname_pbd[gname][0])

# # # TO DOWNLOAD PDB FILES
from Bio.PDB import PDBList
from urllib.request import urlopen
import requests
import os.path
from os import path
pdbl = PDBList()
b=0
pdb_list_final=[]
os. chdir("/home/dora/work/thesis/mammals/pdbfiles/")
for i in pdb_list:
    ## check how many entity ids has each protein and download pdb for
    ## proteins with 1 entity id
    
    url="https://data.rcsb.org/rest/v1/core/assembly/" +i[0:4] +"/1"
    
    response = requests.get(url)
    apidata=response.json()


    filename=i[0:4]+".pdb"
    if path.exists(filename) == True:
        print(b, "exists")
        pass
    else:
        #downloads the pdb files as .ent and puts then in a dir named "PDB"
        a=pdbl.retrieve_pdb_file(i[0:4],pdir="PDB",file_format="pdb")
        print(b,"downloaded")
        #renames the files so they will be .pdb
        if path.exists(a) == True:
            newname= i[0:4]+".pdb"
            os.rename(a,newname)
            pdb_list_final.append(i)
        else:
            pass
    b+=1
