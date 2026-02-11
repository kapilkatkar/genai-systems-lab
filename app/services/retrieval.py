"""
Handles similarity search and filtering.
"""

def retrieve_chunks(vectorstore, query: str, domain: str, top_k: int = 5, max_distance: float = 1.2):
    """
    Retrieve relevant chunks using similarity search.

    Notes:
    - Chroma returns distance (lower is better)
    - We filter using max_distance
    - Domain filter is applied using metadata
    """

    # Get top_k results with scores
    results = vectorstore.similarity_search_with_score(
        query,
        k=top_k,
        filter={"domain": domain}
    )

    print(f"Query: {query}")
    print(f"Domain: {domain}")
    print(f"Total results returned: {len(results)}")

    filtered_chunks = []

    for idx, (doc, score) in enumerate(results):
        source = doc.metadata.get("source", "unknown")
        doc_domain = doc.metadata.get("domain", "unknown")

        print(f"Result {idx+1} | score: {score:.4f} | source: {source} | domain: {doc_domain}")
        print(f"Chunk preview: {doc.page_content[:150]}...\n")

        # Filter by distance threshold
        if score <= max_distance:
            filtered_chunks.append({
                "text": doc.page_content,
                "source": source,
                "domain": doc_domain,
                "score": score
            })

    print(f"Filtered chunks count: {len(filtered_chunks)}\n")
    return filtered_chunks
