#!/usr/bin/env python
"""
Script de teste para verificar se o pacote foi instalado corretamente
Execute após: pip install -e .
"""

try:
    import nibo_api
    print(f"✓ nibo_api importado com sucesso")
    print(f"  Versão: {nibo_api.__version__}")
    
    # Testar imports principais
    from nibo_api import NiboSettings
    print("✓ NiboSettings importado")
    
    from nibo_api import NiboEmpresaClient
    print("✓ NiboEmpresaClient importado")
    
    from nibo_api import NiboObrigacoesClient
    print("✓ NiboObrigacoesClient importado")
    
    from nibo_api import (
        NiboAPIError,
        NiboAuthenticationError,
        NiboNotFoundError,
        NiboValidationError,
        NiboServerError,
        NiboRateLimitError
    )
    print("✓ Todas as exceções importadas")
    
    print("\n✅ Todos os testes passaram! O pacote está instalado corretamente.")
    
except ImportError as e:
    print(f"❌ Erro ao importar: {e}")
    exit(1)
except Exception as e:
    print(f"❌ Erro inesperado: {e}")
    exit(1)
