import configparser
class Myconf(configparser.ConfigParser):
    def __init__(self, defaults=None):
        configparser.ConfigParser.__init__(self, defaults=defaults)
    def optionxform(self, optionstr):
        return optionstr

def run(gene_name,configfile="/home/fanyucai/config/config.ini"):
    config = Myconf()
    config.read(configfile)
    trans1=config.get('database','Canonical_transcript_file')
    trans2=config.get('database','msk_transcript')
    infile=open(trans1,"r")
    clinvar_trans,msk_trans="",""
    for line in infile:
        line=line.strip()
        array=line.split("\t")
        if array[0]==gene_name:
            clinvar_trans=array[1]
            continue
    infile.close()
    infile=infile=open(trans2,"r")
    for line in infile:
        line = line.strip()
        array = line.split("\t")
        if array[0]==gene_name:
            msk_trans=array[1]
            continue
    infile.close()
    return clinvar_trans,msk_trans

