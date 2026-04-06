// Variável global para o gráfico (para podermos atualizar os dados sem recriá-lo)
let chartInstance = null;

async function atualizarInterface() {
    try {
        const response = await fetch("https://titan-motors-projeto.onrender.com/dados");
        const data = await response.json();

        console.log("Dados recebidos da API:", data); // <-- ADICIONE ISSO AQUI

        if (!Array.isArray(data) || data.length === 0) return;

        // 1. LÓGICA PARA A LISTA SIMPLES (Atualizada para os nomes do Neon)
        const container = document.getElementById("dados");
        if (container) {
            container.innerHTML = "";
            data.forEach(item => {
                const linha = document.createElement("div");
                linha.style.padding = "10px";
                linha.style.borderBottom = "1px solid #ccc";
                
                // Mapeia os nomes que vêm do banco (podem variar entre maiúsculas/minúsculas)
                const rpm = item.rpm || item.RPM || 0;
                const vibracao = item.vibracao || item.vibracao || 0;
                const saude = item.health || item.Health || 0;
                const tempo = item.timestamp || "---";

                linha.innerHTML = `
                    ⏱ ${tempo} | 
                    ⚙ **RPM:** ${rpm} | 
                    📳 **Vibração:** ${Number(vibracao).toFixed(2)} | 
                    ❤️ **Saúde:** ${(Number(saude) * 100).toFixed(1)}%
                `;
                container.appendChild(linha);
            });
        }

        // 2. LÓGICA PARA O DASHBOARD (RPM, SAÚDE E CUSTOS)
        const rpmCard = document.getElementById("rpm-val");
        const healthCard = document.getElementById("health-val");
        const cardSaudeContainer = document.getElementById("card-saude");

        if (rpmCard && healthCard) {
            const maisRecente = data[0]; 
            const saudePercentual = (maisRecente.health * 100).toFixed(1);
            
            // Atualiza os textos básicos
            rpmCard.innerText = maisRecente.rpm;
            healthCard.innerText = saudePercentual + "%";

            // --- LÓGICA DE CUSTOS AUTOMATIZADA ---
            // Seleciona os valores dentro dos cards financeiros
            const elementoPrejuizo = document.querySelector(".custo-prejuizo + p strong");
            const elementoEconomia = document.querySelector(".custo-ganho + p strong");

            if (elementoPrejuizo && elementoEconomia) {
                // Cálculo dinâmico: quanto menor a saúde, maior o prejuízo potencial
                const prejuizoCalculado = (100 - saudePercentual) * 250; 
                const economiaCalculada = 15000 - prejuizoCalculado; // Exemplo de ROI

                elementoPrejuizo.innerText = `R$ ${prejuizoCalculado.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`;
                elementoEconomia.innerText = `R$ ${economiaCalculada.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`;
            }

            // ALERTA VISUAL (Pulsação vermelha se saúde < 70%)
            if (cardSaudeContainer) {
                if (saudePercentual < 70) {
                    cardSaudeContainer.classList.add("alerta-critico");
                    document.getElementById("status-text").innerText = "⚠️ MANUTENÇÃO NECESSÁRIA";
                } else {
                    cardSaudeContainer.classList.remove("alerta-critico");
                    document.getElementById("status-text").innerText = "✅ Operação Normal";
                }
            }

            // Atualiza o Gráfico com os últimos 10 pontos
            atualizarGrafico(data.slice(0, 10).reverse());
        }

    } catch (error) {
        console.error("Erro ao conectar na API:", error);
    }
}

function atualizarGrafico(ultimosDados) {
    const ctx = document.getElementById('vibrationChart');
    if (!ctx) return;

    // 1. Criamos os rótulos (labels) para o eixo X com segurança
    const labels = ultimosDados.map(d => {
        // Se o timestamp existir e for uma string com espaço, pegamos só a hora
        if (d.timestamp && typeof d.timestamp === 'string' && d.timestamp.includes(' ')) {
            return d.timestamp.split(' ')[1]; 
        }
        return d.timestamp || "--:--"; // Fallback caso o dado esteja incompleto
    });

    // 2. Criamos a lista de valores de vibração garantindo que sejam números
    const valores = ultimosDados.map(d => Number(d.vibracao) || 0);

    if (!chartInstance) {
        // Cria o gráfico pela primeira vez se ele não existir
        chartInstance = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Nível de Vibração',
                    data: valores,
                    borderColor: '#00d4ff',
                    tension: 0.3,
                    fill: true,
                    backgroundColor: 'rgba(0, 212, 255, 0.1)'
                }]
            },
            options: { 
                responsive: true, 
                maintainAspectRatio: false,
                scales: {
                    y: { beginAtZero: true } // Ajuda a visualizar melhor as variações
                }
            }
        });
    } else {
        // Se o gráfico já existe, apenas atualizamos os dados
        chartInstance.data.labels = labels;
        chartInstance.data.datasets[0].data = valores;
        chartInstance.update('none'); // Atualização suave sem resetar a animação
    }
}

// Executa a função assim que a página termina de carregar
window.onload = () => {
    // Primeira chamada para não esperar os primeiros 2 segundos
    atualizarInterface();

    // Define o intervalo de atualização (300000 milissegundos = 5 minutos)
    setInterval(atualizarInterface, 300000);
};

/*// Inicia o loop de atualização (5 minutos)
setInterval(atualizarInterface, 300000);
atualizarInterface();*/

