 ##
 ## \file    extract_elements.py
 ## \brief   extract the list of a specific elements of a given model
 ## \author  Tung Nguyen (tung.nguyen@ebi.ac.uk)

import sys
from libsbml import *

def get_qualifier_type(qualifier_type):
    return {
        MODEL_QUALIFIER: 'bqmodel',
        BIOLOGICAL_QUALIFIER: 'bqbiol',
        UNKNOWN_QUALIFIER: 'unknown'
    } [qualifier_type]

def convert_bqbiol_to_string(bqbiol):
    return {
        BQB_IS              : 'is',
        BQB_HAS_PART        : 'hasPart',
        BQB_IS_PART_OF      : 'isPartOf',
        BQB_IS_VERSION_OF   : 'isVersionOf',
        BQB_HAS_VERSION     : 'hasVersion',
        BQB_IS_HOMOLOG_TO   : 'isHomologTo',
        BQB_IS_DESCRIBED_BY : 'isDescribedBy',
        BQB_IS_ENCODED_BY   : 'isEncodedBy',
        BQB_ENCODES         : 'encodes',
        BQB_OCCURS_IN       : 'occursIn',
        BQB_HAS_PROPERTY    : 'hasProperty',
        BQB_IS_PROPERTY_OF  : 'isPropertyOf',
        BQB_HAS_TAXON       : 'hasTaxon'
    } [bqbiol]

def convert_bqmodel_to_string(bqmodel):
    return {
        BQM_IS              : 'is',
        BQM_IS_DESCRIBED_BY : 'isDescribedBy',
        BQM_IS_DERIVED_FROM : 'isDerivedFrom',
        BQM_IS_INSTANCE_OF  : 'isInstanceOf',
        BQM_HAS_INSTANCE    : 'hasInstance'
    } [bqmodel]

def main(args):
    """usage: extract_elements.py <sbml_file>
    Extract species, reactions, compartments, etc. along their annotations.
        <sbml_file>:       is your SBML file
    """
    if len(args) != 2:
        print(main.__doc__)
        sys.exit(2)

    d = readSBML(args[1])
    errors = d.getNumErrors()

    if errors > 0:
        print("Read Error(s):" + Environment.NewLine)
        d.printErrors()
        print("Correct the above and re-run." + Environment.NewLine)
    else:
        model = d.getModel()
        if model is None:
            print("No model present.")
            return 1
        '''
        Replace model.getNumSpecies() below by your interested types of elements, for instance, model.getReactions()
        '''
        nb_elements = model.getNumSpecies()
        for i in range(0, nb_elements):
            '''
            Replace model.getSpecies(i) below by the according method to the element type declared just above.
            For instance, if you change to model.getReactions(), you must use model.getReaction(i)
            '''
            s = model.getSpecies(i)
            annotation = s.getCVTerms()
            metaId = s.getMetaId()
            element_name = s.getName()
            element_name = "," + element_name if element_name else ""
            if annotation:
                for anno in annotation:
                    qualifierType = anno.getQualifierType()
                    if qualifierType == BIOLOGICAL_QUALIFIER:
                        anno_str = get_qualifier_type(qualifierType) + ":" + \
                                   convert_bqbiol_to_string(anno.getBiologicalQualifierType())
                    else:
                        anno_str = get_qualifier_type(qualifierType) + ":" + \
                                   convert_bqmodel_to_string(anno.getModelQualifierType())

                    resources = anno.getResources()
                    for j in range(0, resources.getNumAttributes()):
                        uri = resources.getValue(j)
                        if uri.startswith('urn:miriam'):
                            the_rest = uri[11:] # 11 = len('urn:miriam') + 1
                            the_first_colon = the_rest.find(":")
                            external_resource = the_rest[:the_first_colon]
                            accession_id = the_rest[the_first_colon + 1: ]
                        elif uri.startswith('http://'):
                            # starts with http://
                            tokenised_uri = uri.split("/")
                            external_resource = tokenised_uri[len(tokenised_uri)-2]
                            accession_id = tokenised_uri[len(tokenised_uri)-1]
                        else:
                            external_resource = "unknown"
                            accession_id = "unknown"

                        out_str = metaId + "," + external_resource + "," + anno_str + "," + accession_id + element_name
                        print(out_str)
            else:
                out_str = metaId + ",,,," + element_name
                print(out_str)

    return errors

if __name__ == '__main__':
    main(sys.argv)
