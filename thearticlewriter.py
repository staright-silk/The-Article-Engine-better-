import os
import shutil
from whoosh.fields import Schema, TEXT
from whoosh.index import create_in
from whoosh.qparser import MultifieldParser
from whoosh.scoring import TF_IDF

INDEX_DIR = "indexdir"

if os.path.exists(INDEX_DIR):
    shutil.rmtree(INDEX_DIR)
os.mkdir(INDEX_DIR)

schema = Schema(
    title=TEXT(stored=True),
    content=TEXT(stored=True)
)

ix = create_in(INDEX_DIR, schema)
writer = ix.writer()

writer.add_document(
    title="The Stars Beyond Us",
    content="""We’ve always looked up. Before we built cities, before we named constellations,
before we understood what light-years meant, we looked up and wondered.
The stars were gods, maps, omens, stories stitched into mythologies."""
)

writer.add_document(
    title="What Is Literature?",
    content="""Literature is the art of expressing human thoughts, emotions,
and experiences through written language, stories, poetry, and drama."""
)

writer.add_document(
    title="What is Life?",
    content="""tanziruz"""
)

writer.commit()

def search(query_string):
    with ix.searcher(weighting=TF_IDF()) as searcher:
        parser = MultifieldParser(["title", "content"], ix.schema)
        query = parser.parse(query_string)
        results = searcher.search(query)
        return [(r["title"], r["content"]) for r in results]

if __name__ == "__main__":
    while True:
        user_query = input("Enter search query (or 'quit'): ").strip()
        if user_query.lower() == "quit":
            break
        if not user_query:
            print("Please enter a valid query.")
            continue

        results = search(user_query)
        if results:
            for i, (title, content) in enumerate(results, 1):
                print(f"\nResult {i}")
                print("Title:", title)
                print("Content:", content)
        else:
            print("No results found.")