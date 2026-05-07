const API_URL = '/api/status';
const PNL_URL = '/api/pnl-history';

async function fetchPnLHistory() {
  const res = await fetch(PNL_URL);
  if (!res.ok) throw new Error('PnL error');
  return res.json();
}

function renderSparkline(data) {
  const container = document.getElementById('pnl-chart');
  if (!container) return;
  if (!data.pnl || data.pnl.length < 2) {
    container.textContent = 'No history';
    return;
  }
  const values = data.pnl.map(p => p.value);
  const min = Math.min(...values);
  const max = Math.max(...values);
  const range = max - min || 1;
  const width = 80;
  const height = 24;
  const points = values.map((v, i) => {
    const x = (i / (values.length - 1)) * width;
    const y = height - ((v - min) / range) * height;
    return `${x},${y}`;
  }).join(' ');
  const color = values[values.length - 1] >= 0 ? 'var(--green)' : 'var(--red)';
  container.innerHTML = `<svg width="${width}" height="${height}" viewBox="0 0 ${width} ${height}"><polyline points="${points}" fill="none" stroke="${color}" stroke-width="2"/></svg>`;
}

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
  document.getElementById('win-rate').textContent = `Win Rate: ${data.portfolio.win_rate || '--'}`;
}

function renderCounts(data) {
  document.getElementById('found').textContent = data.opportunities.length;
  document.getElementById('cross').textContent = data.opportunities.filter(o => o.type === 'cross_exchange').length;
  document.getElementById('triangular').textContent = data.opportunities.filter(o => o.type === 'triangular').length;
}

function renderExchanges(data) {
  const el = document.getElementById('win-rate');
  if (!el) return;
  const list = data.exchanges.slice(0, 6).join(', ') + (data.exchanges.length > 6 ? '...' : '');
  el.textContent = `Win Rate: ${data.portfolio.win_rate || '--'}`;
}

function renderAdvice(data) {
  const el = document.getElementById('ai-advice');
  if (data.ai_advice) {
    el.innerHTML = data.ai_advice;
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
    const [data, pnlData] = await Promise.all([fetchStatus(), fetchPnLHistory()]);
    renderStats(data);
    renderCounts(data);
    renderExchanges(data);
    renderAdvice(data);
    renderOpportunities(data);
    renderSparkline(pnlData);
  } catch (e) {
    console.error('Update failed:', e);
  }
}

document.addEventListener('DOMContentLoaded', () => {
  update();
  setInterval(update, 5000);
});