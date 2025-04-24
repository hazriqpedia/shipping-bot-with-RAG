import pickle

META_PATH = "faiss_index/metadata.pkl"

try:
    with open(META_PATH, "rb") as f:
        metadata = pickle.load(f)
        print(metadata)
        for item in metadata:
            print(f"Type of item: {type(item)}")
except FileNotFoundError:
    print(f"File not found: {META_PATH}")
except Exception as e:
    print(f"Error loading metadata: {e}")
