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

    ## install the prerequisites
    pip install pyparsing
    pip install -e svn+http://python-dlp.googlecode.com/svn/trunk/layercake-python#egg=rdflib
    pip install hg+https://fuxi.googlecode.com/hg/#egg=fuxi

    ## install this package from git
    git clone git://github.com/wwaites/graphmin.git
    cd graphmin
    python setup.py develop

Example
-------

Running this example::

    graphmin -i examples/ex1.n3 -f n3 -r examples/rdfs-rules.n3 

Should give this result::

    @prefix eg: <http://example.org/>.
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.

    eg:a a eg:A.

Because the statement *eg:a a rdfs:Resource* in ex1.n3 is entailed by
the RDFS inference rules.

References
----------

    * `Minimising RDF Graphs Under Rules and Constraints Revisited`_
    * http://code.google.com/p/fuxi/wiki/TopDownSW

.. _Minimising RDF Graphs Under Rules and Constraints Revisited: http://axel.deri.ie/AMW10/rdfmin-full.pdf
