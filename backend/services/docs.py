import os

from typing import List
from fastapi import HTTPException
from models import Document


__author__ = ["Michelle Nguyen"]


class DocsService:
    """Service to handle global document operations"""

    GLOBAL_DOCS_DIR = "es_files/global_docs"

    @staticmethod
    def get_documents() -> List[Document]:
        """Retrieve all available global documents."""
        try:
            # Return empty list when no documents exist
            if not os.path.exists(GlobalDocumentService.GLOBAL_DOCS_DIR):
                return []

            documents = []
            for filename in os.listdir(GlobalDocumentService.GLOBAL_DOCS_DIR):
                if not filename.endswith(".md"):
                    continue

                try:
                    doc_path = os.path.join(
                        GlobalDocumentService.GLOBAL_DOCS_DIR, filename
                    )
                    with open(doc_path, "r") as f:
                        content = f.read()

                    doc_title = filename[:-3]  # Remove .md extension
                    documents.append(Document(content=content, title=doc_title))
                except Exception:
                    # Skip files that can't be read
                    continue

            return documents
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error fetching documents: {str(e)}"
            )

    @staticmethod
    def get_document(title: str) -> Document:
        """Retrieve a specific global document by title."""
        try:
            # Ensure filename has .md extension
            if not title.endswith(".md"):
                filename = f"{title}.md"
            else:
                filename = title
                title = title[:-3]  # Remove .md for the document title

            doc_path = os.path.join(GlobalDocumentService.GLOBAL_DOCS_DIR, filename)

            if not os.path.exists(doc_path):
                raise HTTPException(
                    status_code=404, detail=f"Document '{title}' not found."
                )

            with open(doc_path, "r") as f:
                content = f.read()

            return Document(content=content, title=title)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error retrieving document '{title}': {str(e)}"
            )

    @staticmethod
    def upload_document(content: str, title: str) -> Document:
        """Upload a global document."""
        try:
            # Ensure filename has .md extension
            if not title.endswith(".md"):
                filename = f"{title}.md"
            else:
                filename = title
                title = title[:-3]  # Remove .md for the document title

            # Create directory if it doesn't exist
            os.makedirs(GlobalDocumentService.GLOBAL_DOCS_DIR, exist_ok=True)

            # Full path to file
            file_path = os.path.join(GlobalDocumentService.GLOBAL_DOCS_DIR, filename)

            # Write content to file
            with open(file_path, "w") as f:
                f.write(content)

            return Document(content=content, title=title)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error uploading document: {str(e)}"
            )

    @staticmethod
    def delete_document(title: str):
        """Delete a global document."""
        try:
            # Ensure filename has .md extension
            if not title.endswith(".md"):
                filename = f"{title}.md"
            else:
                filename = title
                title = title[:-3]  # Remove .md for the document title

            # Full path to file
            file_path = os.path.join(GlobalDocumentService.GLOBAL_DOCS_DIR, filename)

            # Check if file exists
            if not os.path.exists(file_path):
                raise HTTPException(
                    status_code=404, detail=f"Document '{title}' not found."
                )

            # Delete file
            os.remove(file_path)
            return {"message": f"Document '{title}' deleted successfully"}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error deleting document: {str(e)}"
            )
