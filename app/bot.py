import base64
from io import BytesIO
import threading
import uuid
import os

from matplotlib import pyplot as plt
import numpy as np
import google.generativeai as genai
import json
import time
from datetime import datetime

class FinanBot:
    def __init__(self):
        self.configure()
        self.model = self.setup_model()
        self.historico = []
        self.sessao_id = str(uuid.uuid4())
        self.carregar_historico()
        self.modulos_aprendizado = self.carregar_modulos()
        self.metas = {}
        self.lembretes = {}
        
    
    def configure(self):
        api_key = os.getenv("GEMINI_API_KEY") or " Coloque a sua chave api aqui"
        genai.configure(api_key=api_key)
    
    def setup_model(self):
        generation_config = {
            "temperature": 0.7,
            "top_p": 1,
            "top_k": 32,
            "max_output_tokens": 4096, 
        }

        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
        ]
        
        return genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            generation_config=generation_config,
            safety_settings=safety_settings
        )
    
    def carregar_modulos(self):
        return {
            "iniciante": [
                {"titulo": "Orçamento Básico", "conteudo": "Aprenda a controlar seus gastos e receitas..."},
                {"titulo": "Dívidas: Primeiros Passos", "conteudo": "Como entender e começar a pagar suas dívidas..."}
            ],
            "intermediario": [
                {"titulo": "Investimentos Iniciais", "conteudo": "Introdução aos tipos básicos de investimentos..."},
                {"titulo": "Planejamento de Metas", "conteudo": "Como estabelecer e alcançar metas financeiras..."}
            ],
            "avancado": [
                {"titulo": "Estratégias de Investimento", "conteudo": "Diversificação e estratégias avançadas..."},
                {"titulo": "Planejamento Patrimonial", "conteudo": "Como proteger e crescer seu patrimônio..."}
            ]
        }
    
    def carregar_historico(self):
        try:
            with open(f'data/historico_{self.sessao_id}.json', 'r') as f:
                self.historico = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.historico = []
    
    def salvar_historico(self):
        import os
        os.makedirs('data', exist_ok=True)  # Garante que a pasta existe
        with open(f'data/historico_{self.sessao_id}.json', 'w') as f:
            json.dump(self.historico, f)
    
    def adicionar_meta(self, meta, valor, prazo):
        meta_id = str(uuid.uuid4())
        self.metas[meta_id] = {
            "meta": meta,
            "valor": float(valor),
            "prazo": prazo,
            "progresso": 0.0,
            "criado_em": datetime.now().isoformat()
        }
        self.salvar_metas()
        return meta_id
    
    def atualizar_meta(self, meta_id, progresso):
        if meta_id in self.metas:
            self.metas[meta_id]["progresso"] = float(progresso)
            self.salvar_metas()
            return True
        return False
    
    def salvar_metas(self):
        with open(f'data/metas_{self.sessao_id}.json', 'w') as f:
            json.dump(self.metas, f)
    
    def carregar_metas(self):
        try:
            with open(f'data/metas_{self.sessao_id}.json', 'r') as f:
                self.metas = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.metas = {}
    
    def adicionar_lembrete(self, titulo, mensagem, data_hora):
        lembrete_id = str(uuid.uuid4())
        self.lembretes[lembrete_id] = {
            "titulo": titulo,
            "mensagem": mensagem,
            "data_hora": data_hora,
            "disparado": False
        }
        self.salvar_lembretes()
        self.agendar_lembrete(lembrete_id)
        return lembrete_id
    
    def agendar_lembrete(self, lembrete_id):
        def disparar_lembrete():
            lembrete = self.lembretes.get(lembrete_id)
            if lembrete and not lembrete["disparado"]:
                data_alvo = datetime.fromisoformat(lembrete["data_hora"])
                agora = datetime.now()
                if data_alvo > agora:
                    time.sleep((data_alvo - agora).total_seconds())
                
                if lembrete_id in self.lembretes and not self.lembretes[lembrete_id]["disparado"]:
                    self.lembretes[lembrete_id]["disparado"] = True
                    self.salvar_lembretes()
                    print(f"\nLEMBRETE: {lembrete['titulo']} - {lembrete['mensagem']}\n")
        
        thread = threading.Thread(target=disparar_lembrete)
        thread.daemon = True
        thread.start()
    
    def salvar_lembretes(self):
        with open(f'data/lembretes_{self.sessao_id}.json', 'w') as f:
            json.dump(self.lembretes, f)
    
    def carregar_lembretes(self):
        try:
            with open(f'data/lembretes_{self.sessao_id}.json', 'r') as f:
                self.lembretes = json.load(f)
                for lembrete_id, lembrete in self.lembretes.items():
                    if not lembrete["disparado"]:
                        self.agendar_lembrete(lembrete_id)
        except (FileNotFoundError, json.JSONDecodeError):
            self.lembretes = {}
    
    def gerar_grafico(self, dados, tipo="bar"):
        plt.figure(figsize=(8, 4))
        
        if tipo == "bar":
            plt.bar(dados['categorias'], dados['valores'])
        elif tipo == "pie":
            plt.pie(dados['valores'], labels=dados['categorias'], autopct='%1.1f%%')
        elif tipo == "line":
            plt.plot(dados['categorias'], dados['valores'])
        
        plt.title(dados.get('titulo', 'Gráfico Financeiro'))
        plt.tight_layout()
        
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plt.close()
        
        img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return f"data:image/png;base64,{img_base64}"
    
    def gerar_resposta(self, prompt):
        contexto = f"""
        Você é o FinanBot, um assistente virtual especializado em educação financeira. 
        Data atual: {datetime.now().strftime('%d/%m/%Y %H:%M')}
        Diretrizes:
        1. Seja empático e encorajador
        2. Use linguagem simples e evite jargões complexos
        3. Forneça exemplos práticos quando possível
        4. Para cálculos, explique o raciocínio passo a passo
        5. Quando relevante, sugira módulos de aprendizado
        6. Para perguntas complexas, sugira agendar um lembrete para continuar depois
        7. Nunca recomende produtos financeiros específicos
        8.Use os padrôes de texto da linguagem natural
        9. Responda de forma clara e objetiva
        """
        conversa = [contexto] + self.historico[-6:] + [f"Usuário: {prompt}"]
        try:
            resposta = self.model.generate_content(conversa)
            texto_resposta = resposta.text if hasattr(resposta, "text") else str(resposta)
            if any(palavra in prompt.lower() for palavra in ["gráfico", "grafico", "visualizar", "tabela"]):
                try:
                    dados = {
                        'categorias': ['Alimentação', 'Moradia', 'Transporte', 'Lazer', 'Outros'],
                        'valores': np.random.randint(100, 1000, size=5).tolist(),
                        'titulo': 'Distribuição de Gastos Mensais'
                    }
                    grafico = self.gerar_grafico(dados, tipo="pie")
                    texto_resposta += f"\n\n![Gráfico de Distribuição de Gastos]({grafico})"
                except Exception as e:
                    print(f"Erro ao gerar gráfico: {e}")
            return texto_resposta
        except Exception as e:
            return f"Desculpe, ocorreu um erro: {str(e)}"
    def processar_comando(self, comando):
        partes = comando.strip().split()
        if not partes:
            return None

        if partes[0] == "/meta":
            if len(partes) >= 4:
                meta = ' '.join(partes[1:-2])
                valor = partes[-2]
                prazo = partes[-1]
                meta_id = self.adicionar_meta(meta, valor, prazo)
                return f"Meta '{meta}' adicionada com sucesso! ID: {meta_id}"
            else:
                return "Formato incorreto. Use: /meta [descrição] [valor] [prazo]"

        elif partes[0] == "/lembrete":
            if len(partes) >= 4:
                titulo = ' '.join(partes[1:-2])
                mensagem = partes[-2]
                data_hora = partes[-1]
                lembrete_id = self.adicionar_lembrete(titulo, mensagem, data_hora)
                return f"Lembrete '{titulo}' agendado para {data_hora}! ID: {lembrete_id}"
            else:
                return "Formato incorreto. Use: /lembrete [título] [mensagem] [data_hora]"

        elif partes[0] == "/modulos":
            nivel = partes[1] if len(partes) > 1 else "iniciante"
            if nivel in self.modulos_aprendizado:
                modulos = "\n".join([f"- {m['titulo']}" for m in self.modulos_aprendizado[nivel]])
                return f"Módulos disponíveis ({nivel}):\n{modulos}"
            else:
                return f"Nível inválido. Opções: iniciante, intermediario, avancado"

        elif partes[0] == "/ajuda":
            return (
                "Comandos especiais:\n"
                "/meta [descrição] [valor] [prazo] - Adiciona uma nova meta\n"
                "/lembrete [título] [mensagem] [data_hora] - Agenda um lembrete\n"
                "/modulos [nivel] - Lista módulos de aprendizado\n"
                "/ajuda - Mostra esta ajuda"
            )

        return None
