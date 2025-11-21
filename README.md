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
  "api_token": "SEU_TOKEN_EMPRESA_AQUI",
  "obrigacoes_api_token": "SEU_TOKEN_OBRIGACOES_AQUI",
  "empresa_base_url": "https://api.nibo.com.br/empresas/v1",
  "obrigacoes_base_url": "https://api.nibo.com.br/accountant/api/v1",
  "obrigacoes_user_id": "SEU_USER_ID_AQUI"
}
```

**Nota**: O `obrigacoes_user_id` é opcional e só é necessário se o token de Obrigações não estiver vinculado a um usuário específico. Se `obrigacoes_api_token` não for fornecido, o sistema usará `api_token` como fallback.

### Variáveis de Ambiente (Alternativa)

Você também pode usar variáveis de ambiente:

- `NIBO_API_TOKEN`: Token de API do Nibo Empresa
- `NIBO_OBRIGACOES_API_TOKEN`: Token de API do Nibo Obrigações (opcional, usa `NIBO_API_TOKEN` como fallback)
- `NIBO_OBRIGACOES_USER_ID`: User ID para API Obrigações (opcional)
- `NIBO_EMPRESA_BASE_URL`: URL base da API Empresa (opcional, padrão: `https://api.nibo.com.br/empresas/v1`)
- `NIBO_OBRIGACOES_BASE_URL`: URL base da API Obrigações (opcional, padrão: `https://api.nibo.com.br/accountant/api/v1`)

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
from uuid import UUID

# Inicializa o cliente
config = NiboConfig()
client = NiboObrigacoesClient(config)

# Lista escritórios
escritorios = client.escritorios.listar()
accounting_firm_id = UUID(escritorios["items"][0]["id"])

# Lista contatos vinculados a um escritório
contatos = client.contatos.listar(accounting_firm_id)

# Lista clientes vinculados a um escritório
clientes = client.clientes.listar(accounting_firm_id)

# Cria um novo cliente
novo_cliente = client.clientes.criar(
    accounting_firm_id=accounting_firm_id,
    name="Cliente Teste",
    code="CLI-001",
    document_number="12345678901"
)

# Lista grupos de clientes (tags)
grupos = client.grupos_clientes.listar(accounting_firm_id)

# Lista relatórios de obrigações
relatorios = client.relatorios.listar_relatorios(accounting_firm_id)

# Lista tarefas
tarefas = client.tarefas.listar(accounting_firm_id)

# Cria uma nova tarefa
tarefa = client.tarefas.criar(
    accounting_firm_id=accounting_firm_id,
    name="Nova tarefa",
    customer_id=UUID("..."),
    task_template_id=UUID("...")
)
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
- **Contatos**: CRUD completo com departamentos (requer `accounting_firm_id`)
- **Clientes**: CRUD completo com grupos (requer `accounting_firm_id`)
- **CNAEs**: Listagem (requer `accounting_firm_id`)
- **Grupos de Clientes (Tags)**: Listagem (requer `accounting_firm_id`, endpoint: `/tags`)
- **Departamentos**: Listagem (requer `accounting_firm_id`)
- **Tarefas**: Listagem e criação (requer `accounting_firm_id`)
- **Templates de Tarefas**: Listagem (requer `accounting_firm_id`)
- **Responsabilidades**: Listagem e transferência (requer `accounting_firm_id`)
- **Relatórios**: Listagem de relatórios de obrigações (requer `accounting_firm_id`, endpoint: `/reports/obligations/complete`)

**Nota**: A maioria dos endpoints da API de Obrigações requer o `accounting_firm_id` (ID do escritório contábil) como parâmetro. Você pode obter esse ID através do endpoint de listagem de escritórios.

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
except NiboValidationError:
    print("Erro de validação - verifique os dados enviados")
except NiboRateLimitError:
    print("Limite de requisições excedido")
except NiboServerError:
    print("Erro no servidor")
```

### Códigos de Status HTTP

O cliente trata os seguintes códigos de status como sucesso:
- `200 OK`: Requisição bem-sucedida
- `201 Created`: Recurso criado com sucesso
- `202 Accepted`: Requisição aceita (alguns endpoints de criação retornam 202 com corpo vazio)

Erros comuns:
- `400 Bad Request`: `NiboValidationError` - Dados inválidos
- `401 Unauthorized`: `NiboAuthenticationError` - Token inválido ou expirado
- `404 Not Found`: `NiboNotFoundError` - Recurso não encontrado
- `429 Too Many Requests`: `NiboRateLimitError` - Limite de requisições excedido
- `5xx Server Error`: `NiboServerError` - Erro no servidor

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

## Autenticação

### Nibo Empresa
A API de Empresa usa o header `ApiToken` para autenticação.

### Nibo Obrigações
A API de Obrigações usa:
- Header `X-API-Key`: Token de API de Obrigações
- Header `X-User-Id`: User ID (opcional, necessário se o token não estiver vinculado a um usuário)

## Documentação da API

Para mais detalhes sobre os endpoints disponíveis, consulte a documentação oficial:
- [Nibo Empresa API](https://nibo.readme.io/reference/como-utilizar-a-api)
- [Nibo Obrigações API](https://nibo.readme.io/reference/como-utilizar-a-api)
- [Listar Grupos de Clientes](https://nibo.readme.io/reference/listar-grupos-de-clientes)
- [Listar Relatórios](https://nibo.readme.io/reference/listar-relatorios)

## Licença

Este projeto é fornecido como está, sem garantias.

