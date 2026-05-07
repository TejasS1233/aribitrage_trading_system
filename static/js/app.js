const API_URL = '/api/status';

async function fetchStatus() {
  const res = await fetch(API_URL);
  if (!res.ok) throw new Error('API error');
  return res.json();
}

function formatCurrency(value) {
  return '$' + value.toLocaleString();
}

function formatProfit(profit) {
  const sign = profit >= 0 ? '+' : '';
  return sign + profit.toFixed(4) + '%';
}

function getProfitClass(profit) {
  return profit >= 0 ? 'positive' : 'negative';
}

function renderStats(data) {
  document.getElementById('balance').textContent = formatCurrency(data.portfolio.balance);
  document.getElementById('wins').textContent = data.portfolio.wins;
  document.getElementById('losses').textContent = data.portfolio.losses;
  document.getElementById('trades').textContent = data.portfolio.trades;
}

function renderCounts(data) {
  document.getElementById('found').textContent = data.opportunities.length;
  document.getElementById('cross').textContent = data.opportunities.filter(o => o.type === 'cross_exchange').length;
  document.getElementById('triangular').textContent = data.opportunities.filter(o => o.type === 'triangular').length;
  document.getElementById('opps-count').textContent = data.opportunities.length;
}

function renderExchanges(data) {
  const list = data.exchanges.slice(0, 6).join(', ') + (data.exchanges.length > 6 ? '...' : '');
  document.getElementById('exchanges-list').textContent = list || '-';
}

function renderAdvice(data) {
  const el = document.getElementById('ai-advice');
  if (data.ai_advice) {
    el.textContent = data.ai_advice;
  } else {
    el.textContent = 'Waiting for opportunities...';
  }
}

function renderOpportunities(data) {
  const container = document.getElementById('opps-list');
  
  if (!data.opportunities || data.opportunities.length === 0) {
    container.innerHTML = `
      <div class="empty-state">
        <div class="empty-icon">
          <svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
            <path d="M12 6v6l4 2"></path>
          </svg>
        </div>
        <div class="empty-title">No opportunities found</div>
        <div class="empty-desc">Keep scanning...</div>
      </div>
    `;
    return;
  }
  
  container.innerHTML = data.opportunities.map(o => {
    const path = Array.isArray(o.path) ? o.path.join(' → ') : o.path;
    const exchanges = o.exchanges.join(' → ');
    const type = o.type.replace('_', ' ');
    const profitClass = getProfitClass(o.profit);
    const profitDisplay = formatProfit(o.profit);
    const volume = o.volume ? formatCurrency(o.volume) : '$1,000';
    
    return `
      <div class="opp-item">
        <div class="opp-left">
          <span class="opp-type ${o.type}">${type}</span>
          <div>
            <div class="opp-path">${path}</div>
            <div class="opp-exchanges">${exchanges}</div>
          </div>
        </div>
        <div class="opp-right">
          <div class="opp-profit ${profitClass}">${profitDisplay}</div>
          <div class="opp-volume">Vol: ${volume}</div>
        </div>
      </div>
    `;
  }).join('');
}

async function update() {
  try {
    const data = await fetchStatus();
    renderStats(data);
    renderCounts(data);
    renderExchanges(data);
    renderAdvice(data);
    renderOpportunities(data);
  } catch (e) {
    console.error('Update failed:', e);
  }
}

document.addEventListener('DOMContentLoaded', () => {
  update();
  setInterval(update, 5000);
});