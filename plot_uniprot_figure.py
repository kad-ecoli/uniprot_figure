#!/usr/bin/env python
docstring=''' plot uniprot vs pdb and trembl vs swissprot '''

import matplotlib
matplotlib.use("agg")
from matplotlib import pylab as plt
import numpy as np

#### parse uniprot data ####
uniprot_release=[]
uniprot_list=[]
trembl_list=[]
swissprot_list=[]
fp=open("uniprot.stat",'rU')
lines=fp.read().splitlines()
fp.close()
for line in lines[1:]:
    release,swissprot,trembl=line.split()
    y,m=release.split('_')
    uniprot_release.append(float(y)+float(m)/12)
    trembl_list.append(int(trembl))
    swissprot_list.append(int(swissprot))
    uniprot_list.append(int(trembl)+int(swissprot))

#### years where both databases have data is preserved ####
min_year=int(min(uniprot_release))

uniprot_list=[e for i,e in enumerate(uniprot_list) if uniprot_release[i]>=min_year]
swissprot_list=[e for i,e in enumerate(swissprot_list) if uniprot_release[i]>=min_year]
trembl_list=[e for i,e in enumerate(trembl_list) if uniprot_release[i]>=min_year]
uniprot_release=[e for e in uniprot_release if e>=min_year]


#### uniprot vs pdb ####
plt.figure(1,figsize=(6,4))
plt.semilogy(uniprot_release,uniprot_list,'d-',clip_on=False,color='black',
    label='UniProt (%d entries)'%uniprot_list[-1])
plt.semilogy(uniprot_release,swissprot_list,'^-',clip_on=False,color='black',
    label='SwissProt (%d entries)'%swissprot_list[-1])
plt.axis([min_year,max(uniprot_release),
    min(swissprot_list)*0.9,max(uniprot_list)*1.1])
plt.xlabel("Year")
plt.ylabel("Database entry number (log scale)")

xticks=sorted(set(map(int,uniprot_release)))
plt.xticks(xticks,map(str,xticks))
plt.legend(loc='best',fontsize=10)
plt.tight_layout()

for outfmt in ["png","svg","eps"]:
    plt.savefig("uniprot.%s"%outfmt,dpi=350)
