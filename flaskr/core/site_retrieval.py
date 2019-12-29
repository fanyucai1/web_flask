import os
import sys
import configparser
import re
import subprocess
import uuid
class Myconf(configparser.ConfigParser):
    def __init__(self, defaults=None):
        configparser.ConfigParser.__init__(self, defaults=defaults)
    def optionxform(self, optionstr):
        return optionstr

def run(chr,pos,configfile="/home/fanyucai/config/config.ini"):
    config = Myconf()
    config.read(configfile)
    unique_filename = str(uuid.uuid4())
    gtf=config.get('database','hg19_gtf')
    bedtools=config.get('software','bedtools2.28.0')
    hg19=config.get('database','hg19_ref')
    gencode_gtf=config.get('database','gencode_gtf')
    ##################################
    result_gene,result_trans,result_detail,result_chain=[],[],[],[]
    infile=open(gtf,"r")
    ##################################
    geneID,transcriptID=[],[]
    for line in infile:
        line=line.strip()
        if not line.startswith("#"):
            array=line.split("\t")
            p = re.compile(r'gene_name \"(\S+)\"')
            gene_name = p.findall(line)[0]
            p = re.compile(r'transcript_id \"(\S+)\"')
            transcript = p.findall(line)[0]
            if chr==array[0] and array[2] == "transcript" and int(pos) >= int(array[3]) and int(pos) <= int(array[4]):
                geneID.append(gene_name)
                transcriptID.append(transcript)
    infile.close()
    if len(geneID)==0:
        infile=open(gencode_gtf,"r")
        for line in infile:
            line = line.strip()
            if not line.startswith("#"):
                array = line.split("\t")
                if chr == array[0] and array[2] == "gene" and int(pos) >= int(array[3]) and int(pos) <= int(array[4]):
                    result_gene.append(array[2])
        infile.close()
    ###################################
    infile = open(gtf, "r")
    for line in infile:
        line=line.strip()
        if not line.startswith("#"):
            array=line.split("\t")
            if chr == array[0] and array[2] == "exon":
                p = re.compile(r'gene_name \"(\S+)\"')
                gene_name = p.findall(line)[0]
                p = re.compile(r'transcript_id \"(\S+)\"')
                transcript = p.findall(line)[0]
                p = re.compile(r'exon_number \"(\S+)\";')
                exon_number = p.findall(line)[0]
                if transcript in transcriptID:
                    if int(pos) >= int(array[3]) and int(pos) <= int(array[4]):
                        result_gene.append(gene_name)
                        result_trans.append(transcript)
                        result_detail.append("exon_number:%s"%(exon_number))
                        result_chain.append(array[6])
    infile.close()
    ##############################
    tmp = open("%s.bed"%unique_filename, "w")
    right=int(pos)+20
    left=int(pos)-20-1#bed的文件是左闭右开
    tmp.write("%s\t%s\t%s\n"%(chr,left,right))
    tmp.close()
    cmd='%s getfasta -fi %s -bed %s.bed -fo %s.fasta && rm %s.bed'%(bedtools,hg19,unique_filename,unique_filename,unique_filename)
    subprocess.check_call(cmd,shell=True)
    infile=open("%s.fasta"%unique_filename,"r")
    outstring=""
    for line in infile:
        if not line.startswith(">"):
            print(line)
            outstring=line[0:20].lower()+line[20:21].upper()+line[21:].lower()
    infile.close()
    subprocess.check_call('rm %s.fasta'%(unique_filename),shell=True)
    return chr,pos,result_gene,result_trans,result_detail,result_chain,outstring

if __name__=="__main__":
    chr=sys.argv[0]
    pos=sys.argv[1]
    run(chr,pos)