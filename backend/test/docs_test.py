import os
import shutil
import pytest
from pathlib import Path
from fastapi import HTTPException
from ..services import DocsService
from ..models import Document
from ..test.fake_data.docs import setup_docs_data


__authors__ = ["Michelle Nguyen"]


def test_get_all_documents(setup_docs_data):
    """Test retrieving all global documents."""
    test_env = setup_docs_data()
    DocsService.GLOBAL_DOCS_DIR = str(test_env / "es_files" / "global_docs")

    documents = DocsService.get_all_documents()

    # Ensure documents are sorted by title before checking since they are returned in a random order
    documents = sorted(documents, key=lambda doc: doc.title)

    assert len(documents) == 2
    assert isinstance(documents[0], Document)
    assert isinstance(documents[1], Document)

    assert documents[0].title == "sample1"
    assert documents[0].content == "Content for sample document 1"
    assert documents[1].title == "sample2"
    assert documents[1].content == "Content for sample document 2"


def test_get_document(setup_docs_data):
    """Test retrieving a specific global document."""
    test_env = setup_docs_data()
    DocsService.GLOBAL_DOCS_DIR = str(test_env / "es_files" / "global_docs")

    document = DocsService.get_document("sample1")

    assert isinstance(document, Document)
    assert document.title == "sample1"
    assert document.content == "Content for sample document 1"


def test_get_nonexistent_document(setup_docs_data):
    """Test retrieving a nonexistent document raises an Exception."""
    test_env = setup_docs_data()
    DocsService.GLOBAL_DOCS_DIR = str(test_env / "es_files" / "global_docs")

    with pytest.raises(HTTPException) as excinfo:
        DocsService.get_document("nonexistent")

    assert excinfo.value.status_code == 404


def test_upload_document(setup_docs_data):
    """Test uploading a new document."""
    test_env = setup_docs_data()
    DocsService.GLOBAL_DOCS_DIR = str(test_env / "es_files" / "global_docs")

    new_doc = DocsService.upload_document("New document content", "new_doc")

    assert isinstance(new_doc, Document)
    assert new_doc.title == "new_doc"
    assert new_doc.content == "New document content"

    file_path = Path(DocsService.GLOBAL_DOCS_DIR) / "new_doc.md"
    assert file_path.exists()


def test_upload_duplicate_document(setup_docs_data):
    """Test uploading a document with an existing title raises an Exception."""
    test_env = setup_docs_data()
    DocsService.GLOBAL_DOCS_DIR = str(test_env / "es_files" / "global_docs")

    DocsService.upload_document("Hello", "sample3")

    with pytest.raises(HTTPException) as excinfo:
        DocsService.upload_document("Bye", "sample3")

    assert excinfo.value.status_code == 409


def test_delete_document(setup_docs_data):
    """Test deleting a document."""
    test_env = setup_docs_data()
    DocsService.GLOBAL_DOCS_DIR = str(test_env / "es_files" / "global_docs")

    DocsService.delete_document("sample1")

    with pytest.raises(HTTPException) as excinfo:
        DocsService.get_document("sample1")

    assert excinfo.value.status_code == 404


def test_delete_all_documents(setup_docs_data):
    """Test deleting all documents."""
    test_env = setup_docs_data()
    DocsService.GLOBAL_DOCS_DIR = str(test_env / "es_files" / "global_docs")

    deleted_count = DocsService.delete_all_documents()
    assert deleted_count == 2

    documents = DocsService.get_all_documents()
    assert len(documents) == 0


def test_delete_nonexistent_document(setup_docs_data):
    """Test deleting a nonexistent document raises an Exception."""
    test_env = setup_docs_data()
    DocsService.GLOBAL_DOCS_DIR = str(test_env / "es_files" / "global_docs")

    with pytest.raises(HTTPException) as excinfo:
        DocsService.delete_document("nonexistent_doc")

    assert excinfo.value.status_code == 404


def test_get_all_documents_from_nonexistent_dir(setup_docs_data):
    """Test retrieving documents when the directory doesn't exist."""
    temp_dir = setup_docs_data()

    # Point to a nonexistent directory
    original_dir = DocsService.GLOBAL_DOCS_DIR
    DocsService.GLOBAL_DOCS_DIR = str(temp_dir / "nonexistent_dir")

    try:
        # Exercise
        documents = DocsService.get_all_documents()

        # Verify
        assert documents == []
    finally:
        # Restore the original directory
        DocsService.GLOBAL_DOCS_DIR = original_dir
        shutil.rmtree(temp_dir)


def test_get_all_documents_with_non_md_files(setup_docs_data):
    """Test retrieving documents when there are non-markdown files."""
    temp_dir = setup_docs_data()
    docs_dir = temp_dir / "es_files" / "global_docs"
    (docs_dir / "not_markdown.txt").write_text("This is not a markdown file")

    original_dir = DocsService.GLOBAL_DOCS_DIR
    DocsService.GLOBAL_DOCS_DIR = str(docs_dir)

    try:
        # Exercise
        documents = DocsService.get_all_documents()

        # Verify
        assert len(documents) == 2
        assert all(doc.title != "not_markdown" for doc in documents)
    finally:
        DocsService.GLOBAL_DOCS_DIR = original_dir
        shutil.rmtree(temp_dir)


def test_get_document_with_md_extension(setup_docs_data):
    """Test retrieving a document when title includes .md extension."""
    temp_dir = setup_docs_data()

    original_dir = DocsService.GLOBAL_DOCS_DIR
    DocsService.GLOBAL_DOCS_DIR = str(temp_dir / "es_files" / "global_docs")

    try:
        # Exercise
        document = DocsService.get_document("sample1.md")

        # Verify
        assert document.title == "sample1"
        assert document.content == "Content for sample document 1"
    finally:
        DocsService.GLOBAL_DOCS_DIR = original_dir
        shutil.rmtree(temp_dir)


def test_delete_document_with_md_extension(setup_docs_data):
    """Test deleting a document when title includes .md extension."""
    temp_dir = setup_docs_data()

    original_dir = DocsService.GLOBAL_DOCS_DIR
    DocsService.GLOBAL_DOCS_DIR = str(temp_dir / "es_files" / "global_docs")

    try:
        # Exercise
        result = DocsService.delete_document("sample1.md")

        # Verify
        assert "deleted successfully" in result["message"]
        doc_path = Path(DocsService.GLOBAL_DOCS_DIR) / "sample1.md"
        assert not os.path.exists(doc_path)
    finally:
        DocsService.GLOBAL_DOCS_DIR = original_dir
        shutil.rmtree(temp_dir)


def test_delete_all_documents_nonexistent_dir(setup_docs_data):
    """Test deleting all documents when the directory doesn't exist."""
    temp_dir = setup_docs_data()

    original_dir = DocsService.GLOBAL_DOCS_DIR
    DocsService.GLOBAL_DOCS_DIR = str(temp_dir / "nonexistent_dir")

    try:
        # Exercise
        deleted_count = DocsService.delete_all_documents()

        # Verify
        assert deleted_count == 0
    finally:
        DocsService.GLOBAL_DOCS_DIR = original_dir
        shutil.rmtree(temp_dir)
