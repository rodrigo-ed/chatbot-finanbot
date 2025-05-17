# FinanBot - README

## Descrição
FinanBot é um assistente virtual especializado em educação financeira. O objetivo do projeto é ajudar os usuários a gerenciar suas finanças pessoais, oferecendo funcionalidades como gerenciamento de metas, lembretes e geração de gráficos para visualização de gastos.

## Estrutura do Projeto
```
FinanBot
├── app
│   ├── __init__.py          # Inicializa o pacote da aplicação Flask
│   ├── bot.py               # Contém a classe FinanBot com a lógica principal
│   ├── routes.py            # Define as rotas da aplicação Flask
│   ├── utils.py             # Funções utilitárias para suporte à aplicação
│   ├── static               # Arquivos estáticos (CSS/JS)
│   └── templates            # Templates HTML
│       └── index.html       # Template principal da aplicação
├── data                     # Armazena arquivos de histórico, metas e lembretes
├── requirements.txt         # Dependências do projeto
├── run.py                   # Ponto de entrada para executar a aplicação
└── README.md                # Documentação do projeto
```

## Instalação
1. Clone o repositório:
   ```
   git clone <URL_DO_REPOSITORIO>
   cd FinanBot
   ```

2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

## Uso
Para iniciar a aplicação, execute o seguinte comando:
```
python run.py
```
A aplicação estará disponível em `http://127.0.0.1:5000`.

## Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para abrir um pull request ou relatar problemas.

## Licença
Este projeto é licenciado sob a MIT License. Veja o arquivo LICENSE para mais detalhes.