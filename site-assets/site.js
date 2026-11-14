const root = document.body.dataset.root || '';
const inputs = document.querySelectorAll('.search');
let index;
const esc = s => s.replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]));
inputs.forEach(input => input.addEventListener('input', async () => {
  const results = input.nextElementSibling;
  const query = input.value.trim().toLowerCase();
  results.replaceChildren();
  if (query.length < 2) return;
  try {
    index ||= await (await fetch(root + 'search.json')).json();
    const terms = query.split(/\s+/);
    const scored = [];
    for (const p of index) {
      const title = p.title.toLowerCase(), text = p.text.toLowerCase();
      if (!terms.every(t => title.includes(t) || text.includes(t))) continue;
      scored.push({p, score: terms.reduce((s, t) => s + (title.includes(t) ? 50 : 0) + Math.min(10, text.split(t).length - 1), 0)});
    }
    scored.sort((a, b) => b.score - a.score);
    for (const {p} of scored.slice(0, 25)) {
      const a = document.createElement('a'); a.href = root + p.url;
      const at = p.text.toLowerCase().indexOf(terms[0]);
      const snip = at < 0 ? '' : (at > 40 ? '…' : '') + p.text.slice(Math.max(0, at - 40), at + 90) + '…';
      a.innerHTML = '<strong>' + esc(p.title) + '</strong>' + (snip ? '<br><small>' + esc(snip) + '</small>' : '');
      results.append(a);
    }
    if (!scored.length) results.textContent = 'No matching pages.';
  } catch { results.textContent = 'Search unavailable. Use the navigation below.'; }
}));
document.querySelectorAll('article table').forEach(table => {
  const wrapper = document.createElement('div'); wrapper.className = 'table-scroll';
  wrapper.tabIndex = 0; wrapper.setAttribute('role', 'region'); wrapper.setAttribute('aria-label', 'Scrollable table');
  table.before(wrapper); wrapper.append(table);
});
