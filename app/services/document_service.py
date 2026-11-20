import json
import os
from typing import Dict, List, Optional
from app.models.schemas import DocumentInfo

DATA_DIR = "data"
DOCUMENTS_FILE = os.path.join(DATA_DIR, "documents.json")

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

class DocumentStore:
    def __init__(self):
        self.documents: Dict[int, DocumentInfo] = {}
        self.next_id = 1
        self.load_documents()

    def load_documents(self):
        if os.path.exists(DOCUMENTS_FILE):
            try:
                with open(DOCUMENTS_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for item in data:
                        doc = DocumentInfo(**item)
                        self.documents[doc.id] = doc
                    if self.documents:
                        self.next_id = max(self.documents.keys()) + 1
            except Exception as e:
                print(f"Error loading documents: {e}")

    def save_documents(self):
        try:
            with open(DOCUMENTS_FILE, 'w', encoding='utf-8') as f:
                data = [doc.model_dump() for doc in self.documents.values()]
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error saving documents: {e}")

    def add_document(self, title: str, content: str) -> DocumentInfo:
        doc = DocumentInfo(id=self.next_id, title=title, content=content)
        self.documents[self.next_id] = doc
        self.next_id += 1
        self.save_documents()
        return doc
        
    def get_document(self, doc_id: int) -> Optional[DocumentInfo]:
        return self.documents.get(doc_id)

    def get_all_documents(self) -> List[DocumentInfo]:
        return list(self.documents.values())

    def delete_document(self, doc_id: int) -> bool:
        if doc_id in self.documents:
            del self.documents[doc_id]
            self.save_documents()
            return True
        return False

# Global instance
document_store = DocumentStore()
