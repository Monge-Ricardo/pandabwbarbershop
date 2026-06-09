import socket
import os
import sys
from urllib.parse import urlparse

db_url = os.environ.get("DATABASE_URL")
print(f"DATABASE_URL: {db_url}")

if not db_url:
    print("FAILED: DATABASE_URL is not set.")
    sys.exit(1)

try:
    parsed = urlparse(db_url)
    host = parsed.hostname
    port = parsed.port or 5432
    print(f"Testing connection to {host}:{port}...")
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    s.connect((host, port))
    s.close()
    print("SUCCESS: Connected to database port!")
except Exception as e:
    print(f"FAILED: Cannot connect to database. Error: {e}")
    sys.exit(1)
