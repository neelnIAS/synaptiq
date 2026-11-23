from apps.api.rag import split_text

def test_split_text():
    chunks = split_text("A" * 2000, chunk_size=500, overlap=50)
    assert len(chunks) > 1
    assert all(chunks)
