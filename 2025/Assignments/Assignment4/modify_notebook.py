import json

def modify_notebook():
    with open('main.ipynb', 'r') as f:
        nb = json.load(f)

    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            source = cell['source']
            source_text = "".join(source)

            # TODO4-3 loop (Updated for Recall@1, Recall@5, EM)
            if "# TODO4-3: Run the RAG system" in source_text:
                cell['source'] = [
                    "results = []\n",
                    "correct_count = 0\n",
                    "recall_1_count = 0\n",
                    "recall_5_count = 0\n",
                    "\n",
                    "print(\"Starting evaluation...\")\n",
                    "\n",
                    "for i, query in tqdm(enumerate(queries), total=len(queries)):\n",
                    "    # 1. Retrieve Documents explicitly to measure Recall\n",
                    "    # We retrieve k=5 to measure Recall@5\n",
                    "    retrieved_docs = retriever.get_relevant_documents(query)\n",
                    "    \n",
                    "    # Ground Truth Fact ID for this question is 'i' (since Q1 -> Fact1)\n",
                    "    # But we need to match content since ID might not be preserved perfectly in Chroma retrieval result metadata if not set carefully.\n",
                    "    # However, we saved metadata={'id': i} in TODO2-2.\n",
                    "    target_id = i\n",
                    "    \n",
                    "    # Calculate Recall@1\n",
                    "    if len(retrieved_docs) > 0 and retrieved_docs[0].metadata.get('id') == target_id:\n",
                    "        recall_1_count += 1\n",
                    "        \n",
                    "    # Calculate Recall@5\n",
                    "    # Check if target_id is in any of the top 5 docs\n",
                    "    # Note: retriever might return fewer than 5 if k=3 was set in definition. \n",
                    "    # We should ensure k=5 or check whatever is returned.\n",
                    "    found_in_top_5 = any(doc.metadata.get('id') == target_id for doc in retrieved_docs[:5])\n",
                    "    if found_in_top_5:\n",
                    "        recall_5_count += 1\n",
                    "\n",
                    "    # 2. Generate Answer\n",
                    "    # We pass the retrieved docs to the chain\n",
                    "    response = question_answer_chain.invoke({\"input\": query, \"context\": retrieved_docs})\n",
                    "    # response is just the string answer from stuff_documents_chain usually, or a dict depending on chain type.\n",
                    "    # create_stuff_documents_chain returns a Runnable that outputs string (usually).\n",
                    "    # Let's verify output format. It usually returns the string output of LLM.\n",
                    "    pred = response\n",
                    "    if isinstance(response, dict) and 'answer' in response:\n",
                    "        pred = response['answer']\n",
                    "    \n",
                    "    # 3. Calculate Exact Match (EM)\n",
                    "    # We check if the ground truth answer string is contained in the prediction\n",
                    "    is_correct = answers[i].lower() in pred.lower()\n",
                    "    if is_correct:\n",
                    "        correct_count += 1\n",
                    "    \n",
                    "    results.append({\n",
                    "        \"Query\": query,\n",
                    "        \"Ground_Truth\": answers[i],\n",
                    "        \"Prediction\": pred\n",
                    "    })\n",
                    "\n",
                    "total = len(queries)\n",
                    "print(f\"Recall@1: {recall_1_count / total:.4f}\")\n",
                    "print(f\"Recall@5: {recall_5_count / total:.4f}\")\n",
                    "print(f\"EM Accuracy: {correct_count / total:.4f}\")\n",
                    "\n",
                    "# Save to JSON\n",
                    "with open('NLP_HW4_NTHU_12345678.json', 'w') as f:\n",
                    "    json.dump(results, f, indent=4)\n"
                ]

            # Also need to ensure retriever gets 5 docs for the loop to work for Recall@5
            if "# TODO2-2: Prepare the retrieval database" in source_text:
                 cell['source'] = [
                    "# TODO2-2: Prepare the retrieval database\n",
                    "# You should create a Chroma vector store.\n",
                    "vector_store = Chroma.from_documents(\n",
                    "    documents=docs,\n",
                    "    embedding=embeddings_model,\n",
                    "    collection_name=\"cat_facts\"\n",
                    ")\n",
                    "# We set k=5 here to ensure we can measure Recall@5\n",
                    "retriever = vector_store.as_retriever(\n",
                    "    search_type=\"similarity\",\n",
                    "    search_kwargs={\"k\": 5}\n",
                    ")\n"
                ]

    with open('main.ipynb', 'w') as f:
        json.dump(nb, f, indent=2)

if __name__ == "__main__":
    modify_notebook()
