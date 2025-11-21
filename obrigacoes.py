"""
Módulo de comandos para interagir com a API Nibo Obrigações
Fornece funções para listar obrigações, clientes, contatos, etc.
"""
import argparse
import json
from datetime import datetime, date
from typing import Optional, List, Dict, Any
from uuid import UUID
from nibo_api.config import NiboConfig
from nibo_api.obrigacoes.client import NiboObrigacoesClient
from nibo_api.obrigacoes.tarefas import (
    interpretar_status,
    interpretar_skip_holiday,
    interpretar_frequency,
    interpretar_frequency_schedule
)


def parse_date(date_str):
    """Parse uma data de string para objeto date"""
    if not date_str or date_str == "N/A":
        return None
    try:
        date_str = str(date_str).strip()
        # Tenta formato DD/MM/YYYY primeiro
        if "/" in date_str:
            parts = date_str.split("/")
            if len(parts) == 3:
                return date(int(parts[2]), int(parts[1]), int(parts[0]))
        # Tenta formato ISO (YYYY-MM-DD ou YYYY-MM-DDTHH:MM:SS)
        date_str = date_str.split("T")[0].replace("Z", "")
        return datetime.fromisoformat(date_str).date()
    except:
        return None


def format_date(date_obj):
    """Formata uma data para exibição"""
    if isinstance(date_obj, date):
        return date_obj.strftime("%d/%m/%Y")
    return str(date_obj)


def listar_escritorios() -> Dict[str, Any]:
    """
    Lista todos os escritórios contábeis
    
    Returns:
        Dicionário com 'items' (lista de escritórios) e 'metadata'
    """
    config = NiboConfig()
    client = NiboObrigacoesClient(config)
    return client.escritorios.listar()


def listar_clientes(accounting_firm_id: Optional[UUID] = None, nome_cliente: Optional[str] = None) -> Dict[str, Any]:
    """
    Lista clientes de um escritório contábil
    
    Args:
        accounting_firm_id: UUID do escritório. Se None, usa o primeiro disponível.
        nome_cliente: Nome do cliente para filtrar (opcional)
        
    Returns:
        Dicionário com 'items' (lista de clientes) e 'metadata'
    """
    config = NiboConfig()
    client = NiboObrigacoesClient(config)
    
    if accounting_firm_id is None:
        escritorios = client.escritorios.listar()
        if not escritorios.get("items"):
            raise ValueError("Nenhum escritório encontrado")
        accounting_firm_id = UUID(escritorios["items"][0]["id"])
    
    if nome_cliente:
        # Usa contains para busca parcial
        # Escapa aspas simples no nome do cliente
        nome_escape = nome_cliente.replace("'", "''")
        return client.clientes.listar(
            accounting_firm_id=accounting_firm_id,
            odata_filter=f"contains(name, '{nome_escape}')"
        )
    
    return client.clientes.listar(accounting_firm_id=accounting_firm_id)


def listar_contatos(accounting_firm_id: Optional[UUID] = None) -> Dict[str, Any]:
    """
    Lista contatos de um escritório contábil
    
    Args:
        accounting_firm_id: UUID do escritório. Se None, usa o primeiro disponível.
        
    Returns:
        Dicionário com 'items' (lista de contatos) e 'metadata'
    """
    config = NiboConfig()
    client = NiboObrigacoesClient(config)
    
    if accounting_firm_id is None:
        escritorios = client.escritorios.listar()
        if not escritorios.get("items"):
            raise ValueError("Nenhum escritório encontrado")
        accounting_firm_id = UUID(escritorios["items"][0]["id"])
    
    return client.contatos.listar(accounting_firm_id=accounting_firm_id)


