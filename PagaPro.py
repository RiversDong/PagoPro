import os
import sys
from Bio import SeqIO
from matplotlib import cm
import matplotlib.pyplot as plt
import pandas as pd

def get_pre_filter(infa, prefilter, outf):
    records=SeqIO.parse(infa, "fasta")
    id2seq={}
    for i in records:
        iid=str(i.id); iseq=str(i.seq)
        id2seq[iid]=iseq
    f=open(prefilter).read().split("\n")[0:-11]
    outfile = os.path.join(outf, "piwi.faa")
    out = open(outfile, "w")
    piwi_list=[]
    for i in f:
        if "#" not in i:
            if ""!=i and "Search has CONVERGED!"!=i:
                info = i.split("\t")
                piwi0_id = i.split("\t")[1]
                if piwi0_id not in piwi_list:
                    piwi_list.append(piwi0_id)
    for i in piwi_list:
        iseq = id2seq[i]
        out.write(">"+i+"\n")
        out.write(iseq+"\n")
    out.close()

argvs = sys.argv
for i in range(0, len(argvs)):
    if "-i" in argvs[i]:
        infa = argvs[i+1]
    if "-o" in argvs[i]:
        outf = argvs[i+1]

infa_basename = os.path.basename(infa)
if not os.path.exists(outf):
    os.mkdir(outf)
delta_blast = os.path.join(outf, infa_basename+".prefilter")
db = os.path.join(outf, "db")

if not os.path.exists(db):
    os.mkdir(db)
    dbname = os.path.join(db, infa_basename)
    cmd = "makeblastdb -in {0} -dbtype prot -out {1}".format(infa, dbname) 
    os.system(cmd)
else:
    dbname = os.path.join(db, infa_basename)
    cmd = "makeblastdb -in {0} -dbtype prot -out {1}".format(infa, dbname) 
    os.system(cmd)

query_piwi = os.path.join(os.path.dirname(__file__),"db")
query_piwi = os.path.join(query_piwi,"piwi.fa")
rpsdb = os.path.join(os.path.dirname(__file__), "db")
rpsdb = os.path.join(rpsdb, "cdd_delta")

# the pre-filtering step
cmd = "deltablast -outfmt '7 qseqid sseqid qstart qend sstart send evalue length pident mismatch gaps' -query {0} -db {1} -out {2}  -num_alignments 1000 -evalue 10e-5 -num_iterations 5 -rpsdb {3}".format(query_piwi, dbname, delta_blast, rpsdb)
os.system(cmd)

# extract the protein sequences from the pre-alignment
get_pre_filter(infa, delta_blast, outf)

# InterProScan 进一步筛选其中的Ago和蛋白域的组成
piwi_containing_protein = os.path.join(outf, "piwi.faa")


InterProScan_path = os.path.join(os.path.dirname(__file__), "bin")
InterProScan = os.path.join(InterProScan_path, "interproscan-5.60-92.0")
InterProScan = os.path.join(InterProScan, "interproscan.sh")
interproscan_result = os.path.join(outf, infa_basename)
cmd = "{0} -i {1} -f tsv -dp -b {2}".format(InterProScan, piwi_containing_protein, interproscan_result)
os.system(cmd)

# draw the domain architecture
interproscan_res = interproscan_result+".tsv"
data = pd.read_csv(interproscan_res, sep="\t", header=None, names=["accession", "MD5", "length", "Analysis", "Signature", "description", "Start", "Stop", "Score", "Status", "Date", "InterProID", "InterPro annotations"])
domain_data = data[data["InterPro annotations"].str.contains("domain")]
start = domain_data["Start"]; end = domain_data["Stop"]; dnames=domain_data["InterPro annotations"]
domains=[]; domain_names=[]

# 域和域的名称
seq_len = domain_data["length"].values[0]
for i,j,k in zip(start, end, dnames):
    domains.append((i,j)); domain_names.append(k)

# 计算蛋白质域数量
num_domains = len(domains)
# 选择 colormap
cmap = cm.Set1

# 生成颜色列表，颜色数量与蛋白质域数量相同
colors = [cmap(i) for i in range(num_domains)]

# 创建图像
fig, ax = plt.subplots(figsize=(10, 3))

# 绘制蛋白质序列和绘制每个蛋白质域
ax.hlines(1, xmin=0, xmax=seq_len, linewidth=2)

for i, (start, end) in enumerate(domains):
    color = colors[i]
    domain_name = domain_names[i]
    ax.hlines(2 + i, xmin=start, xmax=end, linewidth=10, color=color)
    ax.vlines(start, 1, 2+i+0.1, linestyle="dashed", color=color, linewidth=1)
    ax.vlines(end, 1, 2+i+0.1, linestyle="dashed", color=color,linewidth=1)
    ax.text(start, 2+i+0.4, domain_name, fontsize=10, color=color) # 标记域的名称

ax.axis('off')
domain_figure = os.path.join(outf, "domain.pdf")
plt.tight_layout(); plt.savefig(domain_figure)