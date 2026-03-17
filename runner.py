import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add project root to sys.path
sys.path.append(os.getcwd())

# Mock necessary modules for imports
mock_qdrant = MagicMock()
sys.modules["qdrant_client"] = mock_qdrant
sys.modules["qdrant_client.http"] = MagicMock()
sys.modules["langchain_qdrant"] = MagicMock()
sys.modules["langchain_openai"] = MagicMock()
sys.modules["langchain_core.documents"] = MagicMock()
sys.modules["langchain_core.prompts"] = MagicMock()
sys.modules["langchain_core.output_parsers"] = MagicMock()
sys.modules["langchain_core.runnables"] = MagicMock()
sys.modules["pypdf"] = MagicMock()
sys.modules["ragas"] = MagicMock()
sys.modules["ragas.metrics"] = MagicMock()
sys.modules["datasets"] = MagicMock()

class TestChunker(unittest.TestCase):
    def test_split_text(self):
        from app.services.chunker import chunker
        text = "This is a long text that needs to be split into chunks for the RAG pipeline. " * 50
        chunks = chunker.split_text(text)
        # Verify it splits (default chunk size 1000)
        self.assertTrue(len(chunks) > 1)

class TestSecurity(unittest.TestCase):
    def test_password_hashing(self):
        from app.core import security
        # We need passlib for this, which might fail if not installed
        try:
            password = "test_password"
            hashed = security.get_password_hash(password)
            self.assertTrue(security.verify_password(password, hashed))
            self.assertFalse(security.verify_password("wrong_password", hashed))
        except ImportError:
            self.skipTest("passlib not installed")

if __name__ == "__main__":
    unittest.main()
