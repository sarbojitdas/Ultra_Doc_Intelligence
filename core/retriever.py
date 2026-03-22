def retrieve_docs(query, retriever):
    return retriever.invoke(query)