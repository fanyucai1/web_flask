import os
import subprocess
import re
import sys
import uuid
annovar = "/software/docker_tumor_base/Resource/Annovar/"
Canonical_transcript_file = "/data/Database/knownCanonical/clinvar_canonical_trans.txt"
out_name = ['Chr', 'Start', 'End', 'Ref', 'Alt', 'Func.refGene', 'Gene.refGene', 'GeneDetail.refGene',
            'ExonicFunc.refGene', 'AAChange.refGene', 'cytoBand',
            'avsnp150', 'snp138', 'ExAC_ALL', 'esp6500siv2_all', '1000g2015aug_all', 'genome_AF', 'exome_AF',
            'cosmic88_coding', 'CLNALLELEID', 'CLNDN', 'CLNDISDB', 'CLNREVSTAT', 'CLNSIG', 'InterVar_automated',
            'Canonical_transcript', 'SIFT_pred', 'Polyphen2_HDIV_pred', 'Polyphen2_HVAR_pred',
            'MutationTaster_pred', 'MutationAssessor_pred', 'FATHMM_pred',
            'CADD_phred']

def run(chr,pos,ref,alt):
    out_put = []
    unique_filename = str(uuid.uuid4())
    tmp=open(unique_filename,"w")
    tmp.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n")
    tmp.write("%s\t%s\t.\t%s\t%s\t.\t.\t.\n"%(chr,pos,ref,alt))
    tmp.close()
    ###################################Canonical transcript info
    transcript = {}
    infile = open(Canonical_transcript_file, "r")
    for line in infile:
        line = line.strip()
        array = line.split("\t")
        transcript[array[0]] = []
        for i in range(1, len(array)):
            tmp = array[i].split(".")
            transcript[array[0]].append(tmp[0])
    infile.close()
    #####################################run annovar
    par = " -protocol refGene,cytoBand,snp138,avsnp150,exac03,esp6500siv2_all,1000g2015aug_all,gnomad211_exome,gnomad211_genome,cosmic88_coding,clinvar_20190305,ljb26_all,intervar_20180118"
    par += " -operation g,r,f,f,f,f,f,f,f,f,f,f,f "
    par += " -nastring . -polish "
    subprocess.check_call("perl %s/table_annovar.pl %s %s/humandb -buildver hg19 -out %s.annovar -remove %s -vcfinput " % (
    annovar, unique_filename,annovar, unique_filename,par), shell=True)
    invcf = open("%s.annovar.hg19_multianno.txt"%(unique_filename), "r")
    dict={}
    for line in invcf:
        line = line.strip()
        array = line.split("\t")
        if line.startswith("Chr"):
            for i in range(len(array)):
                if array[i] in out_name:
                    dict[array[i]]=i
        else:
            final_nm = ""
            tmp = array[dict['AAChange.refGene']].split(",")
            if not array[6] in transcript:
                print(array[6])
                final_nm = tmp[0]
            else:
                if len(tmp) == 1:
                    final_nm = tmp[0]
                else:
                    if final_nm == "":
                        for i in transcript[array[6]]:
                            if final_nm == "":
                                for k in tmp:
                                    if final_nm == "" and re.search(i, k):
                                        final_nm = k
                                        continue
            for i in out_name:
                if i=="Canonical_transcript":
                    out_put.append(final_nm)
                else:
                    out_put.append(array[dict[i]])
    invcf.close()
    subprocess.check_call('rm -rf %s*'%(unique_filename),shell=True)
    return (out_name,out_put)

if __name__ == "__main__":
    if len(sys.argv)==5:
        chr=sys.argv[1]
        pos=sys.argv[2]
        ref=sys.argv[3]
        alt=sys.argv[4]
        run(chr, pos, ref, alt)