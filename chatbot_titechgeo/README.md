# Chatbot inteligente TITECHGEO

Este projeto contém:
- `index.html`: widget flutuante para incorporar no site.
- `app.py`: API Python/Flask que conversa com a API da OpenAI.
- `requirements.txt`: dependências.
- `.env.example`: exemplo de configuração.

## 1. Preparar o backend

Requer Python 3.10 ou superior.

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Configure a variável `OPENAI_API_KEY` no ambiente do servidor. Nunca coloque a chave
da API no HTML, no Wix ou no JavaScript público.

PowerShell (apenas para teste local):
```powershell
$env:OPENAI_API_KEY="SUA_CHAVE"
python app.py
```

A API ficará em `http://localhost:8000`.

## 2. Ligar o widget à API

Abra `index.html` e substitua:
`https://SEU-SERVIDOR.com/chat`
pela URL HTTPS pública do backend, terminando em `/chat`.

## 3. Publicar no Wix

O backend Python precisa ficar hospedado em um serviço que execute aplicações Python
(por exemplo, Render, Railway ou outro servidor). O HTML precisa estar disponível por
HTTPS para ser incorporado como iframe, ou seu conteúdo pode ser adaptado para o recurso
de incorporação de código do Wix.

No editor Wix:
1. Adicione um elemento Incorporar código / HTML iframe.
2. Use a URL HTTPS onde o `index.html` estiver hospedado.
3. Ajuste a largura e altura do elemento conforme o layout do site.
4. Publique e teste em desktop e celular.

## 4. Segurança e produção

- Restrinja CORS ao domínio publicado do Wix em vez de permitir qualquer origem.
- Configure limites de uso, autenticação/antiabuso e monitoramento no backend.
- Configure a chave da OpenAI como variável secreta no provedor de hospedagem.
- Informe aos visitantes que estão conversando com IA e publique aviso de privacidade
  adequado caso colete dados pessoais.
- A API da OpenAI pode gerar custos conforme o uso e o modelo escolhido. O backend usa a Responses API.

O chatbot responde com base nas informações institucionais cadastradas no `KNOWLEDGE`
em `app.py`. Revise e atualize esse texto quando os serviços ou contatos mudarem.
