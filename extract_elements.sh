PYTHON=python
SCRIPT=extract_elements.py
MODEL_FILE=$1
export CMD="$PYTHON $SCRIPT $MODEL_FILE"
${CMD}
