const API_URL = 'http://localhost:8000';

// Inicializar la aplicación
document.addEventListener('DOMContentLoaded', () => {
    setupTabs();
    setupForms();
    loadAllData();
});

// Configurar tabs
function setupTabs() {
    const tabs = document.querySelectorAll('.tab-btn');
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // Actualizar tabs
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            
            // Actualizar contenido
            document.querySelectorAll('.tab-content').forEach(content => {
                content.classList.remove('active');
            });
            document.getElementById(`${tab.dataset.tab}-tab`).classList.add('active');
            
            // Recargar datos según tab
            if (tab.dataset.tab === 'votes') {
                loadVotersSelect();
                loadCandidatesSelect();
            }
            if (tab.dataset.tab === 'statistics') {
                loadStatistics();
            }
        });
    });
}

// Configurar formularios
function setupForms() {
    // Formulario de votantes
    document.getElementById('voter-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const name = document.getElementById('voter-name').value;
        const email = document.getElementById('voter-email').value;
        await createVoter(name, email);
        document.getElementById('voter-form').reset();
        await loadVoters();
        await updateCounts();
    });

    // Formulario de candidatos
    document.getElementById('candidate-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const name = document.getElementById('candidate-name').value;
        const email = document.getElementById('candidate-email').value;
        const party = document.getElementById('candidate-party').value;
        await createCandidate(name, email, party);
        document.getElementById('candidate-form').reset();
        await loadCandidates();
        await updateCounts();
    });

    // Formulario de votos
    document.getElementById('vote-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const voterId = document.getElementById('voter-select').value;
        const candidateId = document.getElementById('candidate-select').value;
        await createVote(voterId, candidateId);
        document.getElementById('vote-form').reset();
        await loadVotes();
        await loadStatistics();
        await loadVotersSelect();
        await loadCandidatesSelect();
        await updateCounts();
    });
}

// Cargar todos los datos
async function loadAllData() {
    await loadVoters();
    await loadCandidates();
    await loadVotes();
    await loadStatistics();
    await loadVotersSelect();
    await loadCandidatesSelect();
    await updateCounts();
}

// ==================== VOTANTES ====================
async function loadVoters() {
    try {
        const response = await fetch(`${API_URL}/voters`);
        if (!response.ok) {
            console.error('Error al cargar votantes:', response.status);
            return;
        }
        const data = await response.json();
        const container = document.getElementById('voters-list');
        container.innerHTML = '';
        
        if (data.voters && data.voters.length > 0) {
            data.voters.forEach(voter => {
                const div = document.createElement('div');
                div.className = 'list-item';
                div.innerHTML = `
                    <div class="info">
                        <strong>${voter.name}</strong>
                        <span class="email">${voter.email}</span>
                        <span class="badge ${voter.has_voted ? 'voted' : 'pending'}">
                            ${voter.has_voted ? '✅ Votó' : '⏳ Pendiente'}
                        </span>
                    </div>
                    <div class="actions">
                        <button onclick="deleteVoter(${voter.id})" class="btn-delete">Eliminar</button>
                    </div>
                `;
                container.appendChild(div);
            });
        } else {
            container.innerHTML = '<p style="color: #999; text-align: center; padding: 20px;">No hay votantes registrados</p>';
        }
    } catch (error) {
        console.error('Error al cargar votantes:', error);
        document.getElementById('voters-list').innerHTML = '<p style="color: #999; text-align: center; padding: 20px;">Error al cargar votantes</p>';
    }
}

async function createVoter(name, email) {
    try {
        const response = await fetch(`${API_URL}/voters`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, email })
        });
        
        if (response.ok) {
            showMessage('success', '✅ Votante registrado correctamente');
        } else {
            const error = await response.json();
            showMessage('error', error.detail || '❌ Error al registrar votante');
        }
    } catch (error) {
        showMessage('error', '❌ Error de conexión');
    }
}

