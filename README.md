# Nibo API - Cliente Python

Cliente Python para integração com a API do Nibo, dividido em dois módulos principais:
- **Nibo Empresa**: API de gestão financeira
- **Nibo Obrigações**: API de obrigações fiscais

## Instalação

```bash
pip install -r requirements.txt
```

## Configuração

### Arquivo config.json

Crie um arquivo `config.json` na raiz do projeto:

```json
{
  "api_token": "SEU_TOKEN_AQUI",
  "empresa_base_url": "https://api.nibo.com.br/empresas/v1",
  "obrigacoes_base_url": "https://api.nibo.com.br/obrigacoes/v1"
}
```

### Variáveis de Ambiente (Alternativa)

Você também pode usar variáveis de ambiente:

- `NIBO_API_TOKEN`: Token de API do Nibo
- `NIBO_EMPRESA_BASE_URL`: URL base da API Empresa (opcional)
- `NIBO_OBRIGACOES_BASE_URL`: URL base da API Obrigações (opcional)

## Uso

### Nibo Empresa

```python
from nibo_api.config import NiboConfig
from nibo_api.empresa.client import NiboEmpresaClient

# Inicializa o cliente
config = NiboConfig()
client = NiboEmpresaClient(config)

# Lista clientes
clientes = client.clientes.listar()
print(f"Total de clientes: {clientes['count']}")

# Lista clientes com filtro OData
clientes_filtrados = client.clientes.listar(
    odata_filter="document/number eq '11497110000127'"
)

# Cria um novo cliente
novo_cliente = client.clientes.criar(
    name="NOME DO CLIENTE",
    document_type="cnpj",
    document_number="11497110000127"
)

# Lista categorias
categorias = client.categorias.listar(odata_filter="type eq 'in'")

# Lista agendamentos de recebimento em aberto
agendamentos = client.agendamentos_receber.listar_abertos(
    odata_filter="stakeholder/cpfCnpj eq '11497110000127'"
)

# Agenda um novo recebimento
agendamento = client.agendamentos_receber.agendar(
    categories=[{
        "categoryId": "03708e32-f12f-4f57-9893-11d15864c7ce",
        "value": "100.00",
        "description": "Descrição"
    }],
    stakeholder_id="48dd1c64-40bf-4590-bd94-bf1318db74e1",
    schedule_date="11/11/2024",
    due_date="11/11/2024",
    description="Descrição do agendamento",
    reference="REF-001"
)
```

### Nibo Obrigações

```python
from nibo_api.config import NiboConfig
from nibo_api.obrigacoes.client import NiboObrigacoesClient

# Inicializa o cliente
config = NiboConfig()
client = NiboObrigacoesClient(config)

# Lista escritórios
escritorios = client.escritorios.listar()

# Lista contatos
contatos = client.contatos.listar()

# Lista clientes
clientes = client.clientes.listar()

# Cria uma nova tarefa
tarefa = client.tarefas.criar(name="Nova tarefa")
```

## Estrutura do Projeto

```
nibo-api/
├── nibo_api/
│   ├── __init__.py
│   ├── config.py                    # Gerenciamento de configuração
│   ├── common/                       # Componentes compartilhados
│   │   ├── client.py                # Cliente HTTP base
│   │   ├── models.py                 # Modelos de dados
│   │   └── exceptions.py            # Exceções customizadas
│   ├── empresa/                      # Módulo Nibo Empresa
│   │   ├── client.py                # Cliente principal
│   │   ├── contatos/                 # Interfaces de contatos
│   │   │   ├── clientes.py
│   │   │   ├── fornecedores.py
│   │   │   ├── funcionarios.py
│   │   │   └── socios.py
│   │   ├── categorias.py
│   │   ├── agendamentos/             # Interfaces de agendamentos
│   │   │   ├── receber.py
│   │   │   ├── pagar.py
│   │   │   ├── recebimentos.py
│   │   │   ├── pagamentos.py
│   │   │   ├── arquivos.py
│   │   │   └── anotacoes.py
│   │   └── ...                       # Outras interfaces
│   └── obrigacoes/                   # Módulo Nibo Obrigações
│       ├── client.py                 # Cliente principal
│       ├── escritorios.py
│       ├── contatos.py
│       ├── clientes.py
│       └── ...                       # Outras interfaces
├── tests/                            # Testes
│   ├── test_empresa/
│   └── test_obrigacoes/
├── config.json                       # Arquivo de configuração
├── requirements.txt
└── README.md
```

## Interfaces Disponíveis

### Nibo Empresa

- **Contatos**: Clientes, Fornecedores, Funcionários, Sócios
- **Categorias**: Listagem, criação, hierarquia
- **Agendamentos**: Recebimentos, Pagamentos, Arquivos, Anotações
- **Centro de Custo**: CRUD completo
- **Empresas**: Listagem e usuários
- **Contas & Extratos**: Saldo, extrato, transferências
- **Conciliação**: Listagem e exclusão
- **Parcelamentos**: Consulta de agendamentos
- **Arquivos**: Upload de arquivos
- **Nota Fiscal**: Perfis, NFS-e, emissão e cancelamento
- **Relatórios**: Planejamento orçamentário
- **Cobranças**: Perfis, listagem, criação e cancelamento

### Nibo Obrigações

- **Escritórios**: Listagem
- **Usuários**: Membros da equipe
- **Arquivos**: Criação para upload
- **Conferência**: Envio para tela de conferência
- **Contatos**: CRUD completo com departamentos
- **Clientes**: CRUD completo com grupos
- **CNAEs**: Listagem
- **Grupos de Clientes**: Listagem
- **Departamentos**: Listagem
- **Tarefas**: Listagem e criação
- **Templates de Tarefas**: Listagem
- **Responsabilidades**: Listagem e transferência
- **Relatórios**: Listagem

## Suporte a OData

A API suporta filtros OData para consultas avançadas:

```python
# Filtro simples
client.clientes.listar(odata_filter="name eq 'Cliente Teste'")

# Filtro com múltiplas condições
client.agendamentos_receber.listar_abertos(
    odata_filter="year(dueDate) eq 2024 AND month(dueDate) eq 11"
)

# Paginação
client.clientes.listar(
    odata_orderby="name",
    odata_top=20,
    odata_skip=0
)
```

## Tratamento de Erros

O cliente lança exceções customizadas:

```python
from nibo_api.common.exceptions import (
    NiboAuthenticationError,
    NiboNotFoundError,
    NiboValidationError,
    NiboServerError,
    NiboRateLimitError
)

try:
    cliente = client.clientes.buscar_por_id(cliente_id)
except NiboNotFoundError:
    print("Cliente não encontrado")
except NiboAuthenticationError:
    print("Erro de autenticação")
```

## Testes

Execute os testes com:

```bash
python -m unittest discover tests
```

Ou execute testes específicos:

```bash
python -m unittest tests.test_empresa.test_clientes
python -m unittest tests.test_obrigacoes.test_escritorios
```

## Documentação da API

Para mais detalhes sobre os endpoints disponíveis, consulte a documentação oficial:
- [Nibo Empresa API](https://nibo.readme.io/reference/como-utilizar-a-api)
- [Nibo Obrigações API](https://nibo.readme.io/reference/como-utilizar-a-api)

## Licença

Este projeto é fornecido como está, sem garantias.

