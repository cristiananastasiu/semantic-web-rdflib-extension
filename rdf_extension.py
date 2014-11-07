"""

This example shows how a custom evaluation function can be added to
handle certain SPARQL Algebra elements

A custom function is added that adds ``rdfs:subClassOf`` "inference" when
asking for ``rdf:type`` triples.

Here the custom eval function is added manually, normally you would use
setuptools and entry_points to do it:
i.e. in your setup.py::

    entry_points = {
        'rdf.plugins.sparqleval': [
            'myfunc =     mypackage:MyFunction',
            ],
    }

"""

import rdflib

from rdflib.plugins.sparql.evaluate import evalBGP
from rdflib.namespace import FOAF
from SPARQLWrapper import SPARQLWrapper, JSON

inferredSubClass = \
    rdflib.RDFS.subClassOf * '*'  # any number of rdfs.subClassOf


def customEval(ctx, part):
    """
    Rewrite triple patterns to get super-classes
    """

    if part.name == 'BGP':
        
        #print(ctx)
        # rewrite triples
        triples = []
        for t in part.triples:
            print(t[0], t[1],t[2])
            if t[1] == rdflib.RDF.type:
                bnode = rdflib.BNode()
                #print(t[0], t[1], bnode)
                triples.append((t[0], t[1], bnode))
                triples.append((bnode, inferredSubClass, t[2]))
            else:
                triples.append(t)

        # delegate to normal evalBGP
        return evalBGP(ctx, triples)

    raise NotImplementedError()

if __name__=='__main__':

    # add function directly, normally we would use setuptools and entry_points
    rdflib.plugins.sparql.CUSTOM_EVALS['exampleEval'] = customEval
    #rdflib.plugin.register('sparql', rdflib.query.Result, 'rdfextras.sparql.query', 'SPARQLQueryResult')
    #rdflib.plugin.register('sparql', rdflib.query.Processor, 'rdfextras.sparql.processor', 'Processor')


    gs = rdflib.Graph()
    gs.open("http://localhost:3030/ds/query")

    g = rdflib.Graph()
    #g.load("/Users/anastasi/Dokumentation/MasterUZH/Courses/WS14/Semantic Web Engineering/exercises/foaf.rdf")

    # Add the subClassStmt so that we can query for it!
    g.add((FOAF.Person,
          rdflib.RDFS.subClassOf,
          FOAF.Agent))

    # Find all FOAF Agents
    #print FOAF


    ret =  gs.query('PREFIX foaf: <http://xmlns.com/foaf/0.1/> SELECT * WHERE {?s a foaf:Person . ?s foaf:name ?mbox . }')
    for x in ret:
        print x
    

 
    sparql = SPARQLWrapper("http://localhost:3030/ds/query")
    sparql.setQuery('PREFIX foaf: <http://xmlns.com/foaf/0.1/> SELECT * WHERE {?s a foaf:Person . ?s foaf:name ?mbox . }')
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
     
    for result in results["results"]['bindings']:
        print(result['mbox']['value'])    
        
    
    '''
    for x in g.query(
            'PREFIX foaf: <http://xmlns.com/foaf/0.1/>' +
            'SELECT ?s ?mbox' +
            'WHERE' +
            '{?s a foaf:Person .' +
            '?s foaf:mbox ?name .' +
            '}'):
        print x
    '''