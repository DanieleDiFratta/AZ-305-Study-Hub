/* Static views: all durable updates come from the repository, never browser storage. */
(() => {
  'use strict';
  const data = window.STUDY_DATA;
  const main = document.getElementById('main');
  if (!data) {
    main.innerHTML = '<div class="loading-error"><h1>Dati non disponibili</h1><p>Ricostruisci il sito con <code>python scripts/build_site.py</code> e riapri la dashboard.</p></div>';
    return;
  }
  const { baseline, progress, resources, blocks, materials } = data;
  const resourceById = new Map(resources.map(r => [r.id, r]));
  const blockById = new Map(blocks.map(b => [b.id, b]));
  const stateLabels = { proposed: 'Proposto', read: 'Letto', discussed: 'Discusso', practiced: 'Esercitato', verified: 'Verificato' };
  const kindLabels = { documentation: 'Documentazione', comparison: 'Confronti', learn_path: 'Percorsi Learn', learn_module: 'Moduli Learn', learn_unit: 'Unità Learn', official_case: 'Casi ufficiali', reference_architecture: 'Architetture', diagram: 'Diagrammi', well_architected: 'Well-Architected', cloud_adoption: 'Cloud Adoption', lifecycle: 'Aggiornamenti e ritiri', customer_story: 'Customer story', exam: 'Certificazione', exam_guide: 'Programma ufficiale', course: 'Corso ufficiale', official_exercises: 'Indici degli esercizi' };
  const materialLabels = { notes: 'Appunti', map: 'Mappe', flashcards: 'Flashcard' };
  const flagLabels = { compare_b2c_external_id_with_current_docs: 'Confrontare B2C ed External ID con la documentazione corrente.', redis_retirement_dates_require_current_faq: 'Controllare le timeline di ritiro nella FAQ corrente.', outbound_defaults_depend_on_api_version: 'Il comportamento outbound dipende dalla versione API e dalla configurazione.', scenario_not_current_product_specification: 'Caso didattico: verificare separatamente le specifiche attuali dei servizi.', no_formal_case_study: 'Questa voce non contiene un caso formale.' };
  const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const formatDate = (value, options = {}) => new Intl.DateTimeFormat('it-IT', { day: 'numeric', month: 'long', year: 'numeric', timeZone: 'Europe/Rome', ...options }).format(new Date(value + 'T12:00:00Z'));
  const today = () => new Intl.DateTimeFormat('en-CA', { timeZone: 'Europe/Rome', year: 'numeric', month: '2-digit', day: '2-digit' }).format(new Date());
  const isFresh = r => r.next_review_on >= today();
  const isAccessible = r => r.status === 'public_content' || r.status === 'public_asset';
  const validPrimary = r => r.role === 'primary' && r.mapping_scope === 'direct' && r.status === 'public_content' && r.http_status === 200 && r.review_current && isFresh(r);
  const countState = (ids, state) => ids.filter(id => progress.objectives[id]?.[state]).length;
  const allIds = baseline.objectives.map(o => o.id);
  const verifiedIds = () => allIds.filter(id => progress.objectives[id]?.verified);
  const coveredIds = () => allIds.filter(id => resources.some(r => r.objective_ids.includes(id) && validPrimary(r)));
  const objectiveLabel = id => baseline.objectives.find(o => o.id === id)?.label_it || id;
  const external = (url, label, cls = '') => `<a class="${esc(cls)}" href="${esc(url)}" target="_blank" rel="noopener noreferrer">${label} <span aria-hidden="true">↗</span></a>`;
  const empty = (title, message, action = '') => `<div class="empty"><div class="empty-icon" aria-hidden="true">▧</div><h2>${esc(title)}</h2><p>${esc(message)}</p>${action}</div>`;
  const heading = (eyebrow, title, subtitle, aside = '') => `<div class="page-heading"><div><p class="eyebrow">${esc(eyebrow)}</p><h1>${esc(title)}</h1><p>${esc(subtitle)}</p></div>${aside}</div>`;
  const blockLink = (id, text) => `<a href="#blocco/${esc(id)}">${esc(text || id)}</a>`;
  const blockStatus = b => progress.blocks[b.id]?.verified ? '<span class="tag green">Verificato</span>' : Object.keys(progress.blocks[b.id] || {}).length ? '<span class="tag green">Avviato</span>' : '<span class="tag">Da iniziare</span>';

  function resourceCard(r, compact = false) {
    const status = r.status === 'public_placeholder' ? '<span class="tag orange">Nessun caso formale</span>' : !isAccessible(r) ? '<span class="tag orange">Contenuto non disponibile</span>' : !r.review_current ? '<span class="tag orange">Revisione da aggiornare</span>' : !isFresh(r) ? '<span class="tag orange">Verifica scaduta</span>' : '<span class="tag green">Fonte verificata</span>';
    return `<article class="resource">${external(r.url, esc(r.title))}${!compact && r.selection_reason_it ? `<p>${esc(r.selection_reason_it)}</p>` : ''}<div class="resource-meta"><span class="tag">${esc(kindLabels[r.kind] || r.kind)}</span>${status}<span>${esc(r.language)}</span><code>${esc(r.id)}</code></div>${!compact ? `<small>Verificata il ${formatDate(r.verified_on)} · Da ricontrollare entro il ${formatDate(r.next_review_on)}${r.objective_ids.length ? `<br>Obiettivi: ${esc(r.objective_ids.join(', '))}${r.mapping_scope !== 'direct' ? ' · associazione di contesto' : ''}` : ''}</small>${r.flags.length ? `<small>${r.flags.map(f => esc(flagLabels[f] || f)).join(' ')}</small>` : ''}` : ''}</article>`;
  }

  function renderHome() {
    const resume = progress.resume;
    const block = blockById.get(resume.block_id);
    const days = Math.ceil((Date.parse(progress.exam_date + 'T00:00:00Z') - Date.parse(today() + 'T00:00:00Z')) / 86400000);
    const covered = coveredIds().length;
    const verified = verifiedIds().length;
    const recentMaterials = [...materials].sort((a, b) => b.published_on.localeCompare(a.published_on)).slice(0, 3);
    const reviews = progress.reviews.filter(r => !r.completed_on).sort((a, b) => a.due_on.localeCompare(b.due_on));
    main.innerHTML = heading('LA PREPARAZIONE, UN PASSO ALLA VOLTA', 'Il tuo prossimo passo.', 'Uno spazio per studiare, collegare le idee e ritrovarle.', `<div class="date-tag"><span>Esame</span> ${formatDate(progress.exam_date)}</div>`) +
      `<section class="hero" aria-labelledby="resume-title"><div class="hero-content"><p class="eyebrow">${Object.keys(progress.blocks[block.id] || {}).length ? 'RIPRENDI IL FILO' : 'IL PUNTO DI PARTENZA'}</p><span class="tag outline">${esc(block.id)} · ${esc(block.estimate)}</span><h2 id="resume-title">${esc(block.title)}</h2><p>${esc(resume.summary)}</p><a class="button" href="#blocco/${esc(block.id)}">${Object.keys(progress.blocks[block.id] || {}).length ? 'Riprendi il blocco' : 'Apri il primo blocco'} <span aria-hidden="true">→</span></a></div><div class="hero-art" aria-hidden="true"><div class="orbit"><div class="orbit-inner">↗</div></div><span>DAL REQUISITO ALLA SCELTA</span></div></section>` +
      `<section class="stats" aria-label="Il percorso in numeri"><div class="stat"><div class="stat-label"><span aria-hidden="true">◷</span> ${days > 0 ? 'Giorni all’esame' : 'Data dell’esame'}</div><div class="stat-value">${days > 0 ? days : formatDate(progress.exam_date, { year: undefined, month: 'short' })}</div><p>${days > 0 ? 'Un blocco alla volta, fino al 1° dicembre.' : 'Consulta il percorso e le verifiche registrate.'}</p></div><div class="stat"><div class="stat-label"><span aria-hidden="true">✓</span> Obiettivi verificati</div><div class="stat-value">${verified} <small>/ ${allIds.length}</small></div><p>Comprensione con evidenza personale</p></div><div class="stat"><div class="stat-label"><span aria-hidden="true">▧</span> Sessioni svolte</div><div class="stat-value">${progress.sessions.length}</div><p>Registrate alla chiusura dello studio</p></div><div class="stat"><div class="stat-label"><span aria-hidden="true">▤</span> Materiali di ripasso</div><div class="stat-value">${materials.length}</div><p>Appunti, mappe e raccolte di flashcard</p></div></section>` +
      `<div class="home-grid"><div><section aria-labelledby="domains-title"><div class="section-heading"><h2 id="domains-title">I quattro domini</h2><a href="#percorso">Esplora il percorso →</a></div><div class="domain-list">${baseline.domains.map((d, i) => {
        const ids = baseline.objectives.filter(o => o.domain === d.id).map(o => o.id);
        const count = countState(ids, 'verified');
        return `<article class="domain"><div class="domain-icon" aria-hidden="true">${['◇', '▱', '↻', '⌘'][i]}</div><div><div class="domain-top"><h3><a href="#biblioteca?domain=${esc(d.id)}">${esc(d.label_it)}</a></h3><span>${count}/${ids.length} verificati</span></div><progress max="${ids.length}" value="${count}" aria-label="${esc(d.label_it)}: ${count} obiettivi verificati su ${ids.length}"></progress><div class="domain-meta"><span>${countState(ids, 'read')} letti · ${countState(ids, 'discussed')} discussi · ${countState(ids, 'practiced')} esercitati</span><span>Peso ${esc(d.weight)}</span></div></div></article>`;
      }).join('')}</div><div class="callout">Biblioteca: <strong>${covered}/${allIds.length} obiettivi con fonti primarie valide</strong> secondo le revisioni registrate. La copertura delle fonti è distinta dalla tua preparazione.</div></section><section class="panel" aria-labelledby="method-title"><p class="eyebrow">IL METODO DI STUDIO</p><h2 id="method-title">Prima leggi, poi approfondiamo.</h2><p>Fonti precise, lettura autonoma, dubbi e spiegazione approfondita. Alla fine: verifica, materiali di ripasso e punto di ripresa salvato.</p><div class="method-strip"><div class="method-step"><b>01 · Leggi</b><span>Un blocco coerente, al tuo ritmo.</span></div><div class="method-step"><b>02 · Confronta</b><span>Dubbi, alternative e compromessi.</span></div><div class="method-step"><b>03 · Verifica</b><span>Motiva e metti alla prova la scelta.</span></div><div class="method-step"><b>04 · Consolida</b><span>Appunti, mappe e flashcard.</span></div></div></section></div>` +
      `<div><section class="panel"><div class="empty-icon" aria-hidden="true">↳</div><h3>Da dove riprendiamo</h3><p>${esc(resume.next_action)}</p>${resume.source_id ? `<p>${external(resourceById.get(resume.source_id).url, esc(resourceById.get(resume.source_id).title))}${resume.section ? `<br>${esc(resume.section)}` : ''}</p>` : ''}<small>Aggiornato il ${formatDate(progress.updated_on)}</small></section><section class="panel"><div class="section-heading"><h3>Il tuo ripasso</h3><span class="tag">${materials.length}</span></div>${recentMaterials.length ? recentMaterials.map(m => `<p><a href="#materiale/${esc(m.id)}">${esc(m.title)} →</a><br><small>${esc(materialLabels[m.kind])} · ${esc(m.block_id)}</small></p>`).join('') : '<p>La raccolta cresce con le sessioni. Qui troverai ciò che abbiamo studiato e consolidato insieme.</p>'}<div class="material-links"><a href="#ripasso?kind=notes">Appunti →</a><a href="#ripasso?kind=map">Mappe →</a><a href="#ripasso?kind=flashcards">Flashcard →</a></div></section><section class="panel"><h3>${reviews.length ? 'Prossimi richiami' : 'Spazio ai dubbi'}</h3>${reviews.length ? `<ul class="timeline">${reviews.slice(0, 3).map(r => `<li><time>${formatDate(r.due_on)}${r.due_on < today() ? ' · Da recuperare' : ''}</time>${blockLink(r.block_id)} · ${esc(r.reason)}</li>`).join('')}</ul>` : `<p>${progress.doubts.length ? esc(progress.doubts.filter(d => !d.resolved_on).map(d => d.text).join(' · ')) || 'I dubbi registrati sono stati risolti.' : 'Nessun dubbio personale ancora registrato. Lo annoteremo durante la lettura, senza perdere il filo.'}</p>`}</section></div></div>`;
  }

  function renderPath() {
    main.innerHTML = heading('IL PERCORSO', 'Dai requisiti all’architettura.', '12 tappe progressive. La durata si adatta alle evidenze e al tempo della sessione.') +
      `<div class="callout">Le durate sono stime di studio, confronto e attività. Le fonti elencate sono riferimenti: la lettura precisa viene concordata all’inizio di ogni sessione.</div><div class="blocks">${blocks.map(b => `<a class="block-card ${b.id === progress.resume.block_id ? 'current' : ''}" href="#blocco/${b.id}"><div class="block-card-top"><span class="block-id">${b.id}</span>${blockStatus(b)}</div><h2>${esc(b.title)}</h2><p>${esc(b.outcome)}</p><div class="block-foot"><span>${esc(b.estimate)} · ${b.objective_ids.length ? `${b.objective_ids.length} obiettivi` : 'Diagnosi dei prerequisiti'}</span><span>${b.id === progress.resume.block_id ? 'Punto di ripresa ' : ''}→</span></div></a>`).join('')}</div>`;
  }

  function renderBlock(id) {
    const b = blockById.get(id);
    if (!b) return renderNotFound();
    const flags = progress.blocks[id] || {};
    const blockMaterials = materials.filter(m => m.block_id === id);
    const doubts = progress.doubts.filter(d => d.block_id === id && !d.resolved_on);
    main.innerHTML = `<a class="back-link" href="#percorso">← Tutto il percorso</a>` + heading(`${id} · ${b.estimate}`, b.title, b.outcome) +
      `<div class="block-states" aria-label="Stati personali del blocco">${Object.entries(stateLabels).map(([key, label]) => `<span class="state ${flags[key] ? 'done' : ''}">${flags[key] ? '✓' : '○'} ${label}${flags[key] ? ` · ${formatDate(flags[key].on, { month: 'short' })}` : ''}</span>`).join('')}</div>` +
      `<div class="detail-grid"><div>${id === progress.resume.block_id ? `<section class="panel"><p class="eyebrow">PUNTO DI RIPRESA</p><h2>La prossima azione</h2><p>${esc(progress.resume.next_action)}</p>${progress.resume.section ? `<p>Sezione: ${esc(progress.resume.section)}</p>` : ''}</section>` : ''}<section class="panel"><h2>Il blocco di studio</h2><p>${esc(b.theory)}</p><h3>Confronto e attività</h3><p>${esc(b.practice)}</p><h3>Che cosa verificare</h3><p>${esc(b.outcome)}</p></section><section aria-labelledby="sources-title"><div class="section-heading"><h2 id="sources-title">Fonti di riferimento</h2><span class="tag">${b.resource_ids.length}</span></div><p class="muted">Sceglieremo le sezioni da leggere in base al blocco e al tempo disponibile.</p><div class="resource-list">${b.resource_ids.map(rid => resourceCard(resourceById.get(rid))).join('')}</div></section></div><aside><section class="panel"><h2>Prima di questo blocco</h2>${b.prerequisites.length ? `<p>${b.prerequisites.map(pid => blockLink(pid, `${pid} · ${blockById.get(pid).title}`)).join('<br>')}</p><p>La diagnosi può confermare prerequisiti già acquisiti.</p>` : '<p>Partiamo dalle decisioni che affronti già sul lavoro. Nessuna competenza è ancora considerata verificata.</p>'}</section><section class="panel"><h2>Obiettivi AZ-305</h2>${b.objective_ids.length ? `<ul class="objectives">${b.objective_ids.map(oid => {
        const primary = resources.filter(r => r.objective_ids.includes(oid) && validPrimary(r));
        const training = resources.some(r => r.objective_ids.includes(oid) && r.role === 'training' && r.mapping_scope === 'direct' && r.review_current && isAccessible(r) && isFresh(r));
        const evidence = progress.objectives[oid] || {};
        return `<li><code>${esc(oid)}</code>${esc(objectiveLabel(oid))}<br><span class="tag ${evidence.verified ? 'green' : ''}">${evidence.verified ? 'Comprensione verificata' : 'Comprensione da verificare'}</span>${!primary.length ? '<br><span class="tag orange">Fonti da ricontrollare</span>' : ''}${!training ? '<br><span class="tag orange">Nessuna unità Learn dedicata</span>' : ''}<details><summary>Fonti ed evidenze</summary>${primary.map(r => `<p>${external(r.url, esc(r.title))}</p>`).join('') || '<p>Nessuna fonte primaria attualmente valida.</p>'}${Object.entries(stateLabels).filter(([state]) => evidence[state]).map(([state, label]) => `<p><strong>${label}</strong> · ${formatDate(evidence[state].on)}<br>${esc(evidence[state].evidence)}</p>`).join('') || '<p>Nessuna evidenza personale registrata.</p>'}</details></li>`;
      }).join('')}</ul>` : '<p>Diagnosi trasversale: non completa automaticamente obiettivi d’esame.</p>'}</section><section class="panel"><h2>Ripasso del blocco</h2>${blockMaterials.length ? blockMaterials.map(m => `<p><a href="#materiale/${esc(m.id)}">${esc(m.title)} →</a></p>`).join('') : '<p>Appunti, mappa e flashcard saranno sviluppati alla fine delle sessioni.</p>'}</section><section class="panel"><h2>Dubbi aperti</h2>${doubts.length ? `<ul class="notice-list">${doubts.map(d => `<li>${esc(d.text)}</li>`).join('')}</ul>` : '<p>Nessun dubbio aperto registrato per questo blocco.</p>'}</section></aside></div>`;
  }

  let libraryState = {};
  function libraryQuery() {
    return new URLSearchParams(location.hash.split('?')[1] || '');
  }
  function renderLibrary() {
    const params = libraryQuery();
    libraryState = { q: params.get('q') || '', domain: params.get('domain') || '', kind: params.get('kind') || '', page: Math.max(1, Number(params.get('page')) || 1) };
    main.innerHTML = heading('LA BIBLIOTECA', 'Le fonti, al posto giusto.', `${resources.length} risorse catalogate. Cerca un argomento o parti da un obiettivo.`) +
      `<div class="toolbar"><div class="field search"><label for="resource-search">Cerca nelle fonti</label><input id="resource-search" type="search" placeholder="SQL, identità, 3.1.2…" value="${esc(libraryState.q)}" autocomplete="off"></div><div class="field"><label for="domain-filter">Dominio</label><select id="domain-filter"><option value="">Tutti i domini</option>${baseline.domains.map(d => `<option value="${esc(d.id)}" ${libraryState.domain === d.id ? 'selected' : ''}>${esc(d.label_it)}</option>`).join('')}</select></div><div class="field"><label for="kind-filter">Tipo di risorsa</label><select id="kind-filter"><option value="">Tutti i tipi</option>${Object.entries(kindLabels).map(([key, label]) => `<option value="${esc(key)}" ${libraryState.kind === key ? 'selected' : ''}>${esc(label)}</option>`).join('')}<option value="placeholder" ${libraryState.kind === 'placeholder' ? 'selected' : ''}>Placeholder (senza caso)</option></select></div></div><p class="results-summary" id="library-summary" role="status"></p><div id="library-results"></div><div id="library-pagination"></div>`;
    document.getElementById('resource-search').addEventListener('input', event => { libraryState.q = event.target.value; libraryState.page = 1; updateLibrary(); });
    document.getElementById('domain-filter').addEventListener('change', event => { libraryState.domain = event.target.value; libraryState.page = 1; updateLibrary(); });
    document.getElementById('kind-filter').addEventListener('change', event => { libraryState.kind = event.target.value; libraryState.page = 1; updateLibrary(); });
    updateLibrary();
  }

  function updateLibrary(focus = false) {
    const normalize = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLocaleLowerCase('it');
    const terms = normalize(libraryState.q).split(/\s+/).filter(Boolean);
    const matches = resources.filter(r => {
      if (libraryState.kind === 'placeholder' ? r.status !== 'public_placeholder' : r.status === 'public_placeholder') return false;
      if (libraryState.kind && libraryState.kind !== 'placeholder' && r.kind !== libraryState.kind) return false;
      if (libraryState.domain && !r.objective_ids.some(id => id.startsWith(libraryState.domain + '.'))) return false;
      const text = normalize([r.id, r.title, r.selection_reason_it, ...r.objective_ids, ...r.objective_ids.map(objectiveLabel)].join(' '));
      return terms.every(term => text.includes(term));
    });
    const pageSize = 20;
    const totalPages = Math.max(1, Math.ceil(matches.length / pageSize));
    libraryState.page = Math.min(Math.floor(libraryState.page), totalPages);
    const start = (libraryState.page - 1) * pageSize;
    document.getElementById('library-summary').textContent = `${matches.length} risorse trovate${matches.length ? ` · ${start + 1}–${Math.min(start + pageSize, matches.length)}` : ''}. I placeholder sono esclusi, salvo selezione esplicita.`;
    document.getElementById('library-results').innerHTML = matches.length ? `<div class="library-grid">${matches.slice(start, start + pageSize).map(r => resourceCard(r)).join('')}</div>` : empty('Nessuna fonte trovata', 'Prova un altro termine o seleziona tutti i domini e tutti i tipi.');
    document.getElementById('library-pagination').innerHTML = totalPages > 1 ? `<div class="pagination"><button class="button secondary small" id="previous-page" ${libraryState.page === 1 ? 'disabled' : ''}>← Precedente</button><span>Pagina ${libraryState.page} di ${totalPages}</span><button class="button secondary small" id="next-page" ${libraryState.page === totalPages ? 'disabled' : ''}>Successiva →</button></div>` : '';
    document.getElementById('previous-page')?.addEventListener('click', () => { libraryState.page--; updateLibrary(true); });
    document.getElementById('next-page')?.addEventListener('click', () => { libraryState.page++; updateLibrary(true); });
    const params = new URLSearchParams();
    for (const [key, value] of Object.entries(libraryState)) if (value && !(key === 'page' && value === 1)) params.set(key, value);
    history.replaceState(null, '', '#biblioteca' + (params.size ? '?' + params : ''));
    if (focus) {
      const summary = document.getElementById('library-summary');
      summary.setAttribute('tabindex', '-1'); summary.focus(); summary.scrollIntoView({ block: 'start' });
    }
  }

  function renderReview() {
    const params = libraryQuery();
    let kind = params.get('kind') || '';
    if (!materialLabels[kind]) kind = '';
    let block = params.get('block') || '';
    main.innerHTML = heading('IL RIPASSO', 'Le idee da ritrovare.', 'Appunti, mappe e flashcard sviluppati a partire dalle sessioni svolte.') +
      `<div class="tabs" aria-label="Tipo di materiale"><button type="button" data-kind="" aria-pressed="${!kind}">Tutti</button>${Object.entries(materialLabels).map(([key, label]) => `<button type="button" data-kind="${key}" aria-pressed="${kind === key}">${label}</button>`).join('')}</div><div class="toolbar"><div class="field"><label for="block-filter">Blocco di studio</label><select id="block-filter"><option value="">Tutti i blocchi</option>${blocks.map(b => `<option value="${b.id}" ${block === b.id ? 'selected' : ''}>${esc(b.id + ' · ' + b.title)}</option>`).join('')}</select></div></div><div id="review-results" aria-live="polite"></div>`;
    function update() {
      const items = materials.filter(m => (!kind || m.kind === kind) && (!block || m.block_id === block)).sort((a, b) => b.published_on.localeCompare(a.published_on));
      document.getElementById('review-results').innerHTML = items.length ? `<div class="blocks">${items.map(m => `<article class="material-card"><span class="tag">${esc(materialLabels[m.kind])} · ${esc(m.block_id)}</span><h2><a href="#materiale/${esc(m.id)}">${esc(m.title)} →</a></h2><p>${esc(m.summary || '')}</p><small>Pubblicato il ${formatDate(m.published_on)}${m.kind === 'flashcards' ? ` · ${m.cards.length} carte` : ''}</small></article>`).join('')}</div>` : empty('Il ripasso comincia dallo studio.', 'Non ci sono ancora materiali pubblicati per questa selezione. Alla fine delle sessioni aggiungeremo appunti approfonditi, mappe e flashcard.', '<a class="button secondary" href="#percorso">Vai al percorso →</a>');
      const query = new URLSearchParams();
      if (kind) query.set('kind', kind);
      if (block) query.set('block', block);
      history.replaceState(null, '', '#ripasso' + (query.size ? '?' + query : ''));
      document.querySelectorAll('[data-kind]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.kind === kind)));
    }
    document.querySelectorAll('[data-kind]').forEach(button => button.addEventListener('click', () => { kind = button.dataset.kind; update(); }));
    document.getElementById('block-filter').addEventListener('change', event => { block = event.target.value; update(); });
    update();
  }

  function renderMaterial(id) {
    const m = materials.find(item => item.id === id);
    if (!m) return renderNotFound();
    main.innerHTML = `<a class="back-link" href="#ripasso">← Materiali di ripasso</a>` + heading(`${materialLabels[m.kind]} · ${m.block_id}`, m.title, `Pubblicato il ${formatDate(m.published_on)}`) + (m.kind === 'flashcards' ? '<div id="flashcard-container"></div>' : `<article class="article">${m.html}</article>`);
    if (m.kind !== 'flashcards') return;
    let index = 0;
    function show() {
      const card = m.cards[index];
      document.getElementById('flashcard-container').innerHTML = `<article class="flashcard"><p class="eyebrow">CARTA ${index + 1} DI ${m.cards.length}</p><h2 id="card-question">${esc(card.question)}</h2><button class="button" id="reveal-answer" aria-expanded="false" aria-controls="card-answer">Mostra la risposta</button><div class="answer" id="card-answer" hidden>${esc(card.answer)}</div></article><div class="pagination"><button class="button secondary" id="card-prev" ${index === 0 ? 'disabled' : ''}>← Precedente</button><span>${index + 1} / ${m.cards.length}</span><button class="button secondary" id="card-next" ${index === m.cards.length - 1 ? 'disabled' : ''}>Successiva →</button></div>`;
      document.getElementById('reveal-answer').addEventListener('click', event => {
        const answer = document.getElementById('card-answer'); answer.hidden = !answer.hidden;
        event.target.setAttribute('aria-expanded', String(!answer.hidden));
        event.target.textContent = answer.hidden ? 'Mostra la risposta' : 'Nascondi la risposta';
      });
      document.getElementById('card-prev').addEventListener('click', () => { if (index > 0) { index--; show(); focusQuestion(); } });
      document.getElementById('card-next').addEventListener('click', () => { if (index < m.cards.length - 1) { index++; show(); focusQuestion(); } });
    }
    function focusQuestion() { const title = document.getElementById('card-question'); title.tabIndex = -1; title.focus(); }
    show();
  }

  function renderNotFound() {
    main.innerHTML = heading('STUDY HUB', 'Questa pagina non c’è.', 'Il collegamento potrebbe riferirsi a un blocco o a un materiale non pubblicato.') + '<a class="button" href="#home">Torna alla panoramica →</a>';
  }

  function render(moveFocus = true) {
    let route;
    try { route = decodeURIComponent(location.hash.slice(1).split('?')[0]) || 'home'; }
    catch { route = 'not-found'; }
    const [view, id] = route.split('/');
    const nav = view === 'blocco' ? 'percorso' : view === 'materiale' ? 'ripasso' : view;
    document.querySelectorAll('[data-nav]').forEach(link => {
      link.classList.toggle('active', link.dataset.nav === nav);
      if (link.dataset.nav === nav) link.setAttribute('aria-current', 'page'); else link.removeAttribute('aria-current');
    });
    if (view === 'home') renderHome();
    else if (view === 'percorso') renderPath();
    else if (view === 'blocco') renderBlock(id);
    else if (view === 'biblioteca') renderLibrary();
    else if (view === 'ripasso') renderReview();
    else if (view === 'materiale') renderMaterial(id);
    else renderNotFound();
    document.title = `${main.querySelector('h1')?.textContent || 'Study Hub'} · AZ-305`;
    if (moveFocus) { main.focus({ preventScroll: true }); window.scrollTo(0, 0); }
  }
  window.addEventListener('hashchange', () => render());
  document.querySelector('.skip-link').addEventListener('click', event => { event.preventDefault(); main.focus(); });
  // Refresh date-sensitive source eligibility when returning to a long-open tab.
  document.addEventListener('visibilitychange', () => { if (!document.hidden) render(false); });
  render(false);
})();
