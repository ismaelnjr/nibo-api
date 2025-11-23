"""
Gerenciador de comandos CLI unificado para Nibo API
"""
import argparse
import sys


def main():
    """Interface de linha de comando principal unificada"""
    parser = argparse.ArgumentParser(
        description="CLI unificado para interagir com as APIs Nibo",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:

  # Comandos de Empresa
  python manage.py empresa organizacoes
  python manage.py empresa clientes --org org_123
  python manage.py empresa agendamentos-receber --org org_123

  # Comandos de Obrigações
  python manage.py obrigacoes escritorios
  python manage.py obrigacoes clientes
  python manage.py obrigacoes obrigacoes --cliente "Nome Cliente"

  # Use --help para ver comandos disponíveis de cada módulo
  python manage.py empresa --help
  python manage.py obrigacoes --help
        """
    )
    
    subparsers = parser.add_subparsers(dest="modulo", help="Módulos disponíveis", required=True)
    
    # Subparser para empresa
    parser_empresa = subparsers.add_parser(
        "empresa",
        help="Comandos para API Nibo Empresa"
    )
    
    # Subparser para obrigacoes
    parser_obrigacoes = subparsers.add_parser(
        "obrigacoes",
        help="Comandos para API Nibo Obrigações"
    )
    
    # Roteia para o módulo apropriado
    if len(sys.argv) < 2:
        parser.print_help()
        return 0
    
    modulo = sys.argv[1]
    
    if modulo == "empresa":
        from nibo_api.empresa.management.cli import main_cli as empresa_main_cli
        # Remove "manage.py" e "empresa" dos argumentos e passa o resto
        sys.argv = sys.argv[1:]  # Remove "manage.py", mantém "empresa" e o resto
        return empresa_main_cli()
    
    elif modulo == "obrigacoes":
        from nibo_api.obrigacoes.management.cli import main_cli as obrigacoes_main_cli
        # Remove "manage.py" e "obrigacoes" dos argumentos e passa o resto
        sys.argv = sys.argv[1:]  # Remove "manage.py", mantém "obrigacoes" e o resto
        return obrigacoes_main_cli()
    
    parser.print_help()
    return 0


if __name__ == "__main__":
    exit(main())

