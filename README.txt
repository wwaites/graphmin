RDF Graph Minimisation Experiment
=================================

  * Source Code: http://github.com/wwaites/graphmin
  * PyPI: http://pypi.python.org/pypi/graphmin
  * Home Page: http://river.styx.org/ww/2010/10/graphmin

Installation
------------

For the inferencing, a special branch of rdflib is 
needed::

    ## don't install this stuff system-wide, use virtualenv
    virtualenv foo
    . ./foo/bin/activate
    ## install the bits that are needed
    pip install pyparsing
    pip install -e svn+http://python-dlp.googlecode.com/svn/trunk/layercake-python#egg=rdflib
    pip install hg+https://fuxi.googlecode.com/hg/#egg=fuxi
    pip install graphmin

Example
-------

Running this example::

    graphmin -i examples/ex1.n3 -f n3 -r examples/rdfs-rules.n3 

Should give this result::

    @prefix eg: <http://example.org/>.
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.

    eg:a a eg:A.

Because *eg:a a rdfs:Resource* is entailed by the RDFS inference rules.

References
----------

    * http://code.google.com/p/fuxi/wiki/TopDownSW