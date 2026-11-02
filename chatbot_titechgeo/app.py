
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)

# Em produção, informe WIX_ORIGIN com o domínio do site publicado.
allowed_origin = os.getenv("WIX_ORIGIN", "*")
CORS(app, resources={r"/chat": {"origins": allowed_origin}})

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

KNOWLEDGE = """
Você é o assistente virtual oficial da TITECHGEO.

Responda sempre no idioma escolhido pelo visitante:
- pt: português brasileiro.
- en: inglês.

Seja claro, cordial e objetivo. Use somente as informações abaixo como
fatos institucionais. Não invente preços, prazos, garantias, disponibilidade,
certificações ou serviços não listados. Quando não souber, diga que a equipe
precisa confirmar.

SOBRE A EMPRESA

A TITECHGEO reúne profissionais que atuam com análise de dados em geral
e geoespacial.

Site: https://titechgeo.wixsite.com/titechgeoficial

Contato:
titechgeo@gmail.com
ngsneto@gmail.com

SERVIÇOS PRINCIPAIS

1. Análise descritiva: identificação de tendências e padrões; pode envolver
análise quantitativa e qualitativa, histogramas e gráficos de setores.

2. Análise prescritiva: simulações e avaliação de possíveis comportamentos futuros.

3. Análise preditiva: identificação de padrões para estimar resultados,
incluindo métodos como regressão.

4. Análise diagnóstica: investigação de relações e possíveis causas de acontecimentos.

5. Análises geoespaciais e geoprocessamento: mapas de localização e mapas temáticos.
Exemplos apresentados no site: pesquisa sobre a Copa do Mundo de 2022,
cafeterias de João Pessoa e mapa mundial de gases de efeito estufa.

6. Acessibilidade web.

7. UX/UI: desenho de interfaces e layouts para websites, celulares e tablets,
como apoio ao desenvolvimento de sistemas web e mobile.

8. Formatação de trabalhos acadêmicos conforme normas ABNT.

EQUIPE

O site apresenta experiência em Sistemas para Internet, Engenharia de Software,
Qualidade e Teste de Software, análise de sistemas, acessibilidade web, UX,
análise estatística com R e Python, geoprocessamento, Gestão Ambiental,
Big Data, mapas temáticos para planejamento urbano e meio ambiente
e cadastro multifinalitário municipal.

ATENDIMENTO COMERCIAL

Se a pessoa demonstrar interesse em contratar:
- Pergunte qual serviço procura.
- Pergunte qual é o objetivo.
- Pergunte como prefere ser contatada.

Não solicite senhas, documentos sensíveis ou dados financeiros.
Não prometa orçamento imediato.

Oriente a pessoa a enviar os detalhes para:
titechgeo@gmail.com ou ngsneto@gmail.com.
"""


@app.post("/chat")
def chat():
    data = request.get_json(silent=True) or {}

    message = (data.get("message") or "").strip()

    if not message:
        return jsonify(error="Mensagem vazia"), 400

    # Idioma escolhido pelo visitante: pt ou en.
    language = (data.get("language") or "pt").lower()

    if language not in ("pt", "en"):
        language = "pt"

    if language == "en":
        language_instruction = (
            "The visitor selected English. "
            "Always respond in English."
        )
        empty_error = "Empty message"
        server_error = (
            "I had a problem consulting the artificial intelligence. "
            "Please try again or contact titechgeo@gmail.com."
        )
    else:
        language_instruction = (
            "O visitante escolheu português. "
            "Responda sempre em português brasileiro."
        )
        empty_error = "Mensagem vazia"
        server_error = (
            "Tive um problema ao consultar a inteligência artificial. "
            "Por favor, tente novamente ou escreva para "
            "titechgeo@gmail.com."
        )

    history = data.get("history") or []

    input_items = []

    for item in history[-10:]:
        role = item.get("role")
        content = item.get("content")

        if role in ("user", "assistant") and isinstance(content, str):
            input_items.append({
                "role": role,
                "content": content[:3000]
            })

    input_items.append({
        "role": "user",
        "content": message[:3000]
    })

    try:
        response = client.responses.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
            instructions=KNOWLEDGE + "\n\n" + language_instruction,
            input=input_items,
            max_output_tokens=600
        )

        return jsonify(
            reply=response.output_text,
            language=language
        )

    except Exception:
        app.logger.exception("Erro ao consultar a OpenAI")

        return jsonify(
            reply=server_error,
            language=language
        ), 502


@app.get("/")
def health():
    return "API do chatbot TITECHGEO ativa."


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000"))
    )
