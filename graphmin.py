from optparse import OptionParser
import logging
import sys

from rdflib.Graph import Graph, ConjunctiveGraph, ReadOnlyGraphAggregate
from FuXi.Rete.Network import ReteNetwork
from FuXi.Rete.Util import generateTokenSet
from FuXi.Rete.RuleStore import SetupRuleStore
from FuXi.Horn.HornRules import HornFromN3
from FuXi.SPARQL.BackwardChainingStore import TopDownSPARQLEntailingStore

log = logging.getLogger("graphmin")

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
    opt_parser.add_option("-l", "--logfile",
                          dest="logfile",
                          help="logfile")
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
        logcfg = {
            "format": "%(asctime)s - %(levelname)s - %(message)s",
            "level": logging.DEBUG,
        }
        if self.opts.logfile:
            logcfg.filename = self.opts.logfile
        logging.basicConfig(**logcfg)

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

        facts = Graph()
        facts.parse(infile, format=self.get_informat())
        infile.close()

#        rstore, rgraph = SetupRuleStore()
#        network = ReteNetwork(rstore)
#        rules = HornFromN3(self.opts.rules)
#        for rule in rules:
#            network.buildNetworkFromClause(rule)
#        network.feedFactsToAdd(generateTokenSet(facts))
#
#        facts += network.inferredFacts

        minimised = Graph()
        minimised.namespace_manageer = facts.namespace_manager
        minimised += facts
        
        for s,p,o in facts.triples((None, None, None)):
            minimised.remove((s,p,o))
            rules = HornFromN3(self.opts.rules)
            topDownStore = TopDownSPARQLEntailingStore(
                minimised.store,
                minimised,
                idb=rules,
                decisionProcedure=0,
                derivedPredicates=[p])
            target = Graph(topDownStore)

            q = "ASK WHERE { %s }" % " ".join(x.n3() for x in (s,p,o))
            log.debug("QUERY %s" % q)
            result = target.query(q).askAnswer[0]
            log.debug("RESULT %s" % result)
            if not result:
                minimised.add((s,p,o))
                if self.opts.debug:
                    log.info("KEEP %s." % " ".join(x.n3() for x in (s,p,o)))
            elif self.opts.debug:
                log.info("DROP %s." % " ".join(x.n3() for x in (s,p,o)))

        if self.opts.outfile == "-":
            outfile = sys.stdout
        else:
            outfile = open(self.opts.outfile, "w+")
        minimised.serialize(outfile, format=self.opts.format)
        outfile.close()

def graphmin():
    GraphMinimiser().command()
