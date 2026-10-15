"""
conftest.py - Fixture cấu hình toàn cục cho Test Suite Tầng 1 và Tầng 2.
"""

import sys
from pathlib import Path
import pytest
from neo4j import GraphDatabase
from qdrant_client import QdrantClient

# Thêm đường dẫn mã nguồn vietlawbert vào PYTHONPATH
VIETLAWBERT_ROOT = Path("/home/dell/Desktop/vietlawbert")
if str(VIETLAWBERT_ROOT) not in sys.path:
    sys.path.insert(0, str(VIETLAWBERT_ROOT))

# Thêm đường dẫn dữ liệu
STORAGE_ROOT = Path("/mnt/data/vietlawbert_data")


@pytest.fixture(scope="session")
def project_paths():
    return {
        "root": VIETLAWBERT_ROOT,
        "raw_shards": STORAGE_ROOT / "raw_shards",
        "processed_parquet": STORAGE_ROOT / "processed_parquet",
        "bulk_vectors": STORAGE_ROOT / "bulk_vectors",
    }


@pytest.fixture(scope="session")
def neo4j_driver():
    """Khởi tạo driver kết nối Neo4j Bolt."""
    uri = "bolt://localhost:7687"
    auth = ("neo4j", "vietlawbert")
    driver = GraphDatabase.driver(uri, auth=auth)
    with driver.session() as session:
        session.run("RETURN 1 AS ping")
    yield driver
    driver.close()


@pytest.fixture(scope="session")
def qdrant_client():
    """Khởi tạo client kết nối Qdrant Engine (loại bỏ cờ check_compatibility gây lỗi httpx)."""
    client = QdrantClient(host="localhost", port=6333, timeout=60.0)
    yield client