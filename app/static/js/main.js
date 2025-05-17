document.addEventListener('DOMContentLoaded', () => {
    const chat = document.getElementById('chat');
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');

    // Mensagem inicial do bot
    setTimeout(() => {
        addMessage('bot', 'Olá! 👋 Eu sou o FinanBot, seu assistente de educação financeira.', true);

    }, 1000);

    // Função para adicionar mensagem ao chat
    function addMessage(sender, text, isHTML = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;

        if (isHTML) {
            messageDiv.innerHTML = text;
        } else {
            messageDiv.textContent = text;
        }

        // Adiciona timestamp
        const timeSpan = document.createElement('span');
        timeSpan.className = 'message-time';
        timeSpan.textContent = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        messageDiv.appendChild(timeSpan);

        chat.appendChild(messageDiv);
        scrollToBottom();
    }

    // Mostra indicador de "digitando"
    function showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'typing-indicator';
        typingDiv.id = 'typing-indicator';

        for (let i = 0; i < 3; i++) {
            const dot = document.createElement('div');
            dot.className = 'typing-dot';
            typingDiv.appendChild(dot);
        }

        chat.appendChild(typingDiv);
        scrollToBottom();
    }

    // Esconde indicador de "digitando"
    function hideTypingIndicator() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    // Rolagem automática para o final do chat
    function scrollToBottom() {
        chat.scrollTop = chat.scrollHeight;
    }

    // Envia mensagem para o backend
    function sendMessage() {
        const message = messageInput.value.trim();
        if (!message) return;

        addMessage('user', message);
        messageInput.value = '';

        // Mostra indicador de que o bot está digitando
        showTypingIndicator();

        // Envia para o servidor (FETCH como no código original)
        fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ mensagem: message })
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro na resposta do servidor');
                }
                return response.json();
            })
            .then(data => {
                hideTypingIndicator();

                // Processa a resposta do servidor
                if (data.resposta) {
                    // Verifica se a resposta contém um gráfico
                    if (data.resposta.includes('![Gráfico')) {
                        const imgSrc = data.resposta.match(/\(([^)]+)\)/)[1];
                        addMessage('bot', data.resposta.replace(/!\[Gráfico.*?\]\(.*?\)/, ''), true);
                        addChart(imgSrc);
                    } else {
                        addMessage('bot', data.resposta, true);
                    }
                }
            })
            .catch(error => {
                hideTypingIndicator();
                addMessage('bot', '⚠️ Ocorreu um erro ao processar sua solicitação. Por favor, tente novamente.', true);
                console.error('Erro:', error);
            });
    }

    // Adiciona gráfico ao chat (igual ao original)
    function addChart(chartUrl) {
        const chartContainer = document.createElement('div');
        chartContainer.className = 'chart-container';

        const chartImg = document.createElement('img');
        chartImg.src = chartUrl;
        chartImg.alt = 'Gráfico financeiro';

        chartContainer.appendChild(chartImg);
        chat.appendChild(chartContainer);
        scrollToBottom();
    }

    // Event Listeners (mantidos)
    sendButton.addEventListener('click', sendMessage);

    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    // Foco automático no input
    messageInput.focus();
});