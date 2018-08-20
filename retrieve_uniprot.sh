#!/bin/bash
FTP_LINK=ftp://ftp.uniprot.org/pub/databases/uniprot/previous_releases

printf "release\tswissprot\ttrembl\n" > uniprot.stat
for RELEASE in `curl -l $FTP_LINK/|grep -ohP 'release-\d+_\d+'`;do
    echo $RELEASE
    RELNOTE=`curl $FTP_LINK/$RELEASE/relnotes.txt`
    if [ -z "$RELNOTE" ];then
        continue
    fi
    SWISSPROT=`echo $RELNOTE|grep -iohP "Swiss-Prot: [,\d]+ entries"|grep -ohP "[,\d]+"|sed 's/,//g'`
    TREMBL=`echo $RELNOTE|grep -iohP "TrEMBL: [,\d]+ entries"|grep -ohP "[,\d]+"|sed 's/,//g'`
    printf "$RELEASE\t$SWISSPROT\t$TREMBL\n"|sed "s/release-//g" >> uniprot.stat
done