async function deleteVoter(id) {
    if (!confirm('¿Eliminar este votante?')) return;
    
    try {
        const response = await fetch(`${API_URL}/voters/${id}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            showMessage('success', '✅ Votante eliminado');
            await loadVoters();
            await updateCounts();
        } else {
            showMessage('error', '❌ Error al eliminar');
        }
    } catch (error) {
        showMessage('error', '❌ Error de conexión');
    }
}

// ==================== CANDIDATOS ====================
async function loadCandidates() {
    try {
        const response = await fetch(`${API_URL}/candidates`);
        if (!response.ok) {
            console.error('Error al cargar candidatos:', response.status);
            return;
        }
        const data = await response.json();
        const container = document.getElementById('candidates-list');
        container.innerHTML = '';
        
        if (data.candidates && data.candidates.length > 0) {
            data.candidates.forEach(candidate => {
                const div = document.createElement('div');
                div.className = 'list-item';
                div.innerHTML = `
                    <div class="info">
                        <strong>${candidate.name}</strong>
                        <span class="email">${candidate.email}</span>
                        ${candidate.party ? `<span style="color: #666;">| ${candidate.party}</span>` : ''}
                        <span style="color: #667eea; margin-left: 10px;">🗳️ ${candidate.votes} votos</span>
                    </div>
                    <div class="actions">
                        <button onclick="deleteCandidate(${candidate.id})" class="btn-delete">Eliminar</button>
                    </div>
                `;
                container.appendChild(div);
            });
        } else {
            container.innerHTML = '<p style="color: #999; text-align: center; padding: 20px;">No hay candidatos registrados</p>';
        }
    } catch (error) {
        console.error('Error al cargar candidatos:', error);
        document.getElementById('candidates-list').innerHTML = '<p style="color: #999; text-align: center; padding: 20px;">Error al cargar candidatos</p>';
    }
}

async function createCandidate(name, email, party) {
    try {
        const response = await fetch(`${API_URL}/candidates`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, email, party: party || null })
        });
        
        if (response.ok) {
            showMessage('success', '✅ Candidato registrado correctamente');
        } else {
            const error = await response.json();
            showMessage('error', error.detail || '❌ Error al registrar candidato');
        }
    } catch (error) {
        showMessage('error', '❌ Error de conexión');
    }
}

async function deleteCandidate(id) {
    if (!confirm('¿Eliminar este candidato?')) return;
    
    try {
        const response = await fetch(`${API_URL}/candidates/${id}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            showMessage('success', '✅ Candidato eliminado');
            await loadCandidates();
            await loadStatistics();
            await updateCounts();
        } else {
            showMessage('error', '❌ Error al eliminar');
        }
    } catch (error) {
        showMessage('error', '❌ Error de conexión');
    }
}

// ==================== VOTOS ====================
async function loadVotes() {
    try {
        const response = await fetch(`${API_URL}/votes`);
        if (!response.ok) {
            console.error('Error al cargar votos:', response.status);
            return;
        }
        const votes = await response.json();
        const container = document.getElementById('votes-list');
        container.innerHTML = '';
        
        if (votes && votes.length > 0) {
            votes.forEach(vote => {
                const div = document.createElement('div');
                div.className = 'list-item';
                div.innerHTML = `
                    <div class="info">
                        <strong>${vote.voter_name || 'Desconocido'}</strong>
                        <span style="color: #666;">→</span>
                        <strong>${vote.candidate_name || 'Desconocido'}</strong>
                        ${vote.candidate_party ? `<span style="color: #666;">(${vote.candidate_party})</span>` : ''}
                        <span style="color: #999; font-size: 12px; margin-left: 10px;">${vote.created_at ? new Date(vote.created_at).toLocaleString() : ''}</span>
                    </div>
                `;
                container.appendChild(div);
            });
        } else {
            container.innerHTML = '<p style="color: #999; text-align: center; padding: 20px;">No hay votos registrados</p>';
        }
    } catch (error) {
        console.error('Error al cargar votos:', error);
        document.getElementById('votes-list').innerHTML = '<p style="color: #999; text-align: center; padding: 20px;">Error al cargar votos</p>';
    }
}

