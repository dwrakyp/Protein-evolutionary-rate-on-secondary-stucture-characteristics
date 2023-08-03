
# # # MANAGE DICTIONARY WITH PROT INFO 
# # # REMOVE THE PROT WITH NO INFO 
import os
import json
os. chdir("/home/dora/work/thesis/mammals/")
with open("d_mammals_prot_info.txt", "r") as f:
    d = json.load(f)

n=0
prot_to_drop=[]
for prot in d:
    print(prot,n)
    n+=1
    for item in d[prot]:
        if item[0:2]=="no":
            prot_to_drop.append(prot)
            break

dict={}
n=0
for item in d:
    print(n)
    n+=1
    if item in prot_to_drop:
        pass
    else:
        dict[item]=d[item]

os. chdir("/home/dora/work/thesis/mammals/")
with open("d_mammals_prot_info_f.txt", 'w') as f:
     f.write(json.dumps(dict))

# # # CHECK THE ORGANISM IN THE DICTIONARY
import os
import json
os. chdir("/home/dora/work/thesis/mammals/")
with open("d_mammals_prot_info_f.txt", "r") as f:
    dict = json.load(f)

import pandas as pd
## create a df and work with that
df=pd.DataFrame.from_dict(dict)
df=df.T
df.columns=["geneName","uniprotID","org","seq"]

#### to keep only the proteins that belong tho the desired organisms
# # # the organisms i want to check
l_org=["Homo sapiens"]
col_org = df["org"].values.tolist()

col_org_f=[]
for item in col_org:
    # Split the item into words
    words = item.split()
    modified_item = ' '.join(words[:2])
    col_org_f.append(modified_item)

row_names=df.index.to_list()
## to drop
n=0
to_drop=[]
for item in col_org_f:
    if item in l_org:
        pass
    else:
        to_drop.append(row_names[n])
    n+=1
#df without the proteins from organisms except the 10 i want  
df_dropped_rows = df.drop(to_drop)
df_dropped_rows.to_csv('df_mammals.csv')

# # # TO CHECK HOW THE GENES ARE REPRESENTED IN THE DATA SET
prot_names=df_dropped_rows.index.to_list()
gene_names=df_dropped_rows["geneName"].values.tolist()

dict_geneNames={}
n=0
for i in prot_names:
    gname=gene_names[n]
    if gname in dict_geneNames:
        dict_geneNames[gname].append(i)
    else:
        dict_geneNames[gname]=[i]
    n+=1

print("the number of the unique geneNames is", len(dict_geneNames))

os. chdir("/home/dora/work/thesis/mammals/")
with open("d_mammals_geneNames.txt", 'w') as f:
     f.write(json.dumps(dict_geneNames))


