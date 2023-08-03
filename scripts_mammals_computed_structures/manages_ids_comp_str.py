import os
import json
import requests

os. chdir("/home/dora/work/thesis/mammals_computed_structures/")
with open('hsapiens_comp_str.txt', 'r') as file:
    str_ids = file.read()

l_id=str_ids.split(",")

l_ids=list(set(l_id))

#l_ids=["AF_AFQ31C13F1","AF_AFQ0VP64F1"]

dict_prot_info={}
n=0
for prot in l_ids:
    print(prot,n)
    ##reach the url
    try:
        url="https://data.rcsb.org/rest/v1/core/polymer_entity/" +prot +"/1"
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
os. chdir("/home/dora/work/thesis/mammals_computed_structures/")
with open("d_computed_structures_protinfo.txt", 'w') as f:
     f.write(json.dumps(dict_prot_info))