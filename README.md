# SCRIPT TO ANNOTATE SBML MODELS AUTOMATICALLY

## Files
* `add_annotations.sh`, the main runnable file coded in Bash.
* `add_annotations.py`, the main script written in Python 3.
* `updated_annotations_samples.(xlsx, csv)`: structured data files containing annotations that you want to add to your models. The excel file facilitates for editing, then save as... as csv to make it as an input of the script.
* `*.xml` are your SBML models.

##How to install required packages/libraries
This script requires `libsbml` installed. To install it, the easiest way is to run the following command.
```
pip install -r requirements.txt
```

## How to run it.

From the terminal pointing to the folder containing these scripts, type:

`sh add_annotations.sh model.xml annotations_added.csv updated_model.xml`

Or

`./add_annotations.sh model.xml annotations_added.csv updated_model.xml`

## How to run the script to extract annotations

To contribute to the building the input file for the script of adding annotations, we also provide with you the script to extract annotations being used in your SBML file.

The script will return data in CSV format but you need to pipe the output into a file.

To run the script, just hit Enter after the following command:

`sh extract_elements.sh your_SBML_file.xml`

To save the output into a file, run as below:

`sh extract_elements.sh your_SBML_file.xml > elements.csv`


### Enjoy your work!