# # #  PLOT TREES KEEP TBL
import os 
import json
import matplotlib.pyplot as plt
from Bio import Phylo

os. chdir("/home/dora/work/thesis/mammals/")
with open("d_mammals_geneNames.txt", "r") as f:
    d_gname_pbd = json.load(f)
with open("list_A_prot_mammals.txt", 'r') as f:
     l_A=json.load(f)
with open("list_B_prot_mammals.txt", 'r') as f:
     l_B=json.load(f)

# because the files in ../fasta/ are named by geneName
l_A_gname=[]
for item in l_A:
    for g in d_gname_pbd:
        if d_gname_pbd[g][0] == item:
            l_A_gname.append(g)
l_B_gname=[]
for item in l_B:
    for g in d_gname_pbd:
        if d_gname_pbd[g][0] == item:
            l_B_gname.append(g)

l_AB=l_A_gname+l_B_gname



os. chdir("/home/dora/work/thesis/mammals/fastas/")

dict_Tbranch_length={}
l_T_b_length=[]
for prot in l_AB:

    if os.path.exists("/home/dora/work/thesis/mammals/fastas/"+prot+".aln.phy.raxml.bestTree")==False:
        pass
    else:
        tree = Phylo.read(prot+".aln.phy.raxml.bestTree", "newick")
        tree.rooted = True
        #to draw to tree
        #Phylo.draw(tree, do_show=False)
        c=tree.total_branch_length()
        cr=round(c, 4)
        print(prot,"total branch length:"+ str(cr))
        dict_Tbranch_length[prot]=c
        l_T_b_length.append(c)

#to save the Total branch lengths in a txt file
os. chdir("/home/dora/work/thesis/mammals/")
with open("d_mammals_Tbranch_lengths.txt", 'w') as f:
     f.write(json.dumps(dict_Tbranch_length))
    
    
## make list with tbl A and B

l_tblA=[]
l_tblB=[]
for i in dict_Tbranch_length:
    if i in l_A_gname:
        l_tblA.append(dict_Tbranch_length[i])
    elif i in l_B_gname:
        l_tblB.append(dict_Tbranch_length[i])

# # ttest
import numpy as np
from scipy import stats
import statistics
ar_A=np.array(l_tblA)
ar_B=np.array(l_tblB)

meanA=statistics.mean(ar_A)
meanB=statistics.mean(ar_B)
stdA=statistics.stdev(ar_A)
stdB=statistics.stdev(ar_B)

#equal_var=False
tresult=stats.ttest_ind(ar_A,ar_B,equal_var=False)
print(tresult)

####gia box plot
import matplotlib.pyplot as plt

# Creating plot
plt.boxplot([ar_A,ar_B])
# plt.title("Boxplot " +set_prot1+" vs "+ set_prot2)
plt.title("Boxplot Alpha vs Beta Mammals pdb structures")
plt.xticks([1, 2], ["A","B"])
plt.ylabel("Total branch length")
plt.suptitle("MeanA="+str(round(meanA,3)) + ", MeanB="+str(round(meanB,3)) +" \n pval="+str(tresult[1]),x=0.50,y=0.86)
# show plot
#plt.ylim((0,10))
#to save plot
os. chdir("/home/dora/work/thesis/plots_orthoDB/")
plt.savefig("mammals_pbd.pdf")

plt.show()


