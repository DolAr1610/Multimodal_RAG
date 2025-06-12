import time
from ingestion.ingest_text import ingest_texts
from ingestion.ingest_image import ingest_images

def main():
    try:
        print("1. Ingesting text embeddings...")
        start_time = time.time()
        #ingest_texts()
        print(f"Text embeddings processed successfully in {time.time() - start_time:.2f} seconds.")

        print("2. Ingesting image embeddings...")
        start_time = time.time()
        ingest_images()
        print(f"Image embeddings processed successfully in {time.time() - start_time:.2f} seconds.")

    except Exception as e:
        print(f"An error occurred during ingestion: {e}")
    else:
        print("All embeddings successfully ingested.")
    finally:
        print("Done.")

if __name__ == "__main__":
    main()