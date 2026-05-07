"""
Comandos CLI para agendamentos
"""
import argparse
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime

from nibo_api.settings import NiboSettings
from nibo_api.empresa.client import NiboEmpresaClient
from ..utils import exibir_resultado_json, exibir_agendamentos


def listar_agendamentos_receber(
    tipo: str = "abertos",
    nome_cliente: Optional[str] = None,
    data_inicio: Optional[str] = None,
    data_fim: Optional[str] = None,
    organizacao_id: Optional[str] = None,
    organizacao_codigo: Optional[str] = None
) -> Dict[str, Any]:
    """
    Lista agendamentos de recebimento
    
    Args:
        tipo: Tipo de agendamentos ('abertos', 'vencidos', 'todos')
        nome_cliente: Nome do cliente para filtrar (opcional)
        organizacao_id: ID da organização (ex: "org_123")
        organizacao_codigo: Código simplificado da organização (ex: "empresa_principal")
        
    Returns:
        Dicionário com 'items' (lista de agendamentos) e 'count'
    """
    config = NiboSettings()
    client = NiboEmpresaClient(
        config,
        organizacao_id=organizacao_id,
        organizacao_codigo=organizacao_codigo
    )
    
    odata_filter_nome = None
    if nome_cliente:
        nome_escape = nome_cliente.replace("'", "''")
        odata_filter_nome = f"contains(stakeholder/name, '{nome_escape}')"

    odata_filter_periodo = None
    if data_inicio or data_fim:
        if not data_inicio or not data_fim:
            raise ValueError("Para filtrar período, informe --data-inicio e --data-fim.")
        odata_filter_periodo = _montar_filtro_periodo_campo(data_inicio, data_fim, "dueDate")

    odata_filter = _combinar_filtros_odata(odata_filter_nome, odata_filter_periodo)
    
    if tipo == "abertos":
        return client.agendamentos_receber.listar_abertos(odata_filter=odata_filter)
    elif tipo == "vencidos":
        return client.agendamentos_receber.listar_vencidos(odata_filter=odata_filter)
    else:
        return client.agendamentos_receber.listar_todos(odata_filter=odata_filter)


def listar_agendamentos_pagar(
    tipo: str = "abertos",
    nome_fornecedor: Optional[str] = None,
    data_inicio: Optional[str] = None,
    data_fim: Optional[str] = None,
    organizacao_id: Optional[str] = None,
    organizacao_codigo: Optional[str] = None
) -> Dict[str, Any]:
    """
    Lista agendamentos de pagamento
    
    Args:
        tipo: Tipo de agendamentos ('abertos', 'vencidos', 'todos')
        nome_fornecedor: Nome do fornecedor para filtrar (opcional)
        organizacao_id: ID da organização (ex: "org_123")
        organizacao_codigo: Código simplificado da organização (ex: "empresa_principal")
        
    Returns:
        Dicionário com 'items' (lista de agendamentos) e 'count'
    """
    config = NiboSettings()
    client = NiboEmpresaClient(
        config,
        organizacao_id=organizacao_id,
        organizacao_codigo=organizacao_codigo
    )
    
    odata_filter_nome = None
    if nome_fornecedor:
        nome_escape = nome_fornecedor.replace("'", "''")
        odata_filter_nome = f"contains(stakeholder/name, '{nome_escape}')"

    odata_filter_periodo = None
    if data_inicio or data_fim:
        if not data_inicio or not data_fim:
            raise ValueError("Para filtrar período, informe --data-inicio e --data-fim.")
        odata_filter_periodo = _montar_filtro_periodo_campo(data_inicio, data_fim, "dueDate")

    odata_filter = _combinar_filtros_odata(odata_filter_nome, odata_filter_periodo)
    
    if tipo == "abertos":
        return client.agendamentos_pagar.listar_abertos(odata_filter=odata_filter)
    elif tipo == "vencidos":
        return client.agendamentos_pagar.listar_vencidos(odata_filter=odata_filter)
    else:
        # Para 'todos', usa abertos (a API não tem listar_todos para pagamentos)
        return client.agendamentos_pagar.listar_abertos(odata_filter=odata_filter)


def criar_agendamento_receber(
    cliente_id: str,
    categoria_id: str,
    valor: float,
    data_agendamento: str,
    data_vencimento: str,
    descricao: str,
    referencia: Optional[str] = None,
    organizacao_id: Optional[str] = None,
    organizacao_codigo: Optional[str] = None
) -> Dict[str, Any]:
    """
    Cria um agendamento de recebimento
    
    Args:
        cliente_id: UUID do cliente
        categoria_id: UUID da categoria
        valor: Valor do agendamento
        data_agendamento: Data de agendamento (DD/MM/YYYY)
        data_vencimento: Data de vencimento (DD/MM/YYYY)
        descricao: Descrição do agendamento
        referencia: Referência do agendamento (opcional)
        organizacao_id: ID da organização (ex: "org_123")
        organizacao_codigo: Código simplificado da organização (ex: "empresa_principal")
        
    Returns:
        Dados do agendamento criado
    """
    config = NiboSettings()
    client = NiboEmpresaClient(
        config,
        organizacao_id=organizacao_id,
        organizacao_codigo=organizacao_codigo
    )
    
    categories = [{
        "categoryId": categoria_id,
        "value": valor,
        "description": descricao
    }]
    
    return client.agendamentos_receber.agendar(
        categories=categories,
        stakeholder_id=UUID(cliente_id),
        schedule_date=data_agendamento,
        due_date=data_vencimento,
        description=descricao,
        reference=referencia
    )


def criar_agendamento_pagar(
    fornecedor_id: str,
    categoria_id: str,
    valor: float,
    data_agendamento: str,
    data_vencimento: str,
    descricao: str,
    referencia: Optional[str] = None,
    organizacao_id: Optional[str] = None,
    organizacao_codigo: Optional[str] = None
) -> Dict[str, Any]:
    """
    Cria um agendamento de pagamento
    
    Args:
        fornecedor_id: UUID do fornecedor
        categoria_id: UUID da categoria
        valor: Valor do agendamento
        data_agendamento: Data de agendamento (DD/MM/YYYY)
        data_vencimento: Data de vencimento (DD/MM/YYYY)
        descricao: Descrição do agendamento
        referencia: Referência do agendamento (opcional)
        organizacao_id: ID da organização (ex: "org_123")
        organizacao_codigo: Código simplificado da organização (ex: "empresa_principal")
        
    Returns:
        Dados do agendamento criado
    """
    config = NiboSettings()
    client = NiboEmpresaClient(
        config,
        organizacao_id=organizacao_id,
        organizacao_codigo=organizacao_codigo
    )
    
    categories = [{
        "categoryId": categoria_id,
        "value": valor,
        "description": descricao
    }]
    
    return client.agendamentos_pagar.agendar(
        categories=categories,
        stakeholder_id=UUID(fornecedor_id),
        schedule_date=data_agendamento,
        due_date=data_vencimento,
        description=descricao,
        reference=referencia
    )


def _parse_data_periodo(data_str: str):
    """Converte data de entrada (DD/MM/YYYY ou YYYY-MM-DD) para datetime."""
    if not data_str:
        return None

    data_limpa = data_str.strip()
    for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(data_limpa, fmt)
        except ValueError:
            continue
    return None


def _montar_filtro_periodo(data_inicio: str, data_fim: str) -> str:
    """Monta filtro OData para campo date no intervalo informado."""
    inicio = _parse_data_periodo(data_inicio)
    fim = _parse_data_periodo(data_fim)
    if not inicio or not fim:
        raise ValueError("Datas inválidas. Use DD/MM/YYYY ou YYYY-MM-DD.")
    if inicio > fim:
        raise ValueError("Data inicial não pode ser maior que data final.")

    inicio_iso = inicio.strftime("%Y-%m-%dT00:00:00Z")
    fim_iso = fim.strftime("%Y-%m-%dT23:59:59Z")
    return f"date ge {inicio_iso} and date le {fim_iso}"


def _montar_filtro_periodo_campo(data_inicio: str, data_fim: str, campo_data: str) -> str:
    """Monta filtro OData para um campo de data específico."""
    inicio = _parse_data_periodo(data_inicio)
    fim = _parse_data_periodo(data_fim)
    if not inicio or not fim:
        raise ValueError("Datas inválidas. Use DD/MM/YYYY ou YYYY-MM-DD.")
    if inicio > fim:
        raise ValueError("Data inicial não pode ser maior que data final.")

    inicio_iso = inicio.strftime("%Y-%m-%dT00:00:00Z")
    fim_iso = fim.strftime("%Y-%m-%dT23:59:59Z")
    return f"{campo_data} ge {inicio_iso} and {campo_data} le {fim_iso}"


def _combinar_filtros_odata(*filtros: Optional[str]) -> Optional[str]:
    """Combina filtros OData com AND, ignorando vazios."""
    validos = [f"({f})" for f in filtros if f]
    if not validos:
        return None
    return " and ".join(validos)


def listar_pagamentos_recebimentos_periodo(
    data_inicio: str,
    data_fim: str,
    organizacao_id: Optional[str] = None,
    organizacao_codigo: Optional[str] = None,
    odata_top: Optional[int] = None,
    odata_skip: Optional[int] = None,
    odata_orderby: str = "date desc"
) -> Dict[str, Any]:
    """
    Lista pagamentos e recebimentos realizados em um período.
    """
    config = NiboSettings()
    client = NiboEmpresaClient(
        config,
        organizacao_id=organizacao_id,
        organizacao_codigo=organizacao_codigo
    )

    odata_filter = _montar_filtro_periodo(data_inicio, data_fim)
    pagamentos = client.pagamentos.listar(
        odata_filter=odata_filter,
        odata_orderby=odata_orderby,
        odata_top=odata_top,
        odata_skip=odata_skip
    )
    recebimentos = client.recebimentos.listar(
        odata_filter=odata_filter,
        odata_orderby=odata_orderby,
        odata_top=odata_top,
        odata_skip=odata_skip
    )

    itens_pagamentos = pagamentos.get("items", [])
    itens_recebimentos = recebimentos.get("items", [])

    total_pagamentos = len(itens_pagamentos)
    total_recebimentos = len(itens_recebimentos)
    valor_total_pagamentos = sum(float(item.get("value", 0) or 0) for item in itens_pagamentos)
    valor_total_recebimentos = sum(float(item.get("value", 0) or 0) for item in itens_recebimentos)

    return {
        "periodo": {"dataInicio": data_inicio, "dataFim": data_fim},
        "filtro": odata_filter,
        "pagamentos": pagamentos,
        "recebimentos": recebimentos,
        "resumo": {
            "totalPagamentos": total_pagamentos,
            "totalRecebimentos": total_recebimentos,
            "valorTotalPagamentos": valor_total_pagamentos,
            "valorTotalRecebimentos": valor_total_recebimentos,
            "saldoLiquido": valor_total_recebimentos - valor_total_pagamentos
        }
    }


def listar_pagamentos_periodo(
    data_inicio: str,
    data_fim: str,
    organizacao_id: Optional[str] = None,
    organizacao_codigo: Optional[str] = None,
    odata_top: Optional[int] = None,
    odata_skip: Optional[int] = None,
    odata_orderby: str = "date desc"
) -> Dict[str, Any]:
    """Lista apenas pagamentos realizados em um período."""
    config = NiboSettings()
    client = NiboEmpresaClient(
        config,
        organizacao_id=organizacao_id,
        organizacao_codigo=organizacao_codigo
    )

    odata_filter = _montar_filtro_periodo(data_inicio, data_fim)
    pagamentos = client.pagamentos.listar(
        odata_filter=odata_filter,
        odata_orderby=odata_orderby,
        odata_top=odata_top,
        odata_skip=odata_skip
    )
    itens_pagamentos = pagamentos.get("items", [])
    valor_total_pagamentos = sum(float(item.get("value", 0) or 0) for item in itens_pagamentos)

    return {
        "periodo": {"dataInicio": data_inicio, "dataFim": data_fim},
        "filtro": odata_filter,
        "pagamentos": pagamentos,
        "resumo": {
            "totalPagamentos": len(itens_pagamentos),
            "valorTotalPagamentos": valor_total_pagamentos
        }
    }


def listar_recebimentos_periodo(
    data_inicio: str,
    data_fim: str,
    organizacao_id: Optional[str] = None,
    organizacao_codigo: Optional[str] = None,
    odata_top: Optional[int] = None,
    odata_skip: Optional[int] = None,
    odata_orderby: str = "date desc"
) -> Dict[str, Any]:
    """Lista apenas recebimentos realizados em um período."""
    config = NiboSettings()
    client = NiboEmpresaClient(
        config,
        organizacao_id=organizacao_id,
        organizacao_codigo=organizacao_codigo
    )

    odata_filter = _montar_filtro_periodo(data_inicio, data_fim)
    recebimentos = client.recebimentos.listar(
        odata_filter=odata_filter,
        odata_orderby=odata_orderby,
        odata_top=odata_top,
        odata_skip=odata_skip
    )
    itens_recebimentos = recebimentos.get("items", [])
    valor_total_recebimentos = sum(float(item.get("value", 0) or 0) for item in itens_recebimentos)

    return {
        "periodo": {"dataInicio": data_inicio, "dataFim": data_fim},
        "filtro": odata_filter,
        "recebimentos": recebimentos,
        "resumo": {
            "totalRecebimentos": len(itens_recebimentos),
            "valorTotalRecebimentos": valor_total_recebimentos
        }
    }


def listar_agendamentos_pagar_receber_periodo(
    data_inicio: str,
    data_fim: str,
    tipo: str = "abertos",
    organizacao_id: Optional[str] = None,
    organizacao_codigo: Optional[str] = None
) -> Dict[str, Any]:
    """Lista agendamentos a pagar e a receber juntos no período (dueDate)."""
    config = NiboSettings()
    client = NiboEmpresaClient(
        config,
        organizacao_id=organizacao_id,
        organizacao_codigo=organizacao_codigo
    )

    odata_filter = _montar_filtro_periodo_campo(data_inicio, data_fim, "dueDate")
    if tipo == "abertos":
        pagar = client.agendamentos_pagar.listar_abertos(odata_filter=odata_filter)
        receber = client.agendamentos_receber.listar_abertos(odata_filter=odata_filter)
    elif tipo == "vencidos":
        pagar = client.agendamentos_pagar.listar_vencidos(odata_filter=odata_filter)
        receber = client.agendamentos_receber.listar_vencidos(odata_filter=odata_filter)
    else:
        pagar = client.agendamentos_pagar.listar_abertos(odata_filter=odata_filter)
        receber = client.agendamentos_receber.listar_todos(odata_filter=odata_filter)

    return {
        "periodo": {"dataInicio": data_inicio, "dataFim": data_fim},
        "filtro": odata_filter,
        "tipo": tipo,
        "agendamentosPagar": pagar,
        "agendamentosReceber": receber,
        "resumo": {
            "totalPagar": len(pagar.get("items", [])),
            "totalReceber": len(receber.get("items", []))
        }
    }


def handle_agendamentos_receber(args):
    """Handler para comando agendamentos-receber"""
    organizacao_id = None
    organizacao_codigo = None
    if hasattr(args, 'organizacao') and args.organizacao:
        if args.organizacao.startswith("org_") or "-" in args.organizacao:
            organizacao_id = args.organizacao
        else:
            organizacao_codigo = args.organizacao
    
    if not organizacao_id and not organizacao_codigo:
        print("ERRO: É necessário fornecer --org (ou --organizacao) para este comando.")
        return 1
    
    try:
        resultado = listar_agendamentos_receber(
            tipo=getattr(args, 'tipo', 'abertos'),
            nome_cliente=getattr(args, 'cliente', None),
            data_inicio=getattr(args, 'data_inicio', None),
            data_fim=getattr(args, 'data_fim', None),
            organizacao_id=organizacao_id,
            organizacao_codigo=organizacao_codigo
        )
    except Exception as e:
        print(f"ERRO: {e}")
        return 1
    
    if args.json:
        exibir_resultado_json(resultado)
    else:
        exibir_agendamentos(resultado, tipo="receber")
    
    return 0


def handle_agendamentos_pagar(args):
    """Handler para comando agendamentos-pagar"""
    organizacao_id = None
    organizacao_codigo = None
    if hasattr(args, 'organizacao') and args.organizacao:
        if args.organizacao.startswith("org_") or "-" in args.organizacao:
            organizacao_id = args.organizacao
        else:
            organizacao_codigo = args.organizacao
    
    if not organizacao_id and not organizacao_codigo:
        print("ERRO: É necessário fornecer --org (ou --organizacao) para este comando.")
        return 1
    
    try:
        resultado = listar_agendamentos_pagar(
            tipo=getattr(args, 'tipo', 'abertos'),
            nome_fornecedor=getattr(args, 'fornecedor', None),
            data_inicio=getattr(args, 'data_inicio', None),
            data_fim=getattr(args, 'data_fim', None),
            organizacao_id=organizacao_id,
            organizacao_codigo=organizacao_codigo
        )
    except Exception as e:
        print(f"ERRO: {e}")
        return 1
    
    if args.json:
        exibir_resultado_json(resultado)
    else:
        exibir_agendamentos(resultado, tipo="pagar")
    
    return 0


def handle_criar_agendamento_receber(args):
    """Handler para comando criar-agendamento-receber"""
    organizacao_id = None
    organizacao_codigo = None
    if hasattr(args, 'organizacao') and args.organizacao:
        if args.organizacao.startswith("org_") or "-" in args.organizacao:
            organizacao_id = args.organizacao
        else:
            organizacao_codigo = args.organizacao
    
    if not organizacao_id and not organizacao_codigo:
        print("ERRO: É necessário fornecer --org (ou --organizacao) para este comando.")
        return 1
    
    try:
        resultado = criar_agendamento_receber(
            cliente_id=args.cliente,
            categoria_id=args.categoria,
            valor=args.valor,
            data_agendamento=args.data_agendamento,
            data_vencimento=args.data_vencimento,
            descricao=args.descricao,
            referencia=getattr(args, 'referencia', None),
            organizacao_id=organizacao_id,
            organizacao_codigo=organizacao_codigo
        )
        
        if args.json:
            exibir_resultado_json(resultado)
        else:
            print("Agendamento de recebimento criado com sucesso!")
            agendamento_id = resultado.get("id", "N/A")
            print(f"ID: {agendamento_id}")
    except Exception as e:
        print(f"ERRO ao criar agendamento: {e}")
        if args.json:
            import traceback
            traceback.print_exc()
        return 1
    
    return 0


def handle_criar_agendamento_pagar(args):
    """Handler para comando criar-agendamento-pagar"""
    organizacao_id = None
    organizacao_codigo = None
    if hasattr(args, 'organizacao') and args.organizacao:
        if args.organizacao.startswith("org_") or "-" in args.organizacao:
            organizacao_id = args.organizacao
        else:
            organizacao_codigo = args.organizacao
    
    if not organizacao_id and not organizacao_codigo:
        print("ERRO: É necessário fornecer --org (ou --organizacao) para este comando.")
        return 1
    
    try:
        resultado = criar_agendamento_pagar(
            fornecedor_id=args.fornecedor,
            categoria_id=args.categoria,
            valor=args.valor,
            data_agendamento=args.data_agendamento,
            data_vencimento=args.data_vencimento,
            descricao=args.descricao,
            referencia=getattr(args, 'referencia', None),
            organizacao_id=organizacao_id,
            organizacao_codigo=organizacao_codigo
        )
        
        if args.json:
            exibir_resultado_json(resultado)
        else:
            print("Agendamento de pagamento criado com sucesso!")
            agendamento_id = resultado.get("id", "N/A")
            print(f"ID: {agendamento_id}")
    except Exception as e:
        print(f"ERRO ao criar agendamento: {e}")
        if args.json:
            import traceback
            traceback.print_exc()
        return 1
    
    return 0


def handle_pagamentos_recebimentos_periodo(args):
    """Handler para comando pagamentos-recebimentos-periodo."""
    organizacao_id = None
    organizacao_codigo = None
    if hasattr(args, "organizacao") and args.organizacao:
        if args.organizacao.startswith("org_") or "-" in args.organizacao:
            organizacao_id = args.organizacao
        else:
            organizacao_codigo = args.organizacao

    if not organizacao_id and not organizacao_codigo:
        print("ERRO: É necessário fornecer --org (ou --organizacao) para este comando.")
        return 1

    try:
        resultado = listar_pagamentos_recebimentos_periodo(
            data_inicio=args.data_inicio,
            data_fim=args.data_fim,
            organizacao_id=organizacao_id,
            organizacao_codigo=organizacao_codigo,
            odata_top=getattr(args, "top", None),
            odata_skip=getattr(args, "skip", None),
            odata_orderby=getattr(args, "orderby", "date desc")
        )
    except Exception as e:
        print(f"ERRO: {e}")
        return 1

    if args.json:
        exibir_resultado_json(resultado)
        return 0

    resumo = resultado.get("resumo", {})
    print("=" * 100)
    print("PAGAMENTOS E RECEBIMENTOS REALIZADOS")
    print(f"Período: {args.data_inicio} até {args.data_fim}")
    print("=" * 100)
    print(f"Pagamentos:   {resumo.get('totalPagamentos', 0)} item(ns) | Valor total: R$ {resumo.get('valorTotalPagamentos', 0):.2f}")
    print(f"Recebimentos: {resumo.get('totalRecebimentos', 0)} item(ns) | Valor total: R$ {resumo.get('valorTotalRecebimentos', 0):.2f}")
    print(f"Saldo líquido: R$ {resumo.get('saldoLiquido', 0):.2f}")
    print("-" * 100)

    pagamentos = resultado.get("pagamentos", {})
    recebimentos = resultado.get("recebimentos", {})
    print(f"Itens retornados de pagamentos: {len(pagamentos.get('items', []))}")
    print(f"Itens retornados de recebimentos: {len(recebimentos.get('items', []))}")
    return 0


def handle_pagamentos_periodo(args):
    """Handler para comando pagamentos-periodo."""
    organizacao_id = None
    organizacao_codigo = None
    if hasattr(args, "organizacao") and args.organizacao:
        if args.organizacao.startswith("org_") or "-" in args.organizacao:
            organizacao_id = args.organizacao
        else:
            organizacao_codigo = args.organizacao

    if not organizacao_id and not organizacao_codigo:
        print("ERRO: É necessário fornecer --org (ou --organizacao) para este comando.")
        return 1

    try:
        resultado = listar_pagamentos_periodo(
            data_inicio=args.data_inicio,
            data_fim=args.data_fim,
            organizacao_id=organizacao_id,
            organizacao_codigo=organizacao_codigo,
            odata_top=getattr(args, "top", None),
            odata_skip=getattr(args, "skip", None),
            odata_orderby=getattr(args, "orderby", "date desc")
        )
    except Exception as e:
        print(f"ERRO: {e}")
        return 1

    if args.json:
        exibir_resultado_json(resultado)
        return 0

    resumo = resultado.get("resumo", {})
    print("=" * 100)
    print("PAGAMENTOS REALIZADOS")
    print(f"Período: {args.data_inicio} até {args.data_fim}")
    print("=" * 100)
    print(f"Pagamentos: {resumo.get('totalPagamentos', 0)} item(ns)")
    print(f"Valor total: R$ {resumo.get('valorTotalPagamentos', 0):.2f}")
    print("-" * 100)
    print(f"Itens retornados: {len(resultado.get('pagamentos', {}).get('items', []))}")
    return 0


