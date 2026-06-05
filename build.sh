#!/usr/bin/env bash
# exit on error
set -o errexit

echo "=========================================="
echo "    INICIANDO SCRIPT DE CONSTRUCCIÓN       "
echo "=========================================="

# 1. Instalar dependencias de Python
echo "-> Instalando paquetes de Python..."
pip install -r requirements.txt

# 2. Descargar y copiar los binarios de Prisma en la ruta del proyecto
echo "-> Descargando y moviendo motores de Prisma..."
python copy_binaries.py

# 3. Generar el cliente de Prisma Python
echo "-> Generando cliente Prisma..."
prisma generate

echo "=========================================="
echo "    CONSTRUCCIÓN COMPLETADA CON ÉXITO     "
echo "=========================================="
