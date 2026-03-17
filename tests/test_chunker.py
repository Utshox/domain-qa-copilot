from app.services.chunker import chunker

def test_split_text():
    text = "This is a long text that needs to be split into chunks for the RAG pipeline. " * 50
    chunks = chunker.split_text(text)
    assert len(chunks) > 1
    assert all(len(c.page_content) <= 1200 for c in chunks) # allowance for overlap

def test_split_text_with_metadata():
    text = "Hello world"
    metadata = {"source": "test.txt"}
    chunks = chunker.split_text(text, metadata=metadata)
    assert len(chunks) == 1
    assert chunks[0].metadata["source"] == "test.txt"
