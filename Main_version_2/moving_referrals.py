import os
import shutil

# This function moves triaged documents into a separate folder
def move_documents(source_file: str, sample_documents: str, processed_folder: str = "processed_documents"):
    os.makedirs(processed_folder, exist_ok=True)
    
    source_path = os.path.join(sample_documents, source_file)
    target_path = os.path.join(processed_folder, source_file)
    
    try:
        shutil.move(source_path, target_path)
    except Exception as e:
        print("Error moving processed documents to folder, {source_file}: {e}")