import os
import json
import pandas as pd
import requests

os. chdir("/home/dora/work/thesis/mammals_computed_structures/")
with open("d_orthodb_gname_fastas.txt", "r") as f:
    d_p_fasta = json.load(f)

l=list(d_p_fasta.keys())

# # # get pdbfiles
os. chdir("/home/dora/work/thesis/mammals_computed_structures/")
with open("d_computed_structures_gName.txt", "r") as f:
    d_gname_pbd = json.load(f)

pdb_list=[]
for gname in l:
    if gname in d_gname_pbd:
        pdb_list.append(d_gname_pbd[gname][0])



# pdb_list=["AF_AFQ6GHQ6F1"]
###get pdbfiles form alphafold and a text in a dictionary
d_prot_pdb={}
n=0
l_prot_no_pdb=[]
for p in pdb_list:
    try:
        url="https://alphafold.ebi.ac.uk/files/AF-"+ p[5:-2] +"-F1-model_v4.pdb"
        #print(url)
        response1 = requests.get(url)
        pdbtext=response1.text
        d_prot_pdb[p]=pdbtext
        print(p,n,"got pdb file")
    except:
        print(p,n, "di not exist in alphafold")
        l_prot_no_pdb.append(p)
    n+=1

#print(d_prot_pdb)

os. chdir("/home/dora/work/thesis/mammals_computed_structures/")
with open("d_prot_pdbfiles.txt", 'w') as f:
     f.write(json.dumps(d_prot_pdb))

#print(pdbtext)
##c save in a pdb files and remove the characters _HUMAN
os. chdir("/home/dora/work/thesis/mammals_computed_structures/pdbfiles/")
n=0
l_no_alphafold=[]
for p in d_prot_pdb:
    if d_prot_pdb[p][0:6]=="HEADER":
        n+=1
        print(n)
        strpdb=d_prot_pdb[p]
        pos=strpdb.index("_HUMAN")
        toremove=strpdb[pos:pos+6]
        strfinal=strpdb.replace(toremove,"")

        #save files in ...pdb
        ofile = open(p+".pdb", "w")

        ofile.write(strfinal)
        #do not forget to close it
        ofile.close()
    else:
        l_no_alphafold.append(p)
print("no structure",len(l_no_alphafold))