def handle_recebimentos_periodo(args):
    """Handler para comando recebimentos-periodo."""
    organizacao_id = None
    organizacao_codigo = None
    if hasattr(args, "organizacao") and args.organizacao:
        if args.organizacao.startswith("org_") or "-" in args.organizacao:
            organizacao_id = args.organizacao
        else:
            organizacao_codigo = args.organizacao

    if not organizacao_id and not organizacao_codigo:
        print("ERRO: É necessário fornecer --org (ou --organizacao) para este comando.")
        return 1

    try:
        resultado = listar_recebimentos_periodo(
            data_inicio=args.data_inicio,
            data_fim=args.data_fim,
            organizacao_id=organizacao_id,
            organizacao_codigo=organizacao_codigo,
            odata_top=getattr(args, "top", None),
            odata_skip=getattr(args, "skip", None),
            odata_orderby=getattr(args, "orderby", "date desc")
        )
    except Exception as e:
        print(f"ERRO: {e}")
        return 1

    if args.json:
        exibir_resultado_json(resultado)
        return 0

    resumo = resultado.get("resumo", {})
    print("=" * 100)
    print("RECEBIMENTOS REALIZADOS")
    print(f"Período: {args.data_inicio} até {args.data_fim}")
    print("=" * 100)
    print(f"Recebimentos: {resumo.get('totalRecebimentos', 0)} item(ns)")
    print(f"Valor total: R$ {resumo.get('valorTotalRecebimentos', 0):.2f}")
    print("-" * 100)
    print(f"Itens retornados: {len(resultado.get('recebimentos', {}).get('items', []))}")
    return 0


def handle_agendamentos_pagar_receber_periodo(args):
    """Handler para comando agendamentos-pagar-receber-periodo."""
    organizacao_id = None
    organizacao_codigo = None
    if hasattr(args, "organizacao") and args.organizacao:
        if args.organizacao.startswith("org_") or "-" in args.organizacao:
            organizacao_id = args.organizacao
        else:
            organizacao_codigo = args.organizacao

    if not organizacao_id and not organizacao_codigo:
        print("ERRO: É necessário fornecer --org (ou --organizacao) para este comando.")
        return 1

    try:
        resultado = listar_agendamentos_pagar_receber_periodo(
            data_inicio=args.data_inicio,
            data_fim=args.data_fim,
            tipo=getattr(args, "tipo", "abertos"),
            organizacao_id=organizacao_id,
            organizacao_codigo=organizacao_codigo
        )
    except Exception as e:
        print(f"ERRO: {e}")
        return 1

    if args.json:
        exibir_resultado_json(resultado)
        return 0

    resumo = resultado.get("resumo", {})
    print("=" * 100)
    print("AGENDAMENTOS A PAGAR E A RECEBER")
    print(f"Período (dueDate): {args.data_inicio} até {args.data_fim}")
    print(f"Tipo: {getattr(args, 'tipo', 'abertos')}")
    print("=" * 100)
    print(f"A pagar:   {resumo.get('totalPagar', 0)} item(ns)")
    print(f"A receber: {resumo.get('totalReceber', 0)} item(ns)")
    return 0


def add_agendamentos_parser(subparsers):
    """Adiciona parsers para comandos de agendamentos"""
    # Comando: agendamentos-receber
    parser_agendamentos_receber = subparsers.add_parser(
        "agendamentos-receber",
        aliases=["receber"],
        help="Lista agendamentos de recebimento"
    )
    parser_agendamentos_receber.add_argument(
        "--tipo",
        type=str,
        choices=["abertos", "vencidos", "todos"],
        default="abertos",
        help="Tipo de agendamentos (padrão: abertos)"
    )
    parser_agendamentos_receber.add_argument("--cliente", type=str, help="Nome do cliente para filtrar")
    parser_agendamentos_receber.add_argument("--data-inicio", type=str, help="Data inicial do período (dueDate)")
    parser_agendamentos_receber.add_argument("--data-fim", type=str, help="Data final do período (dueDate)")
    parser_agendamentos_receber.add_argument(
        "--json",
        action="store_true",
        help="Exibe resultado em formato JSON"
    )
    parser_agendamentos_receber.add_argument(
        "--org",
        "--organizacao",
        type=str,
        dest="organizacao",
        help="ID ou código da organização (ex: 'org_123' ou 'empresa_principal')"
    )
    parser_agendamentos_receber.set_defaults(func=handle_agendamentos_receber)
    
    # Comando: agendamentos-pagar
    parser_agendamentos_pagar = subparsers.add_parser(
        "agendamentos-pagar",
        aliases=["pagar"],
        help="Lista agendamentos de pagamento"
    )
    parser_agendamentos_pagar.add_argument(
        "--tipo",
        type=str,
        choices=["abertos", "vencidos", "todos"],
        default="abertos",
        help="Tipo de agendamentos (padrão: abertos)"
    )
    parser_agendamentos_pagar.add_argument("--fornecedor", type=str, help="Nome do fornecedor para filtrar")
    parser_agendamentos_pagar.add_argument("--data-inicio", type=str, help="Data inicial do período (dueDate)")
    parser_agendamentos_pagar.add_argument("--data-fim", type=str, help="Data final do período (dueDate)")
    parser_agendamentos_pagar.add_argument(
        "--json",
        action="store_true",
        help="Exibe resultado em formato JSON"
    )
    parser_agendamentos_pagar.add_argument(
        "--org",
        "--organizacao",
        type=str,
        dest="organizacao",
        help="ID ou código da organização (ex: 'org_123' ou 'empresa_principal')"
    )
    parser_agendamentos_pagar.set_defaults(func=handle_agendamentos_pagar)
    
    # Comando: criar-agendamento-receber
    parser_criar_agendamento_receber = subparsers.add_parser(
        "criar-agendamento-receber",
        aliases=["novo-receber"],
        help="Cria um agendamento de recebimento"
    )
    parser_criar_agendamento_receber.add_argument("--cliente", "-cli", type=str, required=True, help="UUID do cliente")
    parser_criar_agendamento_receber.add_argument("--categoria", "-cat", type=str, required=True, help="UUID da categoria")
    parser_criar_agendamento_receber.add_argument("--valor", type=float, required=True, help="Valor do agendamento")
    parser_criar_agendamento_receber.add_argument("--data-agendamento", "-da", type=str, required=True, help="Data de agendamento (DD/MM/YYYY)")
    parser_criar_agendamento_receber.add_argument("--data-vencimento", "-dv", type=str, required=True, help="Data de vencimento (DD/MM/YYYY)")
    parser_criar_agendamento_receber.add_argument("--descricao", type=str, required=True, help="Descrição do agendamento")
    parser_criar_agendamento_receber.add_argument("--referencia", type=str, help="Referência do agendamento (opcional)")
    parser_criar_agendamento_receber.add_argument(
        "--json",
        action="store_true",
        help="Exibe resultado em formato JSON"
    )
    parser_criar_agendamento_receber.add_argument(
        "--org",
        "--organizacao",
        type=str,
        dest="organizacao",
        help="ID ou código da organização (ex: 'org_123' ou 'empresa_principal')"
    )
    parser_criar_agendamento_receber.set_defaults(func=handle_criar_agendamento_receber)
    
    # Comando: criar-agendamento-pagar
    parser_criar_agendamento_pagar = subparsers.add_parser(
        "criar-agendamento-pagar",
        help="Cria um agendamento de pagamento"
    )
    parser_criar_agendamento_pagar.add_argument("--fornecedor", "-for", type=str, required=True, help="UUID do fornecedor")
    parser_criar_agendamento_pagar.add_argument("--categoria", "-cat", type=str, required=True, help="UUID da categoria")
    parser_criar_agendamento_pagar.add_argument("--valor", type=float, required=True, help="Valor do agendamento")
    parser_criar_agendamento_pagar.add_argument("--data-agendamento", "-da", type=str, required=True, help="Data de agendamento (DD/MM/YYYY)")
    parser_criar_agendamento_pagar.add_argument("--data-vencimento", "-dv", type=str, required=True, help="Data de vencimento (DD/MM/YYYY)")
    parser_criar_agendamento_pagar.add_argument("--descricao", type=str, required=True, help="Descrição do agendamento")
    parser_criar_agendamento_pagar.add_argument("--referencia", type=str, help="Referência do agendamento (opcional)")
    parser_criar_agendamento_pagar.add_argument(
        "--json",
        action="store_true",
        help="Exibe resultado em formato JSON"
    )
    parser_criar_agendamento_pagar.add_argument(
        "--org",
        "--organizacao",
        type=str,
        dest="organizacao",
        help="ID ou código da organização (ex: 'org_123' ou 'empresa_principal')"
    )
    parser_criar_agendamento_pagar.set_defaults(func=handle_criar_agendamento_pagar)

    # Comando: pagamentos-recebimentos-periodo
    parser_pag_rec_periodo = subparsers.add_parser(
        "pagamentos-recebimentos-periodo",
        aliases=["pag-rec-periodo"],
        help="Lista pagamentos e recebimentos realizados em um período"
    )
    parser_pag_rec_periodo.add_argument("--data-inicio", type=str, required=True, help="Data inicial (DD/MM/YYYY ou YYYY-MM-DD)")
    parser_pag_rec_periodo.add_argument("--data-fim", type=str, required=True, help="Data final (DD/MM/YYYY ou YYYY-MM-DD)")
    parser_pag_rec_periodo.add_argument("--top", type=int, help="Limite de registros ($top)")
    parser_pag_rec_periodo.add_argument("--skip", type=int, help="Registros a pular ($skip)")
    parser_pag_rec_periodo.add_argument("--orderby", type=str, default="date desc", help="Ordenação OData (padrão: date desc)")
    parser_pag_rec_periodo.add_argument(
        "--json",
        action="store_true",
        help="Exibe resultado em formato JSON"
    )
    parser_pag_rec_periodo.add_argument(
        "--org",
        "--organizacao",
        type=str,
        dest="organizacao",
        help="ID ou código da organização (ex: 'org_123' ou 'empresa_principal')"
    )
    parser_pag_rec_periodo.set_defaults(func=handle_pagamentos_recebimentos_periodo)

    # Comando: pagamentos-periodo
    parser_pag_periodo = subparsers.add_parser(
        "pagamentos-periodo",
        aliases=["pag-periodo"],
        help="Lista pagamentos realizados em um período"
    )
    parser_pag_periodo.add_argument("--data-inicio", type=str, required=True, help="Data inicial (DD/MM/YYYY ou YYYY-MM-DD)")
    parser_pag_periodo.add_argument("--data-fim", type=str, required=True, help="Data final (DD/MM/YYYY ou YYYY-MM-DD)")
    parser_pag_periodo.add_argument("--top", type=int, help="Limite de registros ($top)")
    parser_pag_periodo.add_argument("--skip", type=int, help="Registros a pular ($skip)")
    parser_pag_periodo.add_argument("--orderby", type=str, default="date desc", help="Ordenação OData (padrão: date desc)")
    parser_pag_periodo.add_argument(
        "--json",
        action="store_true",
        help="Exibe resultado em formato JSON"
    )
    parser_pag_periodo.add_argument(
        "--org",
        "--organizacao",
        type=str,
        dest="organizacao",
        help="ID ou código da organização (ex: 'org_123' ou 'empresa_principal')"
    )
    parser_pag_periodo.set_defaults(func=handle_pagamentos_periodo)

    # Comando: recebimentos-periodo
    parser_rec_periodo = subparsers.add_parser(
        "recebimentos-periodo",
        aliases=["rec-periodo"],
        help="Lista recebimentos realizados em um período"
    )
    parser_rec_periodo.add_argument("--data-inicio", type=str, required=True, help="Data inicial (DD/MM/YYYY ou YYYY-MM-DD)")
    parser_rec_periodo.add_argument("--data-fim", type=str, required=True, help="Data final (DD/MM/YYYY ou YYYY-MM-DD)")
    parser_rec_periodo.add_argument("--top", type=int, help="Limite de registros ($top)")
    parser_rec_periodo.add_argument("--skip", type=int, help="Registros a pular ($skip)")
    parser_rec_periodo.add_argument("--orderby", type=str, default="date desc", help="Ordenação OData (padrão: date desc)")
    parser_rec_periodo.add_argument(
        "--json",
        action="store_true",
        help="Exibe resultado em formato JSON"
    )
    parser_rec_periodo.add_argument(
        "--org",
        "--organizacao",
        type=str,
        dest="organizacao",
        help="ID ou código da organização (ex: 'org_123' ou 'empresa_principal')"
    )
    parser_rec_periodo.set_defaults(func=handle_recebimentos_periodo)

    # Comando: agendamentos-pagar-receber-periodo
    parser_agr_periodo = subparsers.add_parser(
        "agendamentos-pagar-receber-periodo",
        aliases=["agr-periodo"],
        help="Lista agendamentos a pagar e a receber juntos por período"
    )
    parser_agr_periodo.add_argument("--data-inicio", type=str, required=True, help="Data inicial (DD/MM/YYYY ou YYYY-MM-DD)")
    parser_agr_periodo.add_argument("--data-fim", type=str, required=True, help="Data final (DD/MM/YYYY ou YYYY-MM-DD)")
    parser_agr_periodo.add_argument(
        "--tipo",
        type=str,
        choices=["abertos", "vencidos", "todos"],
        default="abertos",
        help="Tipo de agendamentos (padrão: abertos)"
    )
    parser_agr_periodo.add_argument(
        "--json",
        action="store_true",
        help="Exibe resultado em formato JSON"
    )
    parser_agr_periodo.add_argument(
        "--org",
        "--organizacao",
        type=str,
        dest="organizacao",
        help="ID ou código da organização (ex: 'org_123' ou 'empresa_principal')"
    )
    parser_agr_periodo.set_defaults(func=handle_agendamentos_pagar_receber_periodo)


