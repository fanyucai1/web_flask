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
    gtf=config.get('database','gencode_gtf')
    bedtools=config.get('software','bedtools2.28.0')
    hg19=config.get('database','hg19_ref')
    infile=open(gtf,"r")
    gene_name,transcript,chain,exon=[],[],[],""
    for line in infile:
        line=line.strip()
        if not line.startswith("#"):
            array=line.split("\t")
            if array[2] == "gene" and array[0] == chr and pos >= int(array[3]) and pos <= int(array[4]):
                p = re.compile(r'gene_name \"(\S+)\"')
                gene_name.append(p.findall(line)[0])
            if array[2] == "transcript" and array[0] == chr and pos >= int(array[3]) and pos <= int(array[4]):
                p = re.compile(r'transcript_id \"(\S+)\"')
                transcript.append(p.findall(line)[0])
                chain.append(array[6])
            if array[2]=="exon" and array[0]==chr:
                if pos >int(array[3]) and pos <int(array[4]):
                    p = re.compile(r'exon_number (\d+);')
                    exon_number = p.findall(line)
                    exon=""
                    print("gene name:%s transcript_name:%s exon_number:%s %s" % (gene_name[0], transcript[0], exon_number[0],array[6]))
                elif pos ==int(array[3]) or pos ==int(array[4]):
                    p = re.compile(r'exon_number (\d+);')
                    exon_number = p.findall(line)
                    exon = ""
                    print("gene name:%s transcript_name:%s exon_number:%s %s" % (gene_name[0], transcript[0], exon_number[0], array[6]))
                else:
                    p = re.compile(r'transcript_id \"(\S+)\"')
                    name=p.findall(line)
                    if name and name[0] in transcript:
                        if array[6]=="+":
                            if int(pos) > int(array[4]):
                                p = re.compile(r'exon_number (\d+);')
                                exon_number = p.findall(line)
                                exon=exon_number[0]
                            if int(pos) < int(array[3]) and exon!="":
                                print("gene name:%s transcript_name:%s intron_number:%s %s"%(gene_name[-1],name[0], exon,array[6]))
                                exon=""
                        else:
                            if int(pos) < int(array[3]):
                                p = re.compile(r'exon_number (\d+);')
                                exon_number = p.findall(line)
                                exon=exon_number[0]
                            if int(pos) > int(array[4]) and exon!="":
                                print("gene name:%s transcript_name:%s intron_number:%s %s"%(gene_name[-1],name[0], exon,array[6]))
                                exon=""
    unique_filename = str(uuid.uuid4())
    tmp = open("%s.bed"%unique_filename, "w")
    right=pos+20
    left=pos-20
    tmp.write("%s\t%s\t%s\n"%(chr,left,right))
    tmp.close()
    cmd='%s getfasta -fi %s -bed %s.bed -fo %s.fasta && rm %s.bed'%(bedtools,hg19,unique_filename,unique_filename,unique_filename)
    subprocess.check_call(cmd,shell=True)
    infile=open("%s.fasta"%unique_filename,"r")
    outstring=""
    for line in infile:
        if not line.startswith(">"):
            outstring=line[0:19].lower()+line[20].upper()+line[21:].lower()
    infile.close()
    subprocess.check_call('rm %s.fasta'%(unique_filename),shell=True)
    print(outstring)
if __name__=="__main__":
    run("chr1",29535)