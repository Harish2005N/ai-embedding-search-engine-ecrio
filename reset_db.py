import os
import shutil

DATA_DIR = "data"

def reset():
    print("Resetting database and FAISS index...")
    if os.path.exists(DATA_DIR):
        try:
            # Delete index and documents
            for filename in os.listdir(DATA_DIR):
                file_path = os.path.join(DATA_DIR, filename)
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            print("Successfully cleared data folder.")
        except Exception as e:
            print(f"Error resetting: {e}")
    else:
        print("Data directory does not exist.")

if __name__ == "__main__":
    reset()