def listar_obrigacoes_cliente(
    cliente_identificador: str,
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None,
    accounting_firm_id: Optional[UUID] = None
) -> Dict[str, Any]:
    """
    Lista obrigações de um cliente específico
    
    Args:
        cliente_identificador: Nome do cliente ou UUID do cliente
        data_inicio: Data de início do período (padrão: hoje)
        data_fim: Data de fim do período (padrão: 31/12 do ano atual)
        accounting_firm_id: UUID do escritório. Se None, usa o primeiro disponível.
        
    Returns:
        Dicionário com:
        - items: Lista de obrigações filtradas
        - total_cliente: Total de obrigações do cliente
        - total_periodo: Total de obrigações no período
        - cliente_info: Informações do cliente
    """
    config = NiboConfig()
    client = NiboObrigacoesClient(config)
    
    # Obtém o ID do escritório
    if accounting_firm_id is None:
        escritorios = client.escritorios.listar()
        if not escritorios.get("items"):
            raise ValueError("Nenhum escritório encontrado")
        accounting_firm_id = UUID(escritorios["items"][0]["id"])
    
    # Verifica se o identificador é um UUID válido
    clientes_encontrados = []
    
    try:
        cliente_id = UUID(cliente_identificador)
        # Se for UUID, busca todos os clientes e filtra localmente
        # (a API pode não suportar filtro direto por ID)
        # Busca em todas as páginas se necessário
        cliente_encontrado = None
        skip = 0
        page_size = 100
        
        while cliente_encontrado is None:
            clientes = client.clientes.listar(
                accounting_firm_id=accounting_firm_id,
                odata_top=page_size,
                odata_skip=skip
            )
            
            items = clientes.get("items", [])
            if not items:
                break
            
            # Filtra localmente pelo ID
            for cliente in items:
                if str(cliente.get("id")) == str(cliente_id):
                    cliente_encontrado = cliente
                    break
            
            if cliente_encontrado:
                break
            
            skip += len(items)
            # Limita a busca a 1000 registros (10 páginas)
            if skip >= 1000:
                break
        
        if cliente_encontrado is None:
            raise ValueError(f"Cliente com ID '{cliente_identificador}' não encontrado")
        
        clientes_encontrados = [cliente_encontrado]
    except ValueError:
        # Não é um UUID válido, então busca por nome
        nome_cliente = cliente_identificador
        # Busca todos os clientes que contêm o nome
        nome_escape = nome_cliente.replace("'", "''")
        clientes = client.clientes.listar(
            accounting_firm_id=accounting_firm_id,
            odata_filter=f"contains(name, '{nome_escape}')"
        )
        
        if not clientes.get("items") or len(clientes["items"]) == 0:
            raise ValueError(f"Cliente '{nome_cliente}' não encontrado")
        
        clientes_encontrados = clientes["items"]
    
    if not clientes_encontrados:
        raise ValueError(f"Erro ao identificar o cliente: '{cliente_identificador}'")
    
    # Define as datas
    if data_inicio is None:
        data_inicio = date.today()
    if data_fim is None:
        # Padrão: final do ano atual
        ano_atual = date.today().year
        data_fim = date(ano_atual, 12, 31)
    
    # Coleta IDs de todos os clientes encontrados
    cliente_ids = [UUID(cliente.get("id")) for cliente in clientes_encontrados]
    
    # Busca obrigações usando filtro Customer/Id in ('id1', 'id2', ...)
    # Constrói o filtro com todos os IDs
    ids_str = "', '".join(str(cid) for cid in cliente_ids)
    filtro_cliente = f"Customer/Id in ('{ids_str}')"
    
    items = []
    try:
        relatorios = client.relatorios.listar_relatorios(
            accounting_firm_id=accounting_firm_id,
            odata_filter=filtro_cliente,
            odata_orderby="filedDate desc"
        )
        items = relatorios.get("items", [])
    except Exception:
        # Fallback: busca sem orderby
        try:
            relatorios = client.relatorios.listar_relatorios(
                accounting_firm_id=accounting_firm_id,
                odata_filter=filtro_cliente
            )
            items = relatorios.get("items", [])
        except Exception:
            # Fallback final: busca sem filtro e filtra localmente
            relatorios = client.relatorios.listar_relatorios(
                accounting_firm_id=accounting_firm_id
            )
            items = relatorios.get("items", [])
            
            # Filtra por clientes localmente
            items_cliente = []
            cliente_ids_str = [str(cid) for cid in cliente_ids]
            for item in items:
                customer = item.get("customer")
                if customer and isinstance(customer, dict):
                    customer_id_item = customer.get("id")
                    if customer_id_item and str(customer_id_item) in cliente_ids_str:
                        items_cliente.append(item)
            items = items_cliente
    
    # Filtra por data localmente
    items_filtrados = []
    for item in items:
        duedate_str = item.get("dueDate")
        duedate_obj = parse_date(duedate_str)
        
        if duedate_obj and data_inicio <= duedate_obj <= data_fim:
            items_filtrados.append(item)
    
    return {
        "items": items_filtrados,
        "total_cliente": len(items),
        "total_periodo": len(items_filtrados),
        "clientes_info": clientes_encontrados,  # Lista de todos os clientes encontrados
        "total_clientes": len(clientes_encontrados),
        "periodo": {
            "inicio": data_inicio,
            "fim": data_fim
        }
    }


def exibir_obrigacoes(obrigacoes: Dict[str, Any], detalhado: bool = True):
    """
    Exibe obrigações em formato tabular
    
    Args:
        obrigacoes: Dicionário retornado por listar_obrigacoes_cliente()
        detalhado: Se True, exibe informações detalhadas
    """
    items = obrigacoes.get("items", [])
    total = obrigacoes.get("total_periodo", 0)
    clientes_info = obrigacoes.get("clientes_info", [])
    total_clientes = obrigacoes.get("total_clientes", len(clientes_info) if clientes_info else 0)
    periodo = obrigacoes.get("periodo", {})
    
    print("=" * 100)
    if total_clientes == 1:
        print(f"OBRIGAÇÕES - {clientes_info[0].get('name', 'N/A')}")
    else:
        nomes_clientes = [c.get('name', 'N/A') for c in clientes_info]
        print(f"OBRIGAÇÕES - {total_clientes} cliente(s): {', '.join(nomes_clientes[:3])}")
        if total_clientes > 3:
            print(f"  ... e mais {total_clientes - 3} cliente(s)")
    if periodo:
        print(f"Período: {format_date(periodo.get('inicio'))} até {format_date(periodo.get('fim'))}")
    print(f"Total no período: {total} obrigação(ões)")
    print("=" * 100)
    print()
    
    if total > 0:
        print(f"{'Data Venc.':<12} {'Competência':<12} {'Data Protocolo':<20} {'Status':<20} {'Tipo':<15} {'Valor':<15}")
        print("-" * 100)
        
        for item in items:
            # Data de vencimento
            duedate = item.get("dueDate")
            duedate_obj = parse_date(duedate) if duedate else None
            duedate_str = format_date(duedate_obj) if duedate_obj else (duedate if duedate else "N/A")
            
            # Competência
            accrual = item.get("accrual")
            if accrual:
                if isinstance(accrual, (int, float)):
                    accrual_str = str(int(accrual))
                else:
                    accrual_str = str(accrual)
            else:
                accrual_str = "N/A"
            
            # Data do protocolo
            fileddate = item.get("filedDate")
            fileddate_obj = parse_date(fileddate) if fileddate else None
            fileddate_str = format_date(fileddate_obj) if fileddate_obj else (fileddate if fileddate else "N/A")
            
            # Status
            status_type = item.get("status") or item.get("statusType")
            status_map = {
                1: "Excluído",
                2: "Cancelado",
                3: "Não Recebido",
                4: "Recebido",
                5: "Baixa Justificada",
                6: "Pago"
            }
            status = status_map.get(status_type, f"Status {status_type}" if status_type is not None else "N/A")
            
            # Tipo de obrigação
            obligation = item.get("obligation", {})
            obligation_type = obligation.get("type") if isinstance(obligation, dict) else None
            tipo_map = {
                1: "Pagamento",
                2: "Cadastral",
                3: "Declaração",
                4: "Diversos"
            }
            tipo = tipo_map.get(obligation_type, f"Tipo {obligation_type}" if obligation_type is not None else "N/A")
            
            # Valor
            value = item.get("value")
            if value is not None:
                try:
                    value_str = f"R$ {float(value):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                except:
                    value_str = str(value) if value else "N/A"
            else:
                value_str = "N/A"
            
            print(f"{duedate_str:<12} {accrual_str:<12} {fileddate_str:<20} {status:<20} {tipo:<15} {value_str:<15}")
            
            if detalhado:
                # Informações detalhadas
                number = item.get("number", "N/A")
                obligation_name = obligation.get("name", "N/A") if isinstance(obligation, dict) else "N/A"
                department = item.get("department", {})
                department_name = department.get("name", "N/A") if isinstance(department, dict) else "N/A"
                
                destination_type = item.get("destinationType")
                destination_map = {
                    1: "Arquivos Online",
                    2: "Controle Interno",
                    3: "Cliente",
                    4: "Contador",
                    5: "Baixa Justificada"
                }
                destination = destination_map.get(destination_type, f"Destino {destination_type}" if destination_type is not None else "N/A")
                
                print(f"   Número: {number} | Obrigação: {obligation_name} | Departamento: {department_name}")
                print(f"   Destino: {destination}")
        
        print("-" * 100)
        print(f"Total: {total} obrigação(ões)")
    else:
        print("Nenhuma obrigação encontrada no período especificado.")


