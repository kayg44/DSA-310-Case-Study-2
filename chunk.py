def chunk_text(text, chunk_size=700, overlap=50):
    words = text.split()
    chunks = []
    i = 0
    chunk_id = 0
    
    while i < len(words):
        chunk_words = words[i:i+chunk_size]
        chunk_text = " ".join(chunk_words)
        
        chunks.append({
            "chunk_id": f"chunk_{chunk_id}",
            "text": chunk_text
        })
        
        i += chunk_size - overlap
        chunk_id += 1
    
    return chunks