import json

def modify_notebook():
    with open('main.ipynb', 'r') as f:
        nb = json.load(f)

    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            source = cell['source']
            source_text = "".join(source)

            # TODO4-3: Run RAG and Load Questions (FIXED LOADING)
            if "# Please load the questions_answers.txt file" in source_text:
                 cell['source'] = [
                    "# Question (queries) and answer pairs\n",
                    "# Please load the questions_answers.txt file and prepare the `queries` and `answers` lists.\n",
                    "queries = []\n",
                    "answers = []\n",
                    "with open('questions_answers.txt', 'r') as f:\n",
                    "    # Read all non-empty lines\n",
                    "    lines = [l.strip() for l in f if l.strip()]\n",
                    "    \n",
                    "    # Assuming alternating Question / Answer structure after removing blanks\n",
                    "    # File format seen: Q, A, Blank, Q, A, Blank...\n",
                    "    queries = lines[0::2]\n",
                    "    answers = lines[1::2]\n",
                    "    \n",
                    "print(f\"Loaded {len(queries)} queries and {len(answers)} answers.\")\n"
                 ]

    with open('main.ipynb', 'w') as f:
        json.dump(nb, f, indent=2)

if __name__ == "__main__":
    modify_notebook()