def listar_departamentos(accounting_firm_id: Optional[UUID] = None) -> Dict[str, Any]:
    """
    Lista departamentos de um escritório contábil
    
    Args:
        accounting_firm_id: UUID do escritório. Se None, usa o primeiro disponível.
        
    Returns:
        Dicionário com 'items' (lista de departamentos) e 'metadata'
    """
    config = NiboConfig()
    client = NiboObrigacoesClient(config)
    
    if accounting_firm_id is None:
        escritorios = client.escritorios.listar()
        if not escritorios.get("items"):
            raise ValueError("Nenhum escritório encontrado")
        accounting_firm_id = UUID(escritorios["items"][0]["id"])
    
    return client.departamentos.listar(accounting_firm_id=accounting_firm_id)


def listar_tarefas(
    accounting_firm_id: Optional[UUID] = None,
    usuario_id: Optional[UUID] = None,
    usuario_nome: Optional[str] = None,
    incluir_completas: bool = False
) -> Dict[str, Any]:
    """
    Lista tarefas de um escritório contábil
    
    Args:
        accounting_firm_id: UUID do escritório. Se None, usa o primeiro disponível.
        usuario_id: UUID do usuário para filtrar tarefas (opcional)
        usuario_nome: Nome do usuário para filtrar tarefas (opcional, busca parcial)
        incluir_completas: Se True, inclui tarefas completas (status 3). Padrão: False (exclui completas)
        
    Returns:
        Dicionário com 'items' (lista de tarefas) e 'metadata'
    """
    config = NiboConfig()
    client = NiboObrigacoesClient(config)
    
    if accounting_firm_id is None:
        escritorios = client.escritorios.listar()
        if not escritorios.get("items"):
            raise ValueError("Nenhum escritório encontrado")
        accounting_firm_id = UUID(escritorios["items"][0]["id"])
    
    # Constrói filtro OData
    filtros = []
    
    # Por padrão, exclui tarefas completas (status != 3) se não incluir_completas
    if not incluir_completas:
        filtros.append("status ne 3")
    
    if usuario_id:
        # Filtra por ID do usuário
        filtros.append(f"inChargeUser/Id eq '{usuario_id}'")
    elif usuario_nome:
        # Filtra por nome do usuário (busca parcial)
        nome_escape = usuario_nome.replace("'", "''")
        filtros.append(f"contains(inChargeUser/Name, '{nome_escape}')")
    
    # Combina todos os filtros com 'and'
    odata_filter = " and ".join(filtros) if filtros else None
    
    return client.tarefas.listar(
        accounting_firm_id=accounting_firm_id,
        odata_filter=odata_filter
    )


