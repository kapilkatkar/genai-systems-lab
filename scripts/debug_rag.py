import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.vectorstore import get_vectorstore

def debug(domain: str, query: str):
    vs = get_vectorstore()
    print("Total vectors:", vs._collection.count())

    results = vs.similarity_search(query, k=5)
    print("Retrieved chunks:", len(results))
    for idx, r in enumerate(results):
        print(f"\n--- Result {idx+1} ---")
        print(r.page_content[:300])

if __name__ == "__main__":
    debug("sales", "refund policy")
