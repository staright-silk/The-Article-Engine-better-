import os
from whoosh.fields import Schema, TEXT, ID
from whoosh.index import create_in, open_dir
from whoosh.qparser import MultifieldParser
from whoosh.scoring import TF_IDF
from config import INDEX_DIR

schema = Schema(
    article_id=ID(stored=True),
    title=TEXT(stored=True),
    content=TEXT(stored=True)
)

if not os.path.exists(INDEX_DIR):
    os.mkdir(INDEX_DIR)
    create_in(INDEX_DIR, schema)

def add_to_index(article):
    ix = open_dir(INDEX_DIR)
    writer = ix.writer()
    writer.add_document(
        article_id=str(article.id),
        title=article.title,
        content=article.content
    )
    writer.commit()

def search_index(query_string):
    ix = open_dir(INDEX_DIR)
    with ix.searcher(weighting=TF_IDF()) as searcher:
        parser = MultifieldParser(["title", "content"], ix.schema)
        query = parser.parse(query_string)
        return searcher.search(query, limit=10)
