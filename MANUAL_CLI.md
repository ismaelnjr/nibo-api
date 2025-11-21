# Manual do CLI - Nibo Obrigações

Este manual descreve todos os comandos disponíveis na interface de linha de comando (CLI) do módulo `obrigacoes.py` para interagir com a API Nibo Obrigações.

## Índice

1. [Instalação e Configuração](#instalação-e-configuração)
2. [Comandos Disponíveis](#comandos-disponíveis)
   - [Escritórios](#escritórios)
   - [Clientes](#clientes)
   - [Obrigações](#obrigações)
   - [Contatos](#contatos)
   - [Departamentos](#departamentos)
   - [Tarefas](#tarefas)
   - [Criar Tarefa](#criar-tarefa)
   - [CNAEs](#cnaes)
   - [Grupos de Clientes](#grupos-de-clientes)
   - [Usuários](#usuários)
3. [Opções Globais](#opções-globais)
4. [Exemplos Práticos](#exemplos-práticos)

---

## Instalação e Configuração

### Pré-requisitos

- Python 3.7 ou superior
- Pacote `requests` instalado
- Arquivo `config.json` configurado com as credenciais da API

### Configuração

Certifique-se de que o arquivo `config.json` está configurado corretamente:

```json
{
  "api_token": "seu-token-empresa",
  "obrigacoes_api_token": "seu-token-obrigacoes",
  "obrigacoes_base_url": "https://api.nibo.com.br/accountant/api/v1",
  "obrigacoes_user_id": "seu-user-id-opcional"
}
```

Ou configure via variáveis de ambiente:
- `NIBO_OBRIGACOES_API_TOKEN`
- `NIBO_OBRIGACOES_BASE_URL`
- `NIBO_OBRIGACOES_USER_ID`

---

## Comandos Disponíveis

### Escritórios

Lista todos os escritórios contábeis disponíveis.

**Sintaxe:**
```bash
python obrigacoes.py escritorios [--json] [--escritorio-id ESCRITORIO_ID]
```

**Exemplos:**
```bash
# Listar todos os escritórios
python obrigacoes.py escritorios

# Listar em formato JSON
python obrigacoes.py escritorios --json
```

---

### Clientes

Lista clientes de um escritório contábil.

**Sintaxe:**
```bash
python obrigacoes.py clientes [--nome NOME] [--json] [--escritorio-id ESCRITORIO_ID]
```

**Parâmetros:**
- `--nome`: Nome do cliente para filtrar (busca parcial, opcional)

**Exemplos:**
```bash
# Listar todos os clientes
python obrigacoes.py clientes

# Filtrar por nome (busca parcial)
python obrigacoes.py clientes --nome "BV"

# Listar em formato JSON
python obrigacoes.py clientes --nome "BV" --json
```

**Nota:** A busca por nome é parcial, então `--nome "BV"` encontrará clientes como "BV - BRAGGION & VILACA LTDA." e "BV 3F MATERIAIS PARA CONSTRUÇÃO LTDA - ME".

---

### Obrigações

Lista obrigações de um ou mais clientes.

**Sintaxe:**
```bash
python obrigacoes.py obrigacoes --cliente CLIENTE [--inicio INICIO] [--fim FIM] [--simples] [--json] [--escritorio-id ESCRITORIO_ID]
```

**Parâmetros:**
- `--cliente` (obrigatório): Nome do cliente ou UUID do cliente
- `--inicio`: Data de início do período (formato: DD/MM/YYYY, padrão: hoje)
- `--fim`: Data de fim do período (formato: DD/MM/YYYY, padrão: 31/12 do ano atual)
- `--simples`: Exibe apenas informações básicas (sem detalhes)

**Exemplos:**
```bash
# Listar obrigações de um cliente (período padrão: hoje até 31/12 do ano atual)
python obrigacoes.py obrigacoes --cliente "BV - BRAGGION & VILACA LTDA."

# Listar obrigações por ID do cliente
python obrigacoes.py obrigacoes --cliente "24ab8c16-83d1-4bef-b4b1-f9e7c8b2e387"

# Com período customizado
python obrigacoes.py obrigacoes --cliente "BV" --inicio 01/01/2025 --fim 31/12/2025

# Exibição simples
python obrigacoes.py obrigacoes --cliente "BV" --simples

# Em formato JSON
python obrigacoes.py obrigacoes --cliente "BV" --json
```

**Comportamento:**
- Se o `--cliente` for um nome, busca todos os clientes que contêm esse nome e retorna obrigações de todos eles
- Se o `--cliente` for um UUID, busca obrigações apenas desse cliente específico
- O período padrão é de hoje até o final do ano atual

---

### Contatos

Lista contatos de um escritório contábil.

**Sintaxe:**
```bash
python obrigacoes.py contatos [--json] [--escritorio-id ESCRITORIO_ID]
```

**Exemplos:**
```bash
# Listar todos os contatos
python obrigacoes.py contatos

# Listar em formato JSON
python obrigacoes.py contatos --json
```

---

### Departamentos

Lista departamentos de um escritório contábil.

**Sintaxe:**
```bash
python obrigacoes.py departamentos [--json] [--escritorio-id ESCRITORIO_ID]
```

**Exemplos:**
```bash
# Listar todos os departamentos
python obrigacoes.py departamentos

# Listar em formato JSON
python obrigacoes.py departamentos --json
```

---

### Tarefas

Lista tarefas de um escritório contábil.

**Sintaxe:**
```bash
python obrigacoes.py tarefas [--usuario-id USUARIO_ID] [--usuario-nome USUARIO_NOME] [--incluir-completas] [--json] [--escritorio-id ESCRITORIO_ID]
```

**Parâmetros:**
- `--usuario-id`: UUID do usuário para filtrar tarefas (opcional)
- `--usuario-nome`: Nome do usuário para filtrar tarefas (busca parcial, opcional)
- `--incluir-completas`: Inclui tarefas completas (padrão: exclui tarefas com status 3 - Complete)

**Exemplos:**
```bash
# Listar tarefas não completas (padrão)
python obrigacoes.py tarefas

# Filtrar por nome do usuário
python obrigacoes.py tarefas --usuario-nome "Clayton"

# Filtrar por ID do usuário
python obrigacoes.py tarefas --usuario-id "86bc7fa4-a691-4532-8ac6-0a9238faa540"

# Incluir tarefas completas também
python obrigacoes.py tarefas --usuario-nome "Clayton" --incluir-completas

# Listar em formato JSON
python obrigacoes.py tarefas --usuario-nome "Clayton" --json
```

**Status das Tarefas:**
- **0 - Undefined**: Nenhum status definido
- **1 - Blocked**: Tarefa bloqueada
- **2 - ToDo**: Tarefa pronta para ser iniciada
- **3 - Complete**: Tarefa concluída (excluída por padrão)

**Frequências:**
- **0 - Sem recorrência**
- **1 - Recorrência diária**
- **2 - Recorrência semanal**
- **3 - Recorrência mensal**
- **4 - Recorrência anual**

---

### Criar Tarefa

Cria uma nova tarefa em um escritório contábil.

**Sintaxe:**
```bash
python obrigacoes.py criar-tarefa --nome NOME [--template-id TEMPLATE_ID] [--deadline DEADLINE] [--usuario-responsavel-id USUARIO_RESPONSAVEL_ID] [--cliente-id CLIENTE_ID] [--descricao DESCRICAO] [--departamento-id DEPARTAMENTO_ID] [--arquivo-ids ARQUIVO_IDS ...] [--json] [--escritorio-id ESCRITORIO_ID]
```

**Parâmetros:**
- `--nome` (obrigatório se não usar template): Nome da tarefa
- `--template-id`: ID do template para criar tarefa a partir de template (opcional)
- `--deadline`: Data e hora limite (formato: YYYY-MM-DDTHH:MM:SS ou YYYY-MM-DD)
- `--usuario-responsavel-id`: ID do usuário responsável (opcional)
- `--cliente-id`: ID do cliente associado (opcional)
- `--descricao`: Descrição da tarefa (opcional)
- `--departamento-id`: ID do departamento relacionado (opcional)
- `--arquivo-ids`: IDs de arquivos anexados (separados por espaço, opcional)

**Exemplos:**
```bash
# Criar tarefa simples
python obrigacoes.py criar-tarefa --nome "Nova tarefa"

# Criar tarefa com descrição
python obrigacoes.py criar-tarefa --nome "Tarefa importante" --descricao "Descrição detalhada da tarefa"

# Criar tarefa com usuário responsável e deadline
python obrigacoes.py criar-tarefa --nome "Tarefa urgente" --usuario-responsavel-id "uuid-usuario" --deadline "2025-12-31T23:59:59"

# Criar tarefa a partir de template
python obrigacoes.py criar-tarefa --template-id "uuid-template" --deadline "2025-12-31"

# Criar tarefa com cliente e departamento
python obrigacoes.py criar-tarefa --nome "Tarefa cliente" --cliente-id "uuid-cliente" --departamento-id "uuid-departamento"

# Criar tarefa com arquivos anexados
python obrigacoes.py criar-tarefa --nome "Tarefa com arquivos" --arquivo-ids "uuid-arquivo-1" "uuid-arquivo-2"

# Listar em formato JSON
python obrigacoes.py criar-tarefa --nome "Tarefa" --json
```

**Nota:** A API retorna status 202 (Accepted), indicando que a tarefa foi recebida e será criada de forma assíncrona.

---

### CNAEs

Lista CNAEs (Código Nacional de Atividades Econômicas) de um escritório contábil.

**Sintaxe:**
```bash
python obrigacoes.py cnaes [--json] [--escritorio-id ESCRITORIO_ID]
```

**Exemplos:**
```bash
# Listar todos os CNAEs
python obrigacoes.py cnaes

# Listar em formato JSON
python obrigacoes.py cnaes --json
```

---

### Grupos de Clientes

Lista grupos de clientes (tags) de um escritório contábil.

**Sintaxe:**
```bash
python obrigacoes.py grupos-clientes [--json] [--escritorio-id ESCRITORIO_ID]
```

**Exemplos:**
```bash
# Listar todos os grupos de clientes
python obrigacoes.py grupos-clientes

# Listar em formato JSON
python obrigacoes.py grupos-clientes --json
```

---

### Usuários

Lista membros da equipe de um escritório contábil.

**Sintaxe:**
```bash
python obrigacoes.py usuarios [--nome NOME] [--json] [--escritorio-id ESCRITORIO_ID]
```

**Parâmetros:**
- `--nome`: Nome do usuário para filtrar (busca parcial, opcional)

**Exemplos:**
```bash
# Listar todos os usuários
python obrigacoes.py usuarios

# Filtrar por nome (busca parcial)
python obrigacoes.py usuarios --nome "Ismael"

# Listar em formato JSON
python obrigacoes.py usuarios --nome "Ismael" --json
```

---

## Opções Globais

Todos os comandos suportam as seguintes opções globais:

### `--escritorio-id ESCRITORIO_ID`

Especifica o UUID do escritório contábil. Se não fornecido, usa o primeiro escritório disponível automaticamente.

**Exemplo:**
```bash
python obrigacoes.py clientes --escritorio-id "6ee5e102-0234-4c13-82c9-5b6c910b0a9e"
```

### `--json`

Exibe o resultado em formato JSON ao invés do formato tabular padrão.

**Exemplo:**
```bash
python obrigacoes.py clientes --json
```

---

## Exemplos Práticos

### Exemplo 1: Listar obrigações de um cliente específico

```bash
# Buscar obrigações do cliente "BV - BRAGGION & VILACA LTDA." no período atual
python obrigacoes.py obrigacoes --cliente "BV - BRAGGION & VILACA LTDA."
```

### Exemplo 2: Listar tarefas de um usuário

```bash
# Listar tarefas não completas do usuário "Clayton"
python obrigacoes.py tarefas --usuario-nome "Clayton"
```

### Exemplo 3: Criar uma nova tarefa

```bash
# Criar tarefa com descrição e deadline
python obrigacoes.py criar-tarefa --nome "Revisar documentos" --descricao "Revisar documentos do cliente" --deadline "2025-12-31"
```

### Exemplo 4: Buscar clientes e suas obrigações

```bash
# 1. Listar clientes que contêm "BV" no nome
python obrigacoes.py clientes --nome "BV"

# 2. Listar obrigações de todos os clientes "BV"
python obrigacoes.py obrigacoes --cliente "BV"
```

### Exemplo 5: Exportar dados em JSON

```bash
# Exportar lista de clientes em JSON
python obrigacoes.py clientes --json > clientes.json

# Exportar obrigações em JSON
python obrigacoes.py obrigacoes --cliente "BV" --json > obrigacoes.json
```

### Exemplo 6: Filtrar tarefas por usuário e incluir completas

```bash
# Listar todas as tarefas (incluindo completas) do usuário "Clayton"
python obrigacoes.py tarefas --usuario-nome "Clayton" --incluir-completas
```

---

## Códigos de Saída

- **0**: Sucesso
- **1**: Erro na execução

---

## Tratamento de Erros

O CLI trata automaticamente os seguintes erros:

- **Erro de autenticação (401)**: Token inválido ou expirado
- **Recurso não encontrado (404)**: Endpoint ou recurso não existe
- **Erro de validação (400)**: Dados inválidos fornecidos
- **Limite de requisições (429)**: Muitas requisições em pouco tempo
- **Erro do servidor (5xx)**: Erro interno do servidor

---

## Dicas e Boas Práticas

1. **Use `--json` para integração**: Quando precisar processar os dados programaticamente, use `--json` para obter dados estruturados.

2. **Filtros parciais**: A maioria dos filtros por nome usa busca parcial. Use termos curtos para encontrar mais resultados.

3. **Períodos de datas**: O formato de data é `DD/MM/YYYY` para obrigações. O período padrão é de hoje até o final do ano atual.

4. **IDs vs Nomes**: Você pode usar tanto UUID quanto nomes para identificar recursos. UUIDs são mais precisos, nomes são mais convenientes.

5. **Tarefas completas**: Por padrão, tarefas completas são excluídas. Use `--incluir-completas` se precisar vê-las.

---

## Suporte

Para mais informações sobre a API Nibo, consulte a documentação oficial:
- [Documentação Nibo](https://nibo.readme.io/)

Para problemas ou dúvidas sobre este CLI, verifique:
- Arquivo `README.md` do projeto
- Código-fonte em `obrigacoes.py`
- Testes em `tests/test_obrigacoes/`

