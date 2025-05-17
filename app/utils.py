import base64
from io import BytesIO
from matplotlib import pyplot as plt


def gerar_grafico(dados, tipo="bar"):
    """Gera um gráfico com base nos dados fornecidos"""
    plt.figure(figsize=(8, 4))
    
    if tipo == "bar":
        plt.bar(dados['categorias'], dados['valores'])
    elif tipo == "pie":
        plt.pie(dados['valores'], labels=dados['categorias'], autopct='%1.1f%%')
    elif tipo == "line":
        plt.plot(dados['categorias'], dados['valores'])
    
    plt.title(dados.get('titulo', 'Gráfico Financeiro'))
    plt.tight_layout()
    
    # Salva o gráfico em memória
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    
    # Converte para base64 para exibição na web
    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{img_base64}"