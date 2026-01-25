# Guia de Publicação no PyPI

Este documento descreve como publicar o pacote `nibo-api` no PyPI (Python Package Index).

## Pré-requisitos

1. **Conta no PyPI**: Crie uma conta em https://pypi.org/account/register/
2. **API Token**: Gere um token de API em https://pypi.org/manage/account/token/
3. **TestPyPI (opcional)**: Para testes, crie conta em https://test.pypi.org/

## Preparação

### 1. Atualizar a versão

Antes de publicar, atualize a versão no `pyproject.toml`:

```toml
version = "1.0.1"  # Incremente conforme necessário
```

E também em `nibo_api/__init__.py`:

```python
__version__ = "1.0.1"
```

### 2. Verificar o pacote

```bash
# Instalar ferramentas de build
pip install build twine

# Construir o pacote
python -m build

# Verificar o pacote
twine check dist/*
```

### 3. Testar no TestPyPI (recomendado)

```bash
# Upload para TestPyPI
twine upload --repository testpypi dist/*

# Testar instalação do TestPyPI
pip install --index-url https://test.pypi.org/simple/ nibo-api
```

## Publicação

### Opção 1: Publicação Manual

```bash
# Construir o pacote
python -m build

# Publicar no PyPI
twine upload dist/*
```

Você será solicitado a inserir:
- Username: `__token__`
- Password: Seu token de API do PyPI

### Opção 2: Publicação Automática via GitHub Actions

1. Configure o secret `PYPI_API_TOKEN` no GitHub:
   - Vá em Settings > Secrets and variables > Actions
   - Adicione `PYPI_API_TOKEN` com seu token do PyPI

2. Crie uma release no GitHub:
   - Vá em Releases > Create a new release
   - Crie uma tag (ex: `v1.0.0`)
   - O workflow será executado automaticamente

### Opção 3: Usando GitHub Actions com OIDC (Recomendado)

O workflow `publish.yml` já está configurado para usar OIDC (OpenID Connect), que é mais seguro:

1. Configure o PyPI para aceitar OIDC:
   - Vá em https://pypi.org/manage/account/publishing/
   - Adicione o GitHub como provedor confiável

2. Crie uma release no GitHub - o workflow será executado automaticamente

## Estrutura de Versionamento

Siga o [Semantic Versioning](https://semver.org/):
- **MAJOR**: Mudanças incompatíveis na API
- **MINOR**: Novas funcionalidades compatíveis
- **PATCH**: Correções de bugs compatíveis

Exemplos:
- `1.0.0` → `1.0.1` (patch)
- `1.0.0` → `1.1.0` (minor)
- `1.0.0` → `2.0.0` (major)

## Checklist Antes de Publicar

- [ ] Versão atualizada em `pyproject.toml` e `nibo_api/__init__.py`
- [ ] README.md está completo e atualizado
- [ ] Todos os testes passam
- [ ] `python -m build` executa sem erros
- [ ] `twine check dist/*` não mostra erros
- [ ] Testado no TestPyPI (recomendado)
- [ ] Changelog atualizado (se mantiver um)

## Após a Publicação

1. Verifique a página do pacote: https://pypi.org/project/nibo-api/
2. Teste a instalação:
   ```bash
   pip install nibo-api
   ```
3. Atualize a documentação com o link do PyPI

## Comandos Úteis

```bash
# Ver informações do pacote
python -m pip show nibo-api

# Desinstalar versão antiga
pip uninstall nibo-api

# Instalar versão específica
pip install nibo-api==1.0.0

# Atualizar para última versão
pip install --upgrade nibo-api
```
