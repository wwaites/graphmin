from optparse import OptionParser
import sys

from rdflib.Graph import Graph
from FuXi.Horn.HornRules import HornFromN3
from FuXi.SPARQL.BackwardChainingStore import TopDownSPARQLEntailingStore

class GraphMinimiser(object):
    opt_parser = OptionParser(usage="""
Minimise a graph...
""")
    opt_parser.add_option("-c", "--config",
                          dest="config",
                          help="Configuration file")
    opt_parser.add_option("-d", "--debug",
                          dest="debug",
                          default=False,
                          action="store_true",
                          help="debug")
    opt_parser.add_option("-i", "--input",
                          dest="infile",
                          default="-",
                          help="Input Graph"),
    opt_parser.add_option("-o", "--output",
                          dest="outfile",
                          default="-",
                          help="Output Graph"),
    opt_parser.add_option("-r", "--rules",
                          dest="rules",
                          default=None,
                          help="N3 Rules")
    opt_parser.add_option("-f", "--format",
                          dest="format",
                          default="pretty-xml",
                          help="Output format (default: xml)")

    config = {}
    def __init__(self):
        self.opts, self.args = self.opt_parser.parse_args()
        if self.opts.config:
            fp = open(self.opts.config)
            cfg = eval(fp.read())
            fp.close()
            self.config.update(cfg)

    def get_informat(self):
        if self.opts.infile == "-":
            return "xml"
        formats = { 
            "n3": "n3",
            "nt": "nt",
            "ttl": "n3"
            }
        _f,ext = self.opts.infile.rsplit(".", 1)
        return formats.get(ext, "xml")

    def command(self):
        if self.opts.infile == "-":
            infile = sys.stdin
        else:
            infile = open(self.opts.infile)
        if self.opts.outfile == "-":
            outfile = sys.stdout
        else:
            outfile = open(self.opts.outfile, "w+")

        facts = Graph()
        facts.parse(infile, format=self.get_informat())
        infile.close()

        rules = HornFromN3(self.opts.rules)
        
        for s,p,o in facts.triples((None, None, None)):
            facts.remove((s,p,o))
            topDownStore = TopDownSPARQLEntailingStore(
                facts.store,
                facts,
                idb=rules,
                derivedPredicates=[p])
            target = Graph(topDownStore)
            q = "ASK WHERE { %s }" % " ".join(x.n3() for x in (s,p,o))
            result = target.query(q)
            if not result.askAnswer.pop():
                facts.add((s,p,o))

        facts.serialize(outfile, format=self.opts.format)
        outfile.close()

def graphmin():
    GraphMinimiser().command()
