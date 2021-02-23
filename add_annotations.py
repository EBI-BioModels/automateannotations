 ##
 ## \file    appendAnnotation.py
 ## \brief   adds annotations to various entities of a given model
 ## \author  Tung Nguyen (tung.nguyen@ebi.ac.uk)
 
import sys
import os.path
from libsbml import *
from collections import defaultdict
import csv
 
def main (args):
    """usage: appendAnnotation <input-filename> <annotations-filename> <output-filename>
    Adds annotations to species, reactions, compartments etc.
    <input-filename>:       is your SBML file
    <annotations-filename>: is a csv file containing annotations that are added to entities. 
                            Please look at its structures.
    <output-filename>:      is your updated SBML  file
    """
    if len(args) != 4:
        print(main.__doc__)
        sys.exit(2)

    d = readSBML(args[1])
    errors = d.getNumErrors()
  
    if (errors > 0):
        print("Read Error(s):" + Environment.NewLine)
        d.printErrors()
  
        print("Correct the above and re-run." + Environment.NewLine)
    else:
        print("Well structured document!")
        datafile = args[2]
        updated_annotations = defaultdict(list)
        with open(datafile,"rt") as csvfile:
            cr = csv.reader(csvfile)
            next(cr)
            for row in cr:
                updated_annotations[row[0]].append(row)
        m = d.getModel()
        print("There are", len(updated_annotations), "entities about to be annotated")
        for metaid in updated_annotations:
            if metaid is not None:
                print("The entity associated with the metaid", metaid, "is being annotated!")
                for annotation in updated_annotations[metaid]:
                    external_resource = annotation[1]
                    qualifier = annotation[2]
                    accession_id = annotation[3]
                    element = m.getElementByMetaId(metaid)
                    cv = CVTerm()
                    res = "http://identifiers.org/" + external_resource + "/" + accession_id
                    cv.addResource(res)
                    qs = qualifier.split(":")

                    if qs[0] == "bqbiol":
                        cv.setQualifierType(BIOLOGICAL_QUALIFIER)
                        qualifier_type = BiolQualifierType_fromString(qs[1])
                        cv.setBiologicalQualifierType(qualifier_type)
                    else:
                        cv.setQualifierType(MODEL_QUALIFIER)
                        qualifier_type = ModelQualifierType_fromString(qs[1])
                        cv.setModelQualifierType(qualifier_type)
                    
                    if element is not None:
                        print(">> Annotation:", res)
                        element.addCVTerm(cv)
                    else:
                        # the metaid of model
                        print("Model", metaid, "Or not found any matched element")
                        m.addCVTerm(cv)

            writeSBML(d, args[3])
    return errors

if __name__ == '__main__':
    main(sys.argv)
