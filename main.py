import os
from wf import extract_embeddings

if __name__ == "__main__":
    OUTPUT_DIR = './EMS2_EMBEDDINGS'
    os.mkdir(OUTPUT_DIR)
    extract_embeddings(output_dir=OUTPUT_DIR)
