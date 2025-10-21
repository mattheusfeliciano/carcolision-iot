elements.speedSlider.addEventListener('input', function(e) {
    state.speed = parseFloat(e.target.value);
    addLog(`⚡ Velocidade ajustada para: ${Math.round(state.speed * 50)}%`);
});  // ← Adicione essas duas chaves aqui

// Initialize the application
init();