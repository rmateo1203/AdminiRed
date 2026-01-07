#!/usr/bin/env python
"""
Script para generar un SECRET_KEY seguro para Django.
Uso: python generate_secret_key.py
"""
from django.core.management.utils import get_random_secret_key

if __name__ == '__main__':
    secret_key = get_random_secret_key()
    print("\n" + "="*70)
    print("SECRET_KEY generado:")
    print("="*70)
    print(secret_key)
    print("="*70)
    print("\n⚠️  IMPORTANTE: Copia este valor y agrégalo a tu archivo .env")
    print("   como: SECRET_KEY='tu_clave_aqui'\n")
    print("   NO compartas este valor ni lo subas a repositorios públicos.\n")