def criar_tarefa(
    nome: str,
    accounting_firm_id: Optional[UUID] = None,
    template_id: Optional[str] = None,
    deadline: Optional[str] = None,
    usuario_responsavel_id: Optional[str] = None,
    cliente_id: Optional[str] = None,
    descricao: Optional[str] = None,
    departamento_id: Optional[str] = None,
    arquivo_ids: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Cria uma nova tarefa
    
    Args:
        nome: Nome da tarefa (obrigatório se não usar template)
        accounting_firm_id: UUID do escritório. Se None, usa o primeiro disponível.
        template_id: ID do template para criar tarefa a partir de template (opcional)
        deadline: Data e hora limite (formato: YYYY-MM-DDTHH:MM:SS ou YYYY-MM-DD)
        usuario_responsavel_id: ID do usuário responsável (opcional)
        cliente_id: ID do cliente associado (opcional)
        descricao: Descrição da tarefa (opcional)
        departamento_id: ID do departamento relacionado (opcional)
        arquivo_ids: Lista de IDs de arquivos anexados (opcional)
        
    Returns:
        Resposta da API (status 202 Accepted)
    """
    config = NiboConfig()
    client = NiboObrigacoesClient(config)
    
    if accounting_firm_id is None:
        escritorios = client.escritorios.listar()
        if not escritorios.get("items"):
            raise ValueError("Nenhum escritório encontrado")
        accounting_firm_id = UUID(escritorios["items"][0]["id"])
    
    return client.tarefas.criar(
        accounting_firm_id=accounting_firm_id,
        name=nome,
        task_template_id=template_id,
        deadline=deadline,
        in_charge_user_id=usuario_responsavel_id,
        customer_id=cliente_id,
        description=descricao,
        department_id=departamento_id,
        file_ids=arquivo_ids
    )


def listar_cnaes(accounting_firm_id: Optional[UUID] = None) -> Dict[str, Any]:
    """
    Lista CNAEs de um escritório contábil
    
    Args:
        accounting_firm_id: UUID do escritório. Se None, usa o primeiro disponível.
        
    Returns:
        Dicionário com 'items' (lista de CNAEs) e 'metadata'
    """
    config = NiboConfig()
    client = NiboObrigacoesClient(config)
    
    if accounting_firm_id is None:
        escritorios = client.escritorios.listar()
        if not escritorios.get("items"):
            raise ValueError("Nenhum escritório encontrado")
        accounting_firm_id = UUID(escritorios["items"][0]["id"])
    
    return client.cnaes.listar(accounting_firm_id=accounting_firm_id)


def listar_grupos_clientes(accounting_firm_id: Optional[UUID] = None) -> Dict[str, Any]:
    """
    Lista grupos de clientes (tags) de um escritório contábil
    
    Args:
        accounting_firm_id: UUID do escritório. Se None, usa o primeiro disponível.
        
    Returns:
        Dicionário com 'items' (lista de grupos) e 'metadata'
    """
    config = NiboConfig()
    client = NiboObrigacoesClient(config)
    
    if accounting_firm_id is None:
        escritorios = client.escritorios.listar()
        if not escritorios.get("items"):
            raise ValueError("Nenhum escritório encontrado")
        accounting_firm_id = UUID(escritorios["items"][0]["id"])
    
    return client.grupos_clientes.listar(accounting_firm_id=accounting_firm_id)


def listar_usuarios(accounting_firm_id: Optional[UUID] = None, nome_usuario: Optional[str] = None) -> Dict[str, Any]:
    """
    Lista membros da equipe de um escritório contábil
    
    Args:
        accounting_firm_id: UUID do escritório. Se None, usa o primeiro disponível.
        nome_usuario: Nome do usuário para filtrar (opcional, busca parcial)
        
    Returns:
        Dicionário com 'items' (lista de usuários) e 'metadata'
    """
    config = NiboConfig()
    client = NiboObrigacoesClient(config)
    
    if accounting_firm_id is None:
        escritorios = client.escritorios.listar()
        if not escritorios.get("items"):
            raise ValueError("Nenhum escritório encontrado")
        accounting_firm_id = UUID(escritorios["items"][0]["id"])
    
    # Constrói filtro OData se necessário
    odata_filter = None
    if nome_usuario:
        # Busca parcial por nome
        nome_escape = nome_usuario.replace("'", "''")
        odata_filter = f"contains(name, '{nome_escape}')"
    
    return client.usuarios.listar_membros_equipe(
        accounting_firm_id=accounting_firm_id,
        odata_filter=odata_filter
    )


def exibir_resultado_json(resultado: Dict[str, Any]):
    """Exibe resultado em formato JSON"""
    print(json.dumps(resultado, indent=2, ensure_ascii=False, default=str))


def exibir_lista_simples(resultado: Dict[str, Any], campo_nome: str = "name"):
    """Exibe lista simples de itens"""
    items = resultado.get("items", [])
    if not items:
        print("Nenhum item encontrado.")
        return
    
    print(f"Total: {len(items)} item(ns)")
    print("-" * 80)
    for i, item in enumerate(items, 1):
        nome = item.get(campo_nome, item.get("id", "N/A"))
        item_id = item.get("id", "N/A")
        print(f"{i}. {nome} (ID: {item_id})")


def main_cli():
    """Interface de linha de comando principal"""
    parser = argparse.ArgumentParser(
        description="CLI para interagir com a API Nibo Obrigações",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:

  # Listar escritórios
  python obrigacoes.py escritorios

  # Listar clientes
  python obrigacoes.py clientes
  python obrigacoes.py clientes --nome "BV - BRAGGION & VILACA LTDA"

  # Listar obrigações de um cliente
  python obrigacoes.py obrigacoes --cliente "BV - BRAGGION & VILACA LTDA"
  python obrigacoes.py obrigacoes --cliente "BV" --inicio 01/01/2025 --fim 31/12/2025

  # Listar contatos
  python obrigacoes.py contatos

  # Listar departamentos
  python obrigacoes.py departamentos

  # Listar tarefas
  python obrigacoes.py tarefas
  python obrigacoes.py tarefas --usuario-nome "João"
  python obrigacoes.py tarefas --usuario-id "uuid-do-usuario"

  # Listar CNAEs
  python obrigacoes.py cnaes

  # Listar grupos de clientes
  python obrigacoes.py grupos-clientes

  # Listar usuários
  python obrigacoes.py usuarios

  # Usar formato JSON
  python obrigacoes.py clientes --json
        """
    )
    
    subparsers = parser.add_subparsers(dest="comando", help="Comandos disponíveis")
    
    # Argumentos compartilhados (para usar com parents)
    shared_args = argparse.ArgumentParser(add_help=False)
    shared_args.add_argument(
        "--escritorio-id",
        type=str,
        help="UUID do escritório contábil (opcional, usa o primeiro disponível se não fornecido)"
    )
    shared_args.add_argument(
        "--json",
        action="store_true",
        help="Exibe resultado em formato JSON"
    )
    
    # Comando: escritorios
    parser_escritorios = subparsers.add_parser("escritorios", help="Lista todos os escritórios contábeis", parents=[shared_args])
    
    # Comando: clientes
    parser_clientes = subparsers.add_parser("clientes", help="Lista clientes de um escritório", parents=[shared_args])
    parser_clientes.add_argument("--nome", type=str, help="Nome do cliente para filtrar")
    
    # Comando: obrigacoes
    parser_obrigacoes = subparsers.add_parser("obrigacoes", help="Lista obrigações de um cliente", parents=[shared_args])
    parser_obrigacoes.add_argument("--cliente", type=str, required=True, help="Nome do cliente ou UUID do cliente")
    parser_obrigacoes.add_argument("--inicio", type=str, help="Data de início (DD/MM/YYYY, padrão: hoje)")
    parser_obrigacoes.add_argument("--fim", type=str, help="Data de fim (DD/MM/YYYY, padrão: 31/12 do ano atual)")
    parser_obrigacoes.add_argument("--simples", action="store_true", help="Exibe apenas informações básicas")
    
    # Comando: contatos
    parser_contatos = subparsers.add_parser("contatos", help="Lista contatos de um escritório", parents=[shared_args])
    
    # Comando: departamentos
    parser_departamentos = subparsers.add_parser("departamentos", help="Lista departamentos de um escritório", parents=[shared_args])
    
    # Comando: tarefas
    parser_tarefas = subparsers.add_parser("tarefas", help="Lista tarefas de um escritório", parents=[shared_args])
    parser_tarefas.add_argument("--usuario-id", type=str, help="UUID do usuário para filtrar tarefas")
    parser_tarefas.add_argument("--usuario-nome", type=str, help="Nome do usuário para filtrar tarefas (busca parcial)")
    parser_tarefas.add_argument("--incluir-completas", action="store_true", help="Inclui tarefas completas (padrão: exclui tarefas completas)")
    
    # Comando: criar-tarefa
    parser_criar_tarefa = subparsers.add_parser("criar-tarefa", help="Cria uma nova tarefa", parents=[shared_args])
    parser_criar_tarefa.add_argument("--nome", type=str, required=True, help="Nome da tarefa (obrigatório se não usar template)")
    parser_criar_tarefa.add_argument("--template-id", type=str, help="ID do template para criar tarefa a partir de template")
    parser_criar_tarefa.add_argument("--deadline", type=str, help="Data e hora limite (formato: YYYY-MM-DDTHH:MM:SS ou YYYY-MM-DD)")
    parser_criar_tarefa.add_argument("--usuario-responsavel-id", type=str, help="ID do usuário responsável")
    parser_criar_tarefa.add_argument("--cliente-id", type=str, help="ID do cliente associado")
    parser_criar_tarefa.add_argument("--descricao", type=str, help="Descrição da tarefa")
    parser_criar_tarefa.add_argument("--departamento-id", type=str, help="ID do departamento relacionado")
    parser_criar_tarefa.add_argument("--arquivo-ids", type=str, nargs="+", help="IDs de arquivos anexados (separados por espaço)")
    
    # Comando: cnaes
    parser_cnaes = subparsers.add_parser("cnaes", help="Lista CNAEs de um escritório", parents=[shared_args])
    
    # Comando: grupos-clientes
    parser_grupos = subparsers.add_parser("grupos-clientes", help="Lista grupos de clientes (tags)", parents=[shared_args])
    
    # Comando: usuarios
    parser_usuarios = subparsers.add_parser("usuarios", help="Lista membros da equipe", parents=[shared_args])
    parser_usuarios.add_argument("--nome", type=str, help="Nome do usuário para filtrar (busca parcial)")
    
    args = parser.parse_args()
    
    if not args.comando:
        parser.print_help()
        return
    
    # Converte accounting_firm_id se fornecido
    accounting_firm_id = None
    if args.escritorio_id:
        try:
            accounting_firm_id = UUID(args.escritorio_id)
        except ValueError:
            print(f"ERRO: ID do escritório inválido: {args.escritorio_id}")
            return
    
    try:
        if args.comando == "escritorios":
            resultado = listar_escritorios()
            if args.json:
                exibir_resultado_json(resultado)
            else:
                exibir_lista_simples(resultado, campo_nome="name")
        
        elif args.comando == "clientes":
            resultado = listar_clientes(
                accounting_firm_id=accounting_firm_id,
                nome_cliente=args.nome
            )
            if args.json:
                exibir_resultado_json(resultado)
            else:
                exibir_lista_simples(resultado, campo_nome="name")
        
        elif args.comando == "obrigacoes":
            # Parse das datas
            data_inicio = None
            data_fim = None
            
            if args.inicio:
                data_inicio = parse_date(args.inicio)
                if not data_inicio:
                    print(f"ERRO: Data de início inválida: {args.inicio}. Use formato DD/MM/YYYY")
                    return
            
            if args.fim:
                data_fim = parse_date(args.fim)
                if not data_fim:
                    print(f"ERRO: Data de fim inválida: {args.fim}. Use formato DD/MM/YYYY")
                    return
            
            obrigacoes = listar_obrigacoes_cliente(
                cliente_identificador=args.cliente,
                data_inicio=data_inicio,
                data_fim=data_fim,
                accounting_firm_id=accounting_firm_id
            )
            
            if args.json:
                exibir_resultado_json(obrigacoes)
            else:
                exibir_obrigacoes(obrigacoes, detalhado=not args.simples)
        
        elif args.comando == "contatos":
            resultado = listar_contatos(accounting_firm_id=accounting_firm_id)
            if args.json:
                exibir_resultado_json(resultado)
            else:
                exibir_lista_simples(resultado, campo_nome="name")
        
        elif args.comando == "departamentos":
            resultado = listar_departamentos(accounting_firm_id=accounting_firm_id)
            if args.json:
                exibir_resultado_json(resultado)
            else:
                exibir_lista_simples(resultado, campo_nome="name")
        
        elif args.comando == "tarefas":
            # Converte usuario_id para UUID se fornecido
            usuario_id = None
            if args.usuario_id:
                try:
                    usuario_id = UUID(args.usuario_id)
                except ValueError:
                    print(f"ERRO: ID do usuário inválido: {args.usuario_id}")
                    return 1
            
            resultado = listar_tarefas(
                accounting_firm_id=accounting_firm_id,
                usuario_id=usuario_id,
                usuario_nome=args.usuario_nome,
                incluir_completas=args.incluir_completas
            )
            if args.json:
                exibir_resultado_json(resultado)
            else:
                items = resultado.get("items", [])
                if not items:
                    print("Nenhuma tarefa encontrada.")
                else:
                    # Mostra filtro aplicado se houver
                    filtro_info = ""
                    if args.usuario_id or args.usuario_nome:
                        if args.usuario_id:
                            filtro_info = f" (filtrado por usuário ID: {args.usuario_id})"
                        elif args.usuario_nome:
                            filtro_info = f" (filtrado por usuário: {args.usuario_nome})"
                    
                    print(f"Total: {len(items)} tarefa(s){filtro_info}")
                    print("-" * 100)
                    print(f"{'Nome':<40} {'Status':<15} {'Frequência':<20} {'Usuário':<25} {'ID':<40}")
                    print("-" * 100)
                    for i, item in enumerate(items, 1):
                        nome = item.get("name", "N/A")
                        status_val = item.get("status", 0)
                        status = interpretar_status(status_val)
                        frequency_val = item.get("frequency", 0)
                        frequency = interpretar_frequency(frequency_val)
                        item_id = item.get("id", "N/A")
                        
                        # Obtém nome do usuário responsável
                        in_charge_user = item.get("inChargeUser", {})
                        usuario_nome = in_charge_user.get("name", "N/A") if isinstance(in_charge_user, dict) else "N/A"
                        
                        # Trunca nome se muito longo
                        nome_display = nome[:37] + "..." if len(nome) > 40 else nome
                        usuario_display = usuario_nome[:22] + "..." if len(usuario_nome) > 25 else usuario_nome
                        print(f"{nome_display:<40} {status:<15} {frequency:<20} {usuario_display:<25} {item_id:<40}")
                        
                        # Mostra informações adicionais se disponíveis
                        if frequency_val > 0:  # Se tem recorrência
                            schedule = item.get("frequencySchedule", 0)
                            if schedule > 0:
                                dias = interpretar_frequency_schedule(schedule)
                                print(f"   Dias: {', '.join(dias)}")
                        
                        skip_holiday = item.get("skipHoliday", 0)
                        if skip_holiday > 0:
                            regra = interpretar_skip_holiday(skip_holiday)
                            print(f"   Regra feriados: {regra}")
                    
                    print("-" * 100)
        
        elif args.comando == "criar-tarefa":
            try:
                resultado = criar_tarefa(
                    nome=args.nome,
                    accounting_firm_id=accounting_firm_id,
                    template_id=args.template_id,
                    deadline=args.deadline,
                    usuario_responsavel_id=args.usuario_responsavel_id,
                    cliente_id=args.cliente_id,
                    descricao=args.descricao,
                    departamento_id=args.departamento_id,
                    arquivo_ids=args.arquivo_ids
                )
                
                if args.json:
                    exibir_resultado_json(resultado)
                else:
                    # A API retorna 202 Accepted (criação assíncrona)
                    # O resultado pode estar vazio ou conter informações básicas
                    print("Tarefa criada com sucesso!")
                    print("Status: 202 Accepted (criação assíncrona)")
                    if resultado:
                        print(f"Resposta: {resultado}")
            except Exception as e:
                print(f"ERRO ao criar tarefa: {e}")
                if args.json:
                    import traceback
                    traceback.print_exc()
                return 1
        
        elif args.comando == "cnaes":
            resultado = listar_cnaes(accounting_firm_id=accounting_firm_id)
            if args.json:
                exibir_resultado_json(resultado)
            else:
                items = resultado.get("items", [])
                if not items:
                    print("Nenhum CNAE encontrado.")
                else:
                    print(f"Total: {len(items)} CNAE(s)")
                    print("-" * 80)
                    for i, item in enumerate(items, 1):
                        codigo = item.get("code", "N/A")
                        descricao = item.get("description", "N/A")
                        print(f"{i}. {codigo} - {descricao[:50]}...")
        
        elif args.comando == "grupos-clientes":
            resultado = listar_grupos_clientes(accounting_firm_id=accounting_firm_id)
            if args.json:
                exibir_resultado_json(resultado)
            else:
                exibir_lista_simples(resultado, campo_nome="name")
        
        elif args.comando == "usuarios":
            resultado = listar_usuarios(accounting_firm_id=accounting_firm_id, nome_usuario=args.nome)
            if args.json:
                exibir_resultado_json(resultado)
            else:
                items = resultado.get("items", [])
                if not items:
                    print("Nenhum usuário encontrado.")
                else:
                    print(f"Total: {len(items)} usuário(s)")
                    print("-" * 80)
                    for i, item in enumerate(items, 1):
                        nome = item.get("name", "N/A")
                        email = item.get("email", "N/A")
                        item_id = item.get("id", "N/A")
                        print(f"{i}. {nome} ({email}) - ID: {item_id}")
    
    except Exception as e:
        print(f"ERRO: {e}")
        if args.json:
            import traceback
            traceback.print_exc()
        return 1
    
    return 0


# Exemplo de uso como script
if __name__ == "__main__":
    exit(main_cli())

