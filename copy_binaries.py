import os
import shutil
import sys
from pathlib import Path

def main():
    print("--- Descargando binarios de Prisma ---")
    # Execute prisma py fetch to download the binaries
    exit_code = os.system("prisma py fetch")
    if exit_code != 0:
        print("❌ Error al ejecutar 'prisma py fetch'")
        sys.exit(1)

    print("--- Buscando binarios en directorios de caché ---")
    # Standard cache directories where prisma py fetch puts the binaries
    possible_dirs = [
        Path(os.path.expanduser("~/.cache/prisma-python/binaries")),
        Path("/opt/render/.cache/prisma-python/binaries"),
        Path("/root/.cache/prisma-python/binaries")
    ]

    found = False
    for cache_dir in possible_dirs:
        print(f"Buscando en: {cache_dir}...")
        if cache_dir.exists():
            # Search recursively for query engine binaries (both with and without prisma- prefix)
            # We look for files starting with 'query-engine-' or 'prisma-query-engine-'
            engine_files = list(cache_dir.glob("**/query-engine-*")) + list(cache_dir.glob("**/prisma-query-engine-*"))
            for path in engine_files:
                # Ensure the destination file in the project root starts with 'prisma-query-engine-'
                name = path.name
                if not name.startswith("prisma-"):
                    dest_name = f"prisma-{name}"
                else:
                    dest_name = name
                
                dest = Path(".") / dest_name
                print(f"✅ Encontrado: {path}")
                print(f"-> Copiando a: {dest.resolve()}")
                
                # Copy and set executable permissions
                shutil.copy(path, dest)
                os.chmod(dest, 0o755)
                found = True
            
            # Also copy schema/migration engines if present
            for path in cache_dir.glob("**/schema-engine-*"):
                dest = Path(".") / path.name
                shutil.copy(path, dest)
                os.chmod(dest, 0o755)

    if not found:
        print("❌ ERROR: No se encontró ningún binario de Prisma en las rutas de caché.")
        sys.exit(1)
    else:
        print("✅ Configuración de binarios completada con éxito.")

if __name__ == "__main__":
    main()
