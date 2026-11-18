// Conversor de la portada: mismas reglas que la app (Models.swift · Equivalence).
// kcal = pasos × 75 kg × 0,0005 ; tercios = kcal ÷ (330 ml × 43 kcal/100 ml).
(function () {
  var INK = '#12241C', FOAM = '#FFFDF2', BEER = '#FFAD14', AMBER = '#FFB21A', GLASS = '#DBAB73';
  var OUT = 'M76 18 L104 18 L104 66 C104 84 126 92 126 112 L126 210 Q126 226 112 226 L68 226 Q54 226 54 210 L54 112 C54 92 76 84 76 66 Z';
  var n = 0;
  function bottle(fill) {
    n += 1; var id = 'kb' + n, top = 40, bottom = 222;
    var y = bottom - (bottom - top) * Math.max(0, Math.min(1, fill));
    var inner = '';
    if (fill > 0) {
      var ft = Math.max(top - 8, y - 14);
      inner += '<rect x="0" y="' + y + '" width="180" height="' + (240 - y) + '" fill="' + BEER + '"/>';
      inner += '<rect x="0" y="' + (ft + 5) + '" width="180" height="' + Math.max(6, y - ft) + '" fill="' + FOAM + '"/>';
      for (var bx = 10; bx <= 170; bx += 22) inner += '<ellipse cx="' + (bx + 13) + '" cy="' + (ft + 5) + '" rx="13" ry="9" fill="' + FOAM + '"/>';
    }
    inner += '<path d="M70 124 L70 206" stroke="#fff" stroke-opacity=".7" stroke-width="8" stroke-linecap="round"/>';
    return '<svg viewBox="0 0 190 250" aria-hidden="true"><defs><clipPath id="' + id + '"><path d="' + OUT + '"/></clipPath></defs>' +
      '<path d="' + OUT + '" fill="' + INK + '" transform="translate(5,7)"/><path d="' + OUT + '" fill="' + GLASS + '"/>' +
      '<g clip-path="url(#' + id + ')">' + inner + '</g>' +
      '<rect x="60" y="116" width="60" height="30" rx="6" fill="none" stroke="' + INK + '" stroke-width="4"/>' +
      '<text x="90" y="138" text-anchor="middle" font-family="system-ui,sans-serif" font-weight="900" font-size="20" fill="' + INK + '">33cl</text>' +
      '<rect x="72" y="4" width="36" height="16" rx="4" fill="' + AMBER + '" stroke="' + INK + '" stroke-width="5"/>' +
      '<path d="' + OUT + '" fill="none" stroke="' + INK + '" stroke-width="7" stroke-linejoin="round"/></svg>';
  }
  function equivalence(steps) {
    var kcal = steps * 75 * 0.0005, raw = kcal / (330 * 43 / 100);
    var tenths = Math.floor(raw * 10 + 0.5), whole = Math.floor(tenths / 10), rest = tenths % 10;
    var completed = whole > 0 && rest === 0 ? whole - 1 : whole, fill = whole > 0 && rest === 0 ? 1 : rest / 10;
    return { kcal: kcal, raw: raw, amount: tenths / 10, completed: completed, fill: fill };
  }
  function es(x) { return x.toLocaleString('es-ES', { maximumFractionDigits: 1 }); }
  function texts(e) {
    if (e.raw > 0 && e.amount === 0) return ['menos de 0,1 tercios', 'Aún no llega a una décima'];
    if (e.amount === 0) return ['0 tercios', 'Sin pasos, sin equivalencia'];
    var noun = Math.abs(e.amount - 1) < 1e-4 ? 'tercio' : 'tercios', pct = Math.round(e.fill * 100), b;
    if (e.fill >= 1) b = (e.completed + 1) === 1 ? '1 tercio lleno' : (e.completed + 1) + ' tercios llenos';
    else if (e.completed === 0) b = '1 tercio al ' + pct + ' %';
    else b = (e.completed === 1 ? '1 lleno' : e.completed + ' llenos') + ' + 1 al ' + pct + ' %';
    return [es(e.amount) + ' ' + noun, b];
  }
  var input = document.getElementById('pasos');
  if (!input) return;
  var out = { steps: document.getElementById('pasos-num'), minis: document.getElementById('minis'), main: document.getElementById('principal'),
    total: document.getElementById('total'), breakdown: document.getElementById('desglose'), kcal: document.getElementById('kcal') };
  function render() {
    var steps = parseInt(input.value, 10), e = equivalence(steps), t = texts(e);
    out.steps.textContent = steps.toLocaleString('es-ES');
    var minis = '';
    if (e.completed > 0 && e.completed <= 3) for (var i = 0; i < e.completed; i++) minis += bottle(1);
    if (e.completed > 3) minis = bottle(1) + '<span class="badge">×' + e.completed + '</span>';
    out.minis.innerHTML = minis;
    out.main.innerHTML = bottle(e.fill);
    out.main.firstChild.style.transform = e.fill > 0 && e.fill < 1 ? 'rotate(-3deg)' : 'none';
    out.total.textContent = '≈ ' + t[0];
    out.breakdown.textContent = t[1];
    out.kcal.textContent = '≈ ' + Math.round(e.kcal) + ' kcal estimadas con 75 kg';
    input.setAttribute('aria-valuetext', steps + ' pasos, aproximadamente ' + t[0] + ': ' + t[1]);
  }
  input.addEventListener('input', render);
  render();
})();
