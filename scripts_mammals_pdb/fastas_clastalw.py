
##### CLUSTALW
import json
import os
import os.path
from os import path
from Bio.Align.Applications import ClustalwCommandline

os. chdir("/home/dora/work/thesis/mammals/")
with open("d_orthodb_gname_mammals_fastas.txt", "r") as f:
    d_gname_org_fastas = json.load(f)

# check
# d_gname_org_fastas1={}
# d_gname_org_fastas1["AURKA"]=d_gname_org_fastas["AURKA"]

os. chdir("/home/dora/work/thesis/mammals/fastas/")
n=0
for prot in d_gname_org_fastas:
    try:

        ofile = open(prot+".fasta", "w")

        for org in d_gname_org_fastas[prot]:
            org1=org.replace(" ","_")
            ofile.write(">" + org1 + "\n" + d_gname_org_fastas[prot][org] + "\n")

        #do not forget to close it

        ofile.close()
        try:
            cline = ClustalwCommandline("clustalw", infile=prot+".fasta")
            print(cline,n)
            stdout, stderr = cline()
        except:
            print(prot, n, "problem with clustalW running")
    except:
        print(prot,n,"could not open fileprobably due to name")

    n+=1