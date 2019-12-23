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
    gtf=config.get('database','hg19_gtf')
    bedtools=config.get('software','bedtools2.28.0')
    hg19=config.get('database','hg19_ref')
    RefSeq=config.get('database','RefSeq_meta')
    infile=open(gtf,"r")
    ##################################
    gene_fina,transcript_fina,exon="","",""
    for line in infile:
        line=line.strip()
        if not line.startswith("#"):
            array=line.split("\t")
            if array[2] == "exon" and array[0] == chr:
                p = re.compile(r'gene_name \"(\S+)\"')
                gene_name=p.findall(line)[0]
                p = re.compile(r'transcript_id \"(\S+)\"')
                transcript=p.findall(line)[0]
                p = re.compile(r'exon_number \"(\S+)\";')
                exon_number = p.findall(line)[0]
                if pos > int(array[3]) and pos < int(array[4]):
                    print("gene name:%s transcript_name:%s exon_number:%s %s" % (gene_name, transcript, exon_number, array[6]))
                if pos == int(array[3]) or pos == int(array[4]):
                    print("gene name:%s transcript_name:%s exon_number:%s %s" % (gene_name, transcript, exon_number, array[6]))
                if int(pos) > int(array[4]):
                    exon = exon_number[0]
                    gene_fina=gene_name
                    transcript_fina=transcript
                if int(pos) < int(array[3]) and exon != "" and gene_fina==gene_name and transcript_fina==gene_name:
                    print("gene name:%s transcript_name:%s intron_number:%s %s" % (gene_name, transcript, exon, array[6]))
                    exon=""
    infile.close()
    ##############################
    unique_filename = str(uuid.uuid4())
    tmp = open("%s.bed"%unique_filename, "w")
    right=pos+20
    left=pos-20-1#bed的文件是左闭右开
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
    print(outstring)


if __name__=="__main__":
    run("chr1",14362)