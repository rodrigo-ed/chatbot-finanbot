from flask import Blueprint, render_template, request, jsonify
import numpy as np
from .bot import FinanBot

finanbot = FinanBot()
main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html', sessao_id=finanbot.sessao_id)

@main.route('/chat', methods=['POST'])
def chat():
    mensagem = request.json.get('mensagem', '').strip()
    
    if not mensagem:
        return jsonify({"resposta": "Por favor, digite uma mensagem válida."})
    
    # Processa comandos especiais
    if mensagem.startswith('/'):
        resposta = finanbot.processar_comando(mensagem) or "Comando não reconhecido. Digite /ajuda para ver os comandos disponíveis."
    else:
        # Adiciona a pergunta ao histórico
        finanbot.historico.append(f"Usuário: {mensagem}")
        
        # Obtém a resposta
        resposta = finanbot.gerar_resposta(mensagem)
        
        # Adiciona a resposta ao histórico
        finanbot.historico.append(f"FinanBot: {resposta}")
        
        # Limita o histórico
        if len(finanbot.historico) > 20:
            finanbot.historico = finanbot.historico[-20:]
        
        # Salva o histórico
        finanbot.salvar_historico()
    
    return jsonify({"resposta": resposta})

@main.route('/metas', methods=['GET', 'POST'])
def gerenciar_metas():
    if request.method == 'POST':
        data = request.json
        if data.get('acao') == 'adicionar':
            meta_id = finanbot.adicionar_meta(
                data['meta'],
                data['valor'],
                data['prazo']
            )
            return jsonify({"status": "sucesso", "meta_id": meta_id})
        elif data.get('acao') == 'atualizar':
            if finanbot.atualizar_meta(data['meta_id'], data['progresso']):
                return jsonify({"status": "sucesso"})
            return jsonify({"status": "erro", "mensagem": "Meta não encontrada"}), 404
    return jsonify(finanbot.metas)

@main.route('/modulos/<nivel>')
def obter_modulos(nivel):
    modulos = finanbot.modulos_aprendizado.get(nivel, [])
    return jsonify(modulos)

@main.route('/grafico')
def gerar_grafico():
    tipo = request.args.get('tipo', 'bar')
    dados = {
        'categorias': ['Alimentação', 'Moradia', 'Transporte', 'Lazer', 'Outros'],
        'valores': np.random.randint(100, 1000, size=5).tolist(),
        'titulo': 'Distribuição de Gastos Mensais'
    }
    img_data = finanbot.gerar_grafico(dados, tipo)
    return jsonify({"grafico": img_data})