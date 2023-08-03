##### CLUSTALW
import json
import os
from Bio.Align.Applications import ClustalwCommandline

os. chdir("/home/dora/work/thesis/mammals_computed_structures/")
with open("d_orthodb_gname_fastas.txt", "r") as f:
    d_gname_org_fastas = json.load(f)


# # # TO CHECK
# p=d_gname_org_fastas["PRTN3"]
# d_gname_org_fastas1={}
# d_gname_org_fastas1["PRTN3"]=p

os. chdir("/home/dora/work/thesis/mammals_computed_structures/fastas/")
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
        print(prot,n, "problem with protein name could not open file")
    n+=1


