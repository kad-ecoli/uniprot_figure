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

#### parse pdb data ####
pdb_release=[]
pdb_list=[]
fp=open("pdb.stat",'rU')
lines=fp.read().splitlines()
fp.close()
for line in lines[1:]:
    release,pdb=line.split()
    pdb_release.append(int(release))
    pdb_list.append(int(float(pdb)))

#### years where both databases have data is preserved ####
min_year=int(max([min(pdb_release),min(uniprot_release)]))

pdb_list=[e for i,e in enumerate(pdb_list) if pdb_release[i]>=min_year]
pdb_release=[e for e in pdb_release if e>=min_year]

uniprot_list=[e for i,e in enumerate(uniprot_list) if uniprot_release[i]>=min_year]
swissprot_list=[e for i,e in enumerate(swissprot_list) if uniprot_release[i]>=min_year]
trembl_list=[e for i,e in enumerate(trembl_list) if uniprot_release[i]>=min_year]
uniprot_release=[e for e in uniprot_release if e>=min_year]


#### uniprot vs pdb ####
plt.figure(1,figsize=(6,4))
plt.semilogy(uniprot_release,uniprot_list,'d-',
    clip_on=False,color='black',label='UniProt (%d entries)'%uniprot_list[-1])
plt.semilogy(uniprot_release,swissprot_list,'^-',
    clip_on=False,color='black',label='SwissProt (%d entries)'%swissprot_list[-1])
plt.semilogy(pdb_release,pdb_list,'o-',
    clip_on=False,color='grey',label='PDB (%d entries)'%pdb_list[-1])
plt.axis([min_year,max([max(pdb_release),max(uniprot_release)]),
    min(pdb_list),max(uniprot_list)*1.1])
plt.xlabel("year")
plt.ylabel("database entry number (log scale)")
plt.xticks(pdb_release,map(str,pdb_release))
plt.legend(loc='best',fontsize=10)
plt.tight_layout()

for outfmt in ["png","svg","eps"]:
    plt.savefig("all3.%s"%outfmt,dpi=350)
