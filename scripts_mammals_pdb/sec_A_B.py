
#### to determine A and B proteins from dssp files
import requests
import os
import json
#pdb_list=["2NU82"]

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

domh="H"
domh2="E"
n0=0
os. chdir("/home/dora/work/thesis/mammals/pdbfiles/")
dict_sec_str_all={}
prot_to_drop=[]


d_per_A_B={}
l_A_prot=[]
l_B_prot=[]
for file in pdb_list:
    print(file,n0)
    n0+=1

    ### make a dictionary with the prot names-entity id ex. 1OOL3 and the protein chain that is represent ex. A,B
    ### in the dictionary i will keep only the first chain that it represent as the chains are the same for one entity id
    try:
        url="https://data.rcsb.org/rest/v1/core/polymer_entity/" +file[0:4] +"/"+ file[-1:]
        response = requests.get(url)
        apidata=response.json()
        chain=apidata["entity_poly"]["pdbx_strand_id"]
        chain=chain[0]
        
        
        #read the dssp file
        os. chdir("/home/dora/work/thesis/mammals/pdbfiles/")
        file2=file
        file= file[0:4] + ".pdb.dssp"

        if os.path.exists("/home/dora/work/thesis/mammals/pdbfiles/")==False:
            pass
        else:
            n=0
            sec_str=""
            with open(file, "r") as f:
                fopen = f.readlines()
            for li in fopen:
                if li[0:3]=="  #":
                    break
                n+=1
            fopen = fopen[n+1:]
            l_pos_aa_dssp=[]
            
            amino=""
            for l in fopen:
                if l[11]==chain:
                    if l[16]==" ":
                        char="-"
                        amino+=l[13]
                    else:
                        char=l[16]
                        amino+=l[13]
                    l_pos_aa_dssp.append(l[7:10])
                    sec_str+=char
            #keep in a string the first 10 AA in dssp
            first10=amino[0:10]

            if sec_str=="":
                prot_to_drop.append(file2)
            else:


                ### vriskw poso domhs H h E 
                d1=0
                d2=0
                for he in sec_str:
                    if he==domh:
                        d1+=1
                    elif he==domh2:
                        d2+=1

                pososto_d1=d1/len(sec_str)
                pososto_d2=d2/len(sec_str)
            
                d_per_A_B[file2]=[pososto_d1,pososto_d2]

                if pososto_d1>pososto_d2:
                    l_A_prot.append(file2)
                else:
                    l_B_prot.append(file2)

    except:
        print("something wrong with entity poly", file2, str(n0))


os. chdir("/home/dora/work/thesis/mammals/")
with open("d_per_A_B_mammals.txt", 'w') as f:
     f.write(json.dumps(d_per_A_B))
with open("list_A_prot_mammals.txt", 'w') as f:
     f.write(json.dumps(l_A_prot))
with open("list_B_prot_mammals.txt", 'w') as f:
     f.write(json.dumps(l_B_prot))

print("A ",len(l_A_prot)," and B ",len(l_B_prot))



