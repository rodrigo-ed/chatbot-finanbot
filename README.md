# FinanBot - README

## Descrição
FinanBot é um assistente virtual especializado em educação financeira. O objetivo do projeto é ajudar os usuários a gerenciar suas finanças pessoais, oferecendo funcionalidades como gerenciamento de metas, lembretes, geração de gráficos para visualização de gastos e interação via chat.

## Principais Tecnologias
- Python 3.10
- Flask
- Google Generative AI (Gemini)
- HTML5, CSS3, JavaScript (ES6+)
- Font Awesome, Google Fonts

## Estrutura do Projeto

```
FinanBot
├── app
│   ├── __init__.py          # Inicializa o pacote da aplicação Flask
│   ├── bot.py               # Lógica principal do assistente FinanBot
│   ├── routes.py            # Rotas da aplicação Flask
│   ├── utils.py             # Funções utilitárias
│   ├── static/              # Arquivos estáticos (CSS, JS, imagens)
│   └── templates/           # Templates HTML
│       └── index.html       # Template principal
├── data/                    # Dados de histórico, metas e lembretes
├── requirements.txt         # Dependências do projeto
├── run.py                   # Inicializa a aplicação
└── README.md                # Documentação
```

## 📸 Preview
Desktop	Mobile
<img src="https://github.com/rodrigo-ed/chatbot-finanbot.wiki.git" width="200" height="150">


Desktop Preview	Mobile Preview


## Funcionalidades

### Chat Interativo
- Conversa natural sobre finanças pessoais com respostas inteligentes.
- Sugestões automáticas de ações e dicas financeiras.

### Gerenciamento de Metas
- Criação, edição e acompanhamento de metas financeiras.
- Notificações e lembretes para metas.

### Visualização de Gastos
- Geração de gráficos dinâmicos para análise de despesas.
- Histórico de transações e categorias de gastos.

### Lembretes
- Agendamento de lembretes para pagamentos e compromissos financeiros.

### Interface Moderna
- Design responsivo para mobile e desktop.
- Dark Mode automático.
- Animações fluidas e microinterações.
- Acessibilidade (ARIA), loaders animados e feedback visual.

## Tecnologias Utilizadas

### Frontend
- HTML5, CSS3 (Flexbox/Grid)
- JavaScript (ES6+)
- Font Awesome, Google Fonts

### Backend
- Python 3.10
- Flask

### IA e APIs
- Google Generative AI (Gemini) para respostas inteligentes

## Como Executar

1. Clone o repositório:
   ```bash
   git clone <url-do-repositorio>
   cd FinanBot
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Execute a aplicação:
   ```bash
   python run.py
   ```

4. Acesse via navegador:
   ```
   http://localhost:5000
   ```

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## Licença

Este projeto está licenciado sob a licença MIT.


## Melhorias Futuras

- Integração com planilhas financeiras
- Análise de extratos bancários
- Versão mobile nativa
- Suporte a múltiplos usuários

