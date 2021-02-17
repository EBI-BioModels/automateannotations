add_annotations.sh, the main runnable file coded in Bash.
add_annotations.py, the main script written in Python 3.
updated_annotations_samples.(xlsx, csv): structured data files containing annotations that you want to add to your models. The excel file facilitates for editing, then save as... as csv to make it as an input of the script.
*.xml are your SBML models.

How to run it.
From the terminal pointing to the folder containing these scripts, type:
sh add_annotations.sh model.xml annotations_added.csv updated_model.xml
Or
./add_annotations.sh model.xml annotations_added.csv updated_model.xml

