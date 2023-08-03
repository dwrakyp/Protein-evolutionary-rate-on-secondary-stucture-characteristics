import os
import requests
import json


os. chdir("/home/dora/work/thesis/mammals/")
with open("d_mammals_geneNames.txt", "r") as f:
    d_gname_slen = json.load(f)

listp=list(d_gname_slen.keys())

#listp=["asnA","sucC"]
n=0
d_prot_pubid={}
for p in listp:
    try:
        url1="https://data.orthodb.org/current/search?query="+p
        response1 = requests.get(url1)
        apidata1=response1.json()
        if apidata1["data"]=="null":
            print(p, n, "protein query was not found in orthodb")
        else:
            for i in range(0,200):
                if apidata1["bigdata"][i]["level_name"] == "Mammalia":
                    pubid=apidata1["bigdata"][i]["public_id"]
                    d_prot_pubid[p]=pubid
                    print(p, n, "pubid found")
                    break
    except:
        print(p, n, "could not be found in orthodb")
    n+=1


######## GET THE FASTA FILES FOR ALL THE SPECIES(ORG) I WANT
#d_prot_pubid={"AURKA":"5995at40674"}
d_org_fasta={}
n=0
for p in d_prot_pubid:
    id=d_prot_pubid[p]
    try:
        ######## EVERY TIME DEPENDING ON ORGANISMS I WANT I HAVE TO CHANGE THE SPECIES IN THE URL
        url2="https://data.orthodb.org/current/fasta?id="+ id +"&species="
        response2=requests.get(url2)
        data = response2.text
        data1=data.splitlines()
        ### make a dictionary for each protein and the fasta for all the organisms 
        ### many organism have more than 1 fasta also there are more organisms than
        ### the 16 i have chosen
        nn=100
        d_fastas_for1org={}
        for i in range(len(data1)):
            if data1[i] == "":
                pass
            elif data1[i][0]==">":
                linesplit=data1[i].split('"')
                org=linesplit[17]+str(nn)
                fasta=data1[i+1]

                d_fastas_for1org[org]=fasta
                nn+=1
        d_org_fasta[p]=d_fastas_for1org
        print(p,n,"fisrt dict url fine")
    except:
        print(p,n,"could not access url")
    n+=1

n=0
for i in d_org_fasta:
    if len(d_org_fasta[i])>1:
        n+=1
print(n)


####### SPECIFY THE LIST OF ORGANISMS I WANT AND KEEP FOR EACH PROTEIN FASTA, FOR THE FOLLOWING ORGANISMS I KEEP THE FASTA
####### THAT ITS LENGTH IS COLSER TO THE GIVEN FASTA PROTEIN FROM THE DATASET

l_org=["Homo sapiens","Canis lupus familiaris","Mus musculus","Bos taurus","Bison bison bison","Delphinapterus leucas","Equus caballus","Felis catus","Loxodonta africana","Ursus americanus","Pan troglodytes","Panthera leo","Pan paniscus","Rattus norvegicus","Sus scrofa"]#,"

d_gname_prot={}
l_prot=[]
for i in d_gname_slen:
    d_gname_prot[i]=d_gname_slen[i][0]
    l_prot.append(d_gname_slen[i][0])
os. chdir("/home/dora/work/thesis/mammals/")
with open("d_mammals_prot_info_f.txt", "r") as f:
    d_prot_info = json.load(f)

### make a dict with protein and for each prot an other dict with the insects fasta
### and the fasta with the closest length to the one i have from pdb
n=0
d_prot_fasta_final={}
for prot in d_org_fasta:
    n+=1
    print(prot,n)
    pdbid=d_gname_prot[prot]
    seqlen=len(d_prot_info[pdbid][3]) 
    d_org_fasta_final={}
    for org in l_org:
        q=900
        for item in d_org_fasta[prot]:
            orthodb_org=item[:-3]
            if orthodb_org==org: ##### PREPEI NA TO FTIAKSO DEN KANEI SOSTO DIALEGMA ORGANISMON
                ff=d_org_fasta[prot][item]
                num=abs(len(ff)-seqlen)
                if num<q:
                    q=num
                    fasta=ff
        
                d_org_fasta_final[org]=ff
    d_prot_fasta_final[prot]=d_org_fasta_final
    print(prot,n, "dict rearanged with according to insects i chose")


##gia na tsekarv an oles oi proteines exoun fasta kai gia ta 9 insects
prot_to_pop=[]
l_len=[]
for item in d_prot_fasta_final:
    if len(d_prot_fasta_final[item])!=15: ### changes according to insects number
        print(item,len(d_prot_fasta_final[item]))
        prot_to_pop.append(item)
#gia na diksv apo to dict aytew poy exoun ligoterew apo 9
for protein in prot_to_pop:
    d_prot_fasta_final.pop(protein)

print("The number of genenames that have seq for the 15 mammals is ", len(d_prot_fasta_final) )
os. chdir("/home/dora/work/thesis/mammals/")
with open("d_orthodb_gname_mammals_fastas.txt", 'w') as f:
     f.write(json.dumps(d_prot_fasta_final))


