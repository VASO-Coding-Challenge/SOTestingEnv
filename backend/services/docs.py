"""Service to handle manipulation of global docs for ES GUI"""

import os

from typing import List
from fastapi import HTTPException

from ..models import Document


__author__ = ["Michelle Nguyen"]


class DocsService:
    """Service to handle global docs management"""

    GLOBAL_DOCS_DIR = "es_files/global_docs"

    @staticmethod
    def get_all_documents() -> List[Document]:
        """Retrieve all available global documents."""
        try:
            if not os.path.exists(DocsService.GLOBAL_DOCS_DIR):
                return []

            documents = []
            for filename in os.listdir(DocsService.GLOBAL_DOCS_DIR):
                if not filename.endswith(".md"):
                    continue

                try:
                    doc_path = os.path.join(DocsService.GLOBAL_DOCS_DIR, filename)
                    with open(doc_path, "r") as f:
                        content = f.read()

                    doc_title = filename[:-3]
                    documents.append(Document(content=content, title=doc_title))
                except Exception:
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
            if not title.endswith(".md"):
                filename = f"{title}.md"
            else:
                filename = title
                title = title[:-3]

            doc_path = os.path.join(DocsService.GLOBAL_DOCS_DIR, filename)

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
    def upload_document(content: str, title: str):
        """Upload a document to the global docs directory.

        Args:
            content: The content of the document
            title: The title of the document

        Returns:
            Document: The uploaded document

        Raises:
            HTTPException: If a document with the same title already exists
        """
        try:
            filename = f"{title}.md"
            file_path = os.path.join(DocsService.GLOBAL_DOCS_DIR, filename)

            if os.path.exists(file_path):
                raise HTTPException(
                    status_code=409,
                    detail=f"A document with title '{title}' already exists. Please use a different title.",
                )

            os.makedirs(DocsService.GLOBAL_DOCS_DIR, exist_ok=True)

            with open(file_path, "w") as f:
                f.write(content)

            return Document(title=title, content=content)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error uploading document: {str(e)}"
            )

    @staticmethod
    def delete_document(title: str):
        """Delete a global document."""
        try:
            if not title.endswith(".md"):
                filename = f"{title}.md"
            else:
                filename = title
                title = title[:-3]

            file_path = os.path.join(DocsService.GLOBAL_DOCS_DIR, filename)

            if not os.path.exists(file_path):
                raise HTTPException(
                    status_code=404, detail=f"Document '{title}' not found."
                )

            os.remove(file_path)
            return {"message": f"Document '{title}' deleted successfully"}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error deleting document: {str(e)}"
            )

    @staticmethod
    def delete_all_documents():
        """Delete all global documents.

        Returns:
            int: The number of documents deleted
        """
        try:
            deleted_count = 0

            if not os.path.exists(DocsService.GLOBAL_DOCS_DIR):
                return deleted_count

            for filename in os.listdir(DocsService.GLOBAL_DOCS_DIR):
                if filename.endswith(".md"):
                    file_path = os.path.join(DocsService.GLOBAL_DOCS_DIR, filename)

                    os.remove(file_path)
                    deleted_count += 1

            return deleted_count
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error deleting documents: {str(e)}"
            )
