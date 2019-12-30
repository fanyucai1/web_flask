
import configparser
class Myconf(configparser.ConfigParser):
    def __init__(self, defaults=None):
        configparser.ConfigParser.__init__(self, defaults=defaults)
    def optionxform(self, optionstr):
        return optionstr

def run(chr,pos,ref,alt,configfile="/home/fanyucai/config/config.ini"):
    config = Myconf()
    config.read(configfile)
    hotspot=config.get('database','hotspot')
    infile=open(hotspot,"r")
    string="false"
    for line in infile:
        line=line.strip()
        array=line.split("\t")
        if chr==array[0] and pos==array[1] and ref==array[2] and alt==array[3]:
            string="This var site has been contained in hotspot database."
            return string
    infile.close()
    if string=="false":
        string=("This var site has not been contained in hotspot database.\n"
              "You could write a Email to fanyucai1@126.com\n"
              "As follows:Chr\tPos\tRef\tAlt\n")
        return string