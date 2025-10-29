// ===============================
// 🚗 SISTEMA DE DETECÇÃO DE COLISÃO IoT (Web)
// ===============================

// Estado global da simulação
const state = {
    carX: 50,
    distance: 100,
    speed: 1,
    isRunning: false,
    isColliding: false,
    collisions: 0,
    minDistance: 100,
    maxSpeed: 0,
    time: '00:00:00',
    totalTime: 0,
    collisionRate: 0,
    mqttClient: null,
    mqttConnected: false,
    dataPoints: { distance: [], collisions: [], timestamps: [] },
    charts: {}
};

// Referências DOM
const elements = {
    notificationContainer: document.getElementById('notificationContainer'),
    consoleLogs: document.getElementById('consoleLogs'),
    car: document.getElementById('car'),
    distanceIndicator: document.getElementById('distanceIndicator'),
    distanceDisplay: document.getElementById('distanceDisplay'),
    speedDisplay: document.getElementById('speedDisplay'),
    collisionCount: document.getElementById('collisionCount'),
    rateDisplay: document.getElementById('rateDisplay'),
    progressBar: document.getElementById('progressBar'),
    mqttStatus: document.getElementById('mqttStatus'),
    mqttStatusText: document.getElementById('mqttStatusText'),
    connectMqttBtn: document.getElementById('connectMqttBtn'),
    disconnectMqttBtn: document.getElementById('disconnectMqttBtn'),
    startBtn: document.getElementById('startBtn'),
    stopBtn: document.getElementById('stopBtn'),
    resetBtn: document.getElementById('resetBtn'),
    accelerateBtn: document.getElementById('accelerateBtn'),
    speedSlider: document.getElementById('speedSlider'),
    collisionOverlay: document.getElementById('collisionOverlay'),
    collisionAlert: document.getElementById('collisionAlert'),
    distanceAlert: document.getElementById('distanceAlert'),
    statsCollisions: document.getElementById('statsCollisions'),
    statsMinDistance: document.getElementById('statsMinDistance'),
    statsMaxSpeed: document.getElementById('statsMaxSpeed'),
    statsTotalTime: document.getElementById('statsTotalTime'),
    timer: document.getElementById('timer'),
    mqttServer: document.getElementById('mqttServer'),
    mqttPort: document.getElementById('mqttPort'),
    mqttUsername: document.getElementById('mqttUsername'),
    mqttTopic: document.getElementById('mqttTopic')
};

// ===============================
// 🔔 Sistema de Notificação
// ===============================
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `p-4 rounded-lg shadow-lg mb-2 ${
        type === 'success' ? 'bg-green-500' : 
        type === 'error' ? 'bg-red-500' : 
        type === 'warning' ? 'bg-yellow-500' : 'bg-blue-500'
    } text-white`;
    notification.textContent = message;
    
    elements.notificationContainer.appendChild(notification);
    setTimeout(() => notification.remove(), 3000);
}

// ===============================
// 🧾 Sistema de Logs
// ===============================
function addLog(message, type = 'info') {
    const now = new Date();
    const logEntry = document.createElement('div');
    logEntry.className = 'mb-2';
    
    const icon = type === 'error' ? '❌' : 
                type === 'warning' ? '⚠️' : 
                type === 'success' ? '✅' : 'ℹ️';
    
    logEntry.innerHTML = `
        <span class="text-gray-500">[${now.toLocaleTimeString()}]</span> 
        <span class="text-gray-300">${icon} ${message}</span>
    `;
    
    elements.consoleLogs.appendChild(logEntry);
    elements.consoleLogs.scrollTop = elements.consoleLogs.scrollHeight;
    
    if (elements.consoleLogs.children.length > 20)
        elements.consoleLogs.removeChild(elements.consoleLogs.children[0]);
}

// ===============================
// 🎛️ Atualização da Interface
// ===============================
function updateUI() {
    elements.car.style.left = `${state.carX}%`;
    elements.distanceIndicator.textContent = `${state.distance.toFixed(1)}cm`;
    elements.distanceDisplay.textContent = `${state.distance.toFixed(1)}cm`;
    elements.speedDisplay.textContent = `${Math.round(state.speed * 50)}%`;
    elements.collisionCount.textContent = state.collisions;
    elements.rateDisplay.textContent = state.collisionRate.toFixed(1);

    // Barra de progresso
    const progress = Math.max(0, Math.min(100, (100 - state.distance) * 2));
    elements.progressBar.style.width = `${progress}%`;

    // Status MQTT
    if (state.mqttConnected) {
        elements.mqttStatus.innerHTML = `<div class="w-2 h-2 bg-green-400 rounded-full"></div> Conectado`;
        elements.mqttStatus.className = 'text-xl font-bold text-green-400 flex items-center gap-2';
        elements.mqttStatusText.textContent = 'Status: Conectado ao broker MQTT';
        elements.mqttStatusText.className = 'mt-4 text-sm text-center text-green-400';
        elements.connectMqttBtn.classList.add('hidden');
        elements.disconnectMqttBtn.classList.remove('hidden');
    } else {
        elements.mqttStatus.innerHTML = `<div class="w-2 h-2 bg-red-400 rounded-full"></div> Desconectado`;
        elements.mqttStatus.className = 'text-xl font-bold text-red-400 flex items-center gap-2';
        elements.mqttStatusText.textContent = 'Status: Desconectado do broker MQTT';
        elements.mqttStatusText.className = 'mt-4 text-sm text-center text-gray-400';
        elements.connectMqttBtn.classList.remove('hidden');
        elements.disconnectMqttBtn.classList.add('hidden');
    }

    // Estado da colisão
    if (state.isColliding) {
        elements.collisionOverlay.classList.remove('hidden', 'opacity-0');
        elements.collisionOverlay.classList.add('opacity-40');
        elements.collisionAlert.innerHTML = `
            <div class="text-2xl mb-2">🚨</div>
            <p class="font-medium text-red-400">COLISÃO DETECTADA!</p>
        `;
    } else {
        elements.collisionOverlay.classList.add('hidden', 'opacity-0');
        elements.collisionOverlay.classList.remove('opacity-40');
        elements.collisionAlert.innerHTML = `
            <div class="text-2xl mb-2">🛑</div>
            <p class="font-medium text-gray-300">SEM COLISÃO</p>
        `;
    }

    // Alerta de distância
    if (state.distance < 20 && !state.isColliding) {
        elements.distanceAlert.innerHTML = `<div class="text-2xl mb-2">⚠️</div><p class="font-medium text-amber-400">PERIGO: PRÓXIMO!</p>`;
    } else {
        elements.distanceAlert.innerHTML = `<div class="text-2xl mb-2">✅</div><p class="font-medium text-gray-300">DISTÂNCIA SEGURA</p>`;
    }

    // Atualiza métricas e gráficos
    elements.statsCollisions.textContent = state.collisions;
    elements.statsMinDistance.textContent = `${state.minDistance.toFixed(1)}cm`;
    elements.statsMaxSpeed.textContent = `${state.maxSpeed}%`;
    elements.statsTotalTime.textContent = state.time;

    updateCharts();
}

// ===============================
// ⏱️ Timer da simulação
// ===============================
function startTimer() {
    setInterval(() => {
        if (!state.isRunning) return;

        state.totalTime++;
        const hours = Math.floor(state.totalTime / 3600);
        const minutes = Math.floor((state.totalTime % 3600) / 60);
        const seconds = state.totalTime % 60;

        state.time = `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
        elements.timer.textContent = state.time;

        if (state.totalTime > 0)
            state.collisionRate = (state.collisions / state.totalTime) * 60;
    }, 1000);
}

// ===============================
// 🚦 Inicialização
// ===============================
function init() {
    updateUI();
    feather.replace();
    addLog('Sistema inicializado com sucesso!', 'success');
}

init();