async function createVote(voterId, candidateId) {
    try {
        const response = await fetch(`${API_URL}/votes`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                voter_id: parseInt(voterId), 
                candidate_id: parseInt(candidateId) 
            })
        });
        
        if (response.ok) {
            showMessage('success', '✅ Voto registrado correctamente');
            await loadVotes();
            await loadStatistics();
            await loadVotersSelect();
            await loadCandidatesSelect();
            await updateCounts();
        } else {
            const error = await response.json();
            showMessage('error', error.detail || '❌ Error al registrar voto');
        }
    } catch (error) {
        console.error('Error al crear voto:', error);
        showMessage('error', '❌ Error de conexión');
    }
}

async function loadVotersSelect() {
    try {
        const response = await fetch(`${API_URL}/voters`);
        if (!response.ok) {
            console.error('Error al cargar votantes para select:', response.status);
            return;
        }
        const data = await response.json();
        const select = document.getElementById('voter-select');
        select.innerHTML = '<option value="">Seleccionar Votante</option>';
        
        if (data.voters && data.voters.length > 0) {
            let hasAvailable = false;
            data.voters.forEach(voter => {
                const option = document.createElement('option');
                option.value = voter.id;
                option.textContent = `${voter.name} (${voter.email})`;
                if (voter.has_voted) {
                    option.textContent += ' ❌ Ya votó';
                    option.disabled = true;
                } else {
                    option.textContent += ' ✅ Disponible';
                    hasAvailable = true;
                }
                select.appendChild(option);
            });
            if (!hasAvailable) {
                const option = document.createElement('option');
                option.value = '';
                option.textContent = '⚠️ No hay votantes disponibles';
                option.disabled = true;
                select.appendChild(option);
            }
        }
    } catch (error) {
        console.error('Error al cargar votantes:', error);
    }
}

async function loadCandidatesSelect() {
    try {
        const response = await fetch(`${API_URL}/candidates`);
        if (!response.ok) {
            console.error('Error al cargar candidatos para select:', response.status);
            return;
        }
        const data = await response.json();
        const select = document.getElementById('candidate-select');
        select.innerHTML = '<option value="">Seleccionar Candidato</option>';
        
        if (data.candidates && data.candidates.length > 0) {
            data.candidates.forEach(candidate => {
                const option = document.createElement('option');
                option.value = candidate.id;
                option.textContent = `${candidate.name}${candidate.party ? ` (${candidate.party})` : ''}`;
                select.appendChild(option);
            });
        } else {
            const option = document.createElement('option');
            option.value = '';
            option.textContent = '⚠️ No hay candidatos disponibles';
            option.disabled = true;
            select.appendChild(option);
        }
    } catch (error) {
        console.error('Error al cargar candidatos:', error);
    }
}

// ==================== ESTADÍSTICAS ====================
async function loadStatistics() {
    try {
        const response = await fetch(`${API_URL}/votes/statistics`);
        if (!response.ok) {
            console.error('Error al cargar estadísticas:', response.status);
            const container = document.getElementById('statistics-container');
            container.innerHTML = '<p style="color: #999; text-align: center; padding: 20px;">Error al cargar estadísticas</p>';
            return;
        }
        const stats = await response.json();
        const container = document.getElementById('statistics-container');
        
        // Resumen general
        let html = `
            <div class="statistics-grid">
                <div class="stat-card">
                    <div class="number">${stats.total_voters || 0}</div>
                    <div class="label">Total Votantes</div>
                </div>
                <div class="stat-card">
                    <div class="number">${stats.total_voted || 0}</div>
                    <div class="label">Han Votado</div>
                </div>
                <div class="stat-card">
                    <div class="number">${(stats.total_voters || 0) - (stats.total_voted || 0)}</div>
                    <div class="label">Pendientes</div>
                </div>
                <div class="stat-card">
                    <div class="number">${stats.total_candidates || 0}</div>
                    <div class="label">Total Candidatos</div>
                </div>
                <div class="stat-card">
                    <div class="number">${stats.total_votes || 0}</div>
                    <div class="label">Total Votos</div>
                </div>
            </div>
            <h3 style="margin: 20px 0 15px 0;">🏆 Resultados por Candidato</h3>
        `;
        
        if (stats.results && stats.results.length > 0) {
            const maxVotes = Math.max(...stats.results.map(r => r.votes));
            
            stats.results.forEach(result => {
                const percentage = maxVotes > 0 ? (result.votes / maxVotes) * 100 : 0;
                html += `
                    <div class="result-item">
                        <div class="candidate-info">
                            <strong>${result.candidate_name}</strong>
                            ${result.party ? `<span class="party">${result.party}</span>` : ''}
                        </div>
                        <div class="votes-info">
                            <span class="votes">${result.votes}</span>
                            <span class="percentage">${result.percentage}%</span>
                        </div>
                    </div>
                    <div class="bar-container">
                        <div class="bar-fill" style="width: ${percentage}%;"></div>
                    </div>
                `;
            });
        } else {
            html += '<p style="color: #999; text-align: center; padding: 20px;">📊 No hay resultados disponibles aún. ¡Registra votos para ver las estadísticas!</p>';
        }
        
        container.innerHTML = html;
    } catch (error) {
        console.error('Error al cargar estadísticas:', error);
        const container = document.getElementById('statistics-container');
        container.innerHTML = '<p style="color: #999; text-align: center; padding: 20px;">Error al cargar estadísticas</p>';
    }
}

// ==================== UTILIDADES ====================
function showMessage(type, text) {
    let messageDiv = document.getElementById('message');
    if (!messageDiv) {
        const container = document.querySelector('.container');
        const div = document.createElement('div');
        div.id = 'message';
        div.className = `message ${type}`;
        div.textContent = text;
        container.prepend(div);
        setTimeout(() => div.remove(), 4000);
    } else {
        messageDiv.className = `message ${type}`;
        messageDiv.textContent = text;
        messageDiv.style.display = 'block';
        setTimeout(() => {
            messageDiv.style.display = 'none';
        }, 4000);
    }
}

// Actualizar contadores en tabs
function updateCounts() {
    // Contar votantes
    fetch(`${API_URL}/voters`)
        .then(res => res.json())
        .then(data => {
            const count = document.getElementById('voters-count');
            if (count) count.textContent = data.voters ? data.voters.length : 0;
        })
        .catch(() => {});
    
    // Contar candidatos
    fetch(`${API_URL}/candidates`)
        .then(res => res.json())
        .then(data => {
            const count = document.getElementById('candidates-count');
            if (count) count.textContent = data.candidates ? data.candidates.length : 0;
        })
        .catch(() => {});
    
    // Contar votos
    fetch(`${API_URL}/votes`)
        .then(res => res.json())
        .then(data => {
            const count = document.getElementById('votes-count');
            if (count) count.textContent = Array.isArray(data) ? data.length : 0;
        })
        .catch(() => {});
}

// Auto-refresh cada 10 segundos
setInterval(() => {
    const activeTab = document.querySelector('.tab-btn.active');
    if (activeTab) {
        const tabName = activeTab.dataset.tab;
        if (tabName === 'statistics') {
            loadStatistics();
        }
        if (tabName === 'votes') {
            loadVotes();
            loadVotersSelect();
            loadCandidatesSelect();
        }
        if (tabName === 'voters') {
            loadVoters();
        }
        if (tabName === 'candidates') {
            loadCandidates();
        }
        updateCounts();
    }
}, 30000); // Actualizar cada 30 segundos