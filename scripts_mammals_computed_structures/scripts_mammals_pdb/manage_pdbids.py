import os
import json
import requests

os. chdir("/home/dora/work/thesis/mammals/")
with open('pdbids.txt', 'r') as file:
    str_ids = file.read()

l_id=str_ids.split(",")

l_ids=list(set(l_id))
#l_ids=["6TBN","5HX8","3IT8"]

# # # TO GET ALL THE PDB ENTITIES FOR EACH PROT
pdb_List=[]
n=0
for i in l_ids:
    url="https://data.rcsb.org/rest/v1/core/assembly/" +i +"/1"
    response = requests.get(url)
    apidata=response.json()

    try:
        num_entity_ids=apidata["pdbx_struct_assembly"]["oligomeric_count"]
        print(n)
        n+=1
        list_num=[]
        if num_entity_ids<50:
            for num in range(num_entity_ids):
                list_num.append(num+1)
                pdb_List.append(i+str(num+1))
    except:
        print(i,"some error in apidata...")

#to save the pdb list with the entities
os. chdir("/home/dora/work/thesis/mammals/")
with open("l_mammals_pdb_entities.txt", 'w') as f:
     f.write(json.dumps(pdb_List))

# # # TO MAKE A DICT WITH INFO (GENENAME,UNIPROTID,ORGANISM,SEQ) FOR EACH PROT
dict_prot_info={}
n=0
for prot in pdb_List:
    p=prot[0:4]
    ent=prot[4:]
    print(prot,n, "entity ID", ent)
    ##reach the url
    try:
        url="https://data.rcsb.org/rest/v1/core/polymer_entity/" +p +"/"+ str(ent)
        response = requests.get(url)
        apidata=response.json()
    except:
        print(prot," url could not been reached")
    ## extract gene name
    try:
        gene_name_pdb=apidata["rcsb_entity_source_organism"][0]["rcsb_gene_name"][0]["value"]
        gene_name_pdb.lower()
        dict_prot_info[prot]=[gene_name_pdb]
    except:
        print(prot, "--> gene name do not exist")
        dict_prot_info[prot]=["no genename in pdb"]
    ## extract uniprotID
    try:
        uniprotID=apidata["rcsb_polymer_entity_align"][0]["reference_database_accession"]
        dict_prot_info[prot].append(uniprotID)
    except:
        print("no info about uniprot ID")
        dict_prot_info[prot].append("no uniprotID in pdb")
    ## extract organism
    try: 
        org=apidata["rcsb_entity_source_organism"][0]["ncbi_scientific_name"]
        dict_prot_info[prot].append(org)
    except:
        print("no info about organism")
        dict_prot_info[prot].append("no org in pdb")
    ## extract sequence
    try: 
        seq=apidata["entity_poly"]["pdbx_seq_one_letter_code"]
        dict_prot_info[prot].append(seq)
    except:
        print("no info about seq")
        dict_prot_info[prot].append("no seq in pdb")
    n+=1


#to save the dict
os. chdir("/home/dora/work/thesis/mammals/")
with open("d_mammals_prot_info.txt", 'w') as f:
     f.write(json.dumps(dict_prot_info))


