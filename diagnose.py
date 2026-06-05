import socket
import sys
import os
import asyncio
from urllib.parse import urlparse
from dotenv import load_dotenv

# Load env variables from .env file
load_dotenv()

print("==================================================")
print("   DIAGNÓSTICO DE CONEXIÓN A BASE DE DATOS      ")
print("==================================================")

db_url = os.getenv("DATABASE_URL")
if not db_url:
    print("❌ ERROR: No se encontró DATABASE_URL en el archivo .env")
    sys.exit(1)

# Parse URL
try:
    parsed = urlparse(db_url)
    host = parsed.hostname
    port = parsed.port or 5432
    user = parsed.username
    db_name = parsed.path.lstrip('/')
    print(f"Database URL detectada.")
    print(f"-> Host: {host}")
    print(f"-> Port: {port}")
    print(f"-> User: {user}")
    print(f"-> Database: {db_name}")
except Exception as e:
    print(f"❌ ERROR al parsear DATABASE_URL: {e}")
    sys.exit(1)

# 1. DNS Resolution
print("\n[1/3] Resolviendo DNS del host...")
try:
    ip = socket.gethostbyname(host)
    print(f"✅ DNS resuelto con éxito: {host} -> {ip}")
except Exception as e:
    print(f"❌ ERROR de DNS: No se pudo resolver el host {host}.")
    print(f"   Detalles: {e}")
    sys.exit(1)

# 2. TCP Socket Connection
print("\n[2/3] Probando conexión TCP (Sockets)...")
for p in [5432, 6543]:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((host, p))
        s.close()
        print(f"✅ Puerto {p}: Conectado correctamente (Servidor activo y escuchando).")
    except Exception as e:
        print(f"❌ Puerto {p}: No disponible / Bloqueado por firewall. Detalles: {e}")

# 3. Prisma Connection Test
print("\n[3/3] Probando conexión a través del Cliente Prisma...")
try:
    from prisma import Prisma

    async def test_prisma():
        db = Prisma()
        print("-> Llamando a db.connect()...")
        await db.connect()
        print("✅ Prisma se ha conectado correctamente!")
        print("-> Ejecutando consulta de prueba 'SELECT 1;'...")
        res = await db.execute_raw("SELECT 1;")
        print(f"✅ Consulta exitosa! Resultado: {res}")
        await db.disconnect()
        print("-> db.disconnect() ejecutado.")

    asyncio.run(test_prisma())
except Exception as e:
    print(f"❌ ERROR en Prisma: El motor de Prisma no pudo establecer la conexión.")
    print(f"   Detalles del error:")
    print(e)

print("\n==================================================")
