# Configuração do Crew AI para fyntool

## Visão geral
Crew AI é uma integração opcional de biblioteca Python para fyntool. Quando habilitado na instalação, o fyntool cria um arquivo `.env` onde você coloca sua chave do provedor de IA e o modelo.

## Instalação
1. Execute o instalador:
   ```bash
   fyntool install
   ```
2. Quando perguntar **Do you want to enable Crew AI integration?** selecione `Yes`.
3. Serão criados:
   - `~/.config/fyntool/config.json` com `"crew_ai_enabled": true`
   - `~/.config/fyntool/.env` com placeholders

## Configuração
Edite `~/.config/fyntool/.env`:
```
CREW_AI_API_KEY=your_api_key_here
CREW_AI_BASE_URL=https://api.crew.ai
CREW_AI_MODEL=gpt-4o
```
Você também pode alterar editor padrão e idioma em `~/.config/fyntool/config.json`.

## Uso
Verificar status:
```bash
fyntool crew status
```
Testar conexão:
```bash
fyntool crew test
```

Abrir config:
```bash
fyntool config
```

## Notas
- Crew AI é uma biblioteca Python. Instale via `uv pip install crewai`.
- A chave e o modelo são lidos de `.env` em tempo de execução.
