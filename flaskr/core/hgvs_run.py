import hgvs.parser
import hgvs.dataproviders.uta
import hgvs.assemblymapper
import hgvs.normalizer
import sys
def run(hgvs_c):
    #hgvs_c = 'NM_004448.3:c.2310_2311insGCATACGTGATG'
    hp = hgvs.parser.Parser()
    hdp = hgvs.dataproviders.uta.connect()
    hn = hgvs.normalizer.Normalizer(hdp)
    var_c=hn.normalize(hp.parse_hgvs_variant(hgvs_c))
    #################################################可以从基因翻译到蛋白
    am = hgvs.assemblymapper.AssemblyMapper(hdp,assembly_name='GRCh37', alt_aln_method='splign',replace_reference=True)
    var_p = am.c_to_p(var_c)
    var_p.posedit.uncertain = False
    return (str(var_c),str(var_p))

if __name__=="__main__":
    if (len(sys.argv)!=2):
        print("e.g:python3 %s NM_004448.3:c.2310_2311insGCATACGTGATG"%(sys.argv[0]))
        print("\nEmail:fanyucai1@126.com")
    else:
        run(sys.argv[1])