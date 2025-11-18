document.addEventListener('DOMContentLoaded', function() {
    // Adicionar classes de cor baseadas no nome da sala
    const rows = document.querySelectorAll('#result_list tr');
    
    rows.forEach(row => {
        const nomeCell = row.querySelector('.field-nome');
        if (nomeCell) {
            const nomeSala = nomeCell.textContent.trim();
            
            // Adicionar classes baseadas no nome da sala
            if (nomeSala.includes('Minhoto_Sonho')) {
                row.classList.add('sala-minhoto-sonho');
            } else if (nomeSala.includes('Minhoto')) {
                row.classList.add('sala-minhoto');
            } else if (nomeSala.includes('Sonho')) {
                row.classList.add('sala-sonho');
            }
            
            // Adicionar classe para salas especiais
            if (nomeSala.includes('Minhoto') || nomeSala.includes('Sonho')) {
                row.classList.add('sala-especial');
            }
        }
        
        // Colorir agendamentos baseados na data
        const dataInicioCell = row.querySelector('.field-data_inicio');
        const dataFimCell = row.querySelector('.field-data_fim');
        
        if (dataInicioCell && dataFimCell) {
            const hoje = new Date().toISOString().split('T')[0];
            const dataInicio = dataInicioCell.textContent.trim();
            const dataFim = dataFimCell.textContent.trim();
            
            if (dataFim < hoje) {
                row.classList.add('agendamento-passado');
            } else if (dataInicio > hoje) {
                row.classList.add('agendamento-futuro');
            } else {
                row.classList.add('agendamento-hoje');
            }
        }
    });
});