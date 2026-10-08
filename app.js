(() => {
  'use strict';

  const strings = {
    en: {
      eyebrow: 'THE CHARACTER LIBRARY', heroTitle: 'A little company<br>for your desktop<span class="accent">.</span>', heroCopy: 'Explore Coding Cat, a downloadable MIT-licensed PNG pack, and Arin, a public research profile and source with no official installable pack release.', submit: 'Submit on GitHub', browseSource: 'Browse repository', collectionLabel: 'EXPLORE THE COLLECTION', collectionTitle: 'Meet the characters', collectionNote: 'Made to live alongside your work.', searchLabel: 'Search characters', searchPlaceholder: 'Search names, tags, descriptions…', sortLabel: 'Sort characters', all: 'All', recent: 'Newest first', alphabetic: 'A to Z', loading: 'Loading characters…', footer: 'Coding Cat PNG pack and Arin research profile and source; no official Arin pack release.', themeLight: 'Switch to light theme', themeDark: 'Switch to dark theme', rendererFilter: 'Character type filter', collectionAria: 'Character collection', variant: 'Look', creator: 'By', details: 'View details', download: 'Download pack', packDetails: 'Pack details', version: 'Version', renderer: 'Renderer', fileSize: 'Archive size', checksum: 'SHA-256', copy: 'Copy SHA-256', copied: 'Copied!', copyFailed: 'Select the checksum to copy it.', license: 'License', sourceTerms: 'Source terms', importTitle: 'Bring them home', importSteps: ['Download the .herdrchar archive (do not unzip it).', 'In Herdr Desktop Pet, open the menu bar settings → Character → Add Character… and choose the downloaded archive.', 'Select the imported character in the Character tab. Importing alone does not activate it.'], noResults: 'No characters match your search. Try another name or filter.', loadError: 'Could not load the collection. Check your connection or refresh this page.', retry: 'Try again', showing: (n) => `${n} ${n === 1 ? 'character' : 'characters'}`, close: 'Close details', imageAlt: (name, look) => `${name} — ${look} preview`, source: 'Source repository', format: (type) => type === 'rig' ? 'Rig' : 'PNG',
      research: 'Research', researchDetails: 'Research profile', researchPreview: 'Profile preview · No official pack release', researchSource: 'Research source', researchImageAlt: (name) => `${name} — research profile preview`
    },
    ko: {
      eyebrow: '캐릭터 라이브러리', heroTitle: '책상 위의 작은 동료<span class="accent">.</span>', heroCopy: '다운로드 가능한 MIT 라이선스 PNG 팩 Coding Cat과 공개 연구 프로필·소스인 아린을 둘러보세요. 아린의 공식 설치형 팩은 출시되지 않았습니다.', submit: 'GitHub에서 제출하기', browseSource: '저장소 둘러보기', collectionLabel: '컬렉션 둘러보기', collectionTitle: '캐릭터 만나기', collectionNote: '작업하는 동안 곁을 지키는 친구들.', searchLabel: '캐릭터 검색', searchPlaceholder: '이름, 태그, 설명 검색…', sortLabel: '캐릭터 정렬', all: '전체', recent: '최신순', alphabetic: '이름순', loading: '캐릭터를 불러오는 중…', footer: 'Coding Cat PNG 팩과 아린 연구 프로필·소스 공개. 아린 공식 팩은 없습니다.', themeLight: '밝은 테마로 전환', themeDark: '어두운 테마로 전환', rendererFilter: '캐릭터 유형 필터', collectionAria: '캐릭터 컬렉션', variant: '의상', creator: '제작', details: '상세 보기', download: '팩 다운로드', packDetails: '팩 정보', version: '버전', renderer: '렌더러', fileSize: '압축 파일 크기', checksum: 'SHA-256', copy: 'SHA-256 복사', copied: '복사됨!', copyFailed: '체크섬을 선택해 복사해 주세요.', license: '라이선스', sourceTerms: '원본 이용 조건', importTitle: '캐릭터 가져오기', importSteps: ['.herdrchar 압축 파일을 다운로드하세요 (압축 해제하지 마세요).', 'Herdr Desktop Pet 메뉴 막대 설정 → 캐릭터 → 캐릭터 추가…에서 다운로드한 파일을 선택하세요.', '캐릭터 탭에서 가져온 캐릭터를 선택하세요. 가져오기만으로는 활성화되지 않습니다.'], noResults: '검색 결과가 없습니다. 검색어나 필터를 바꿔 보세요.', loadError: '컬렉션을 불러올 수 없습니다. 연결 상태를 확인하거나 새로고침해 주세요.', retry: '다시 시도', showing: (n) => `캐릭터 ${n}개`, close: '상세 정보 닫기', imageAlt: (name, look) => `${name} — ${look} 미리보기`, source: '소스 저장소', format: (type) => type === 'rig' ? '리그' : 'PNG',
      research: '연구', researchDetails: '연구 프로필', researchPreview: '프로필 미리보기 · 공식 팩 출시 없음', researchSource: '연구 소스', researchImageAlt: (name) => `${name} — 연구 프로필 미리보기`
    }
  };

  const $ = (selector) => document.querySelector(selector);
  const cards = $('#cards');
  const status = $('#status');
  const dialog = $('#details');
  const search = $('#search');
  const catalogURL = new URL('./catalog.json', location.href);
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
  const systemDark = matchMedia('(prefers-color-scheme: dark)');
  const state = { catalog: null, loadStatus: 'loading', resultCount: 0, lang: preference('herdr-gallery-language') === 'ko' ? 'ko' : 'en', theme: preference('herdr-gallery-theme'), filter: 'all', sort: 'recent', selected: new Map(), animations: new Set(), activeDetail: null, opener: null };
  if (state.theme !== 'light' && state.theme !== 'dark') state.theme = systemDark.matches ? 'dark' : 'light';

  function preference(key) { try { return localStorage.getItem(key); } catch { return null; } }
  function savePreference(key, value) { try { localStorage.setItem(key, value); } catch { /* Storage may be unavailable in private browsing. */ } }
  function t(key) { return strings[state.lang][key]; }
  function node(tag, className, text) {
    const element = document.createElement(tag);
    if (className) element.className = className;
    if (text !== undefined) element.textContent = text;
    return element;
  }
  function safeURL(value, base = catalogURL) {
    if (typeof value !== 'string' || !value.trim()) return null;
    try {
      const url = new URL(value, base);
      return url.protocol === 'https:' || url.protocol === 'http:' ? url.href : null;
    } catch { return null; }
  }
  function localized(value) { return value?.[state.lang] || value?.en || ''; }
  function bytes(value) {
    if (!Number.isFinite(value) || value < 0) return '—';
    return new Intl.NumberFormat(state.lang === 'ko' ? 'ko-KR' : 'en-US', { maximumFractionDigits: 1 }).format(value / 1048576) + ' MB';
  }
  function link(text, href, className) {
    const a = node('a', className, text);
    a.href = href;
    if (new URL(href).origin !== location.origin) { a.target = '_blank'; a.rel = 'noopener noreferrer'; }
    return a;
  }
  function selectedVariant(character) {
    const available = character.variants.filter((variant) => state.filter === 'all' || variant.renderMode === state.filter);
    const selected = state.selected.get(character.id);
    return available.find((variant) => variant.id === selected) || available[0];
  }
  function latestDate(character) {
    return character.type === 'research'
      ? Date.parse(character.publishedAt) || 0
      : Math.max(...character.variants.map((variant) => Date.parse(variant.publishedAt) || 0));
  }
  function matches(character) {
    if (character.type === 'research') {
      if (state.filter !== 'all' && state.filter !== 'research') return false;
    } else if (character.type === 'pack') {
      if (!character.variants.some((variant) => state.filter === 'all' || variant.renderMode === state.filter)) return false;
    } else return false;
    const query = search.value.trim().toLocaleLowerCase();
    if (!query) return true;
    const names = character.type === 'pack' ? character.variants.flatMap((variant) => [variant.name?.en, variant.name?.ko]) : [];
    const haystack = [character.name, character.author, character.description?.en, character.description?.ko, ...(character.tags || []), ...names].join(' ').toLocaleLowerCase();
    return haystack.includes(query);
  }
  function stopAnimations() {
    for (const stop of state.animations) stop();
    state.animations.clear();
  }
  function animatePreview(image, variant) {
    const idle = safeURL(variant.preview?.idle);
    const frames = (variant.preview?.running || []).map((path) => safeURL(path)).filter(Boolean);
    image.src = idle || '';
    if (!frames.length) return;
    let timer;
    let frame = 0;
    const stop = () => { clearInterval(timer); timer = undefined; image.src = idle || ''; state.animations.delete(stop); };
    const start = () => {
      if (reducedMotion.matches || timer) return;
      frame = 0;
      image.src = frames[frame];
      timer = setInterval(() => { frame = (frame + 1) % frames.length; image.src = frames[frame]; }, 170);
      state.animations.add(stop);
    };
    image.addEventListener('pointerenter', start);
    image.addEventListener('pointerleave', stop);
    image.addEventListener('pointercancel', stop);
    image.addEventListener('blur', stop);
  }
  function card(character) {
    const variant = character.type === 'pack' ? selectedVariant(character) : null;
    const article = node('article', 'character-card');
    const visual = node('div', 'card-visual');
    const image = node('img', 'card-preview');
    image.alt = variant ? t('imageAlt')(character.name, localized(variant.name)) : t('researchImageAlt')(character.name);
    image.loading = 'lazy';
    image.decoding = 'async';
    if (variant) animatePreview(image, variant);
    else image.src = safeURL(character.profile) || '';
    visual.append(image);
    visual.append(node('span', 'format-chip', variant ? t('format')(variant.renderMode) : t('research')));
    article.append(visual);
    const content = node('div', 'card-content');
    const heading = node('div', 'card-heading');
    heading.append(node('h3', '', character.name), node('span', 'creator', `${t('creator')} ${character.author}`));
    content.append(heading, node('p', 'card-description', localized(character.description)));
    if (character.tags?.length) {
      const tags = node('div', 'tag-list');
      for (const tag of character.tags) tags.append(node('span', 'tag', tag));
      content.append(tags);
    }
    if (!variant) {
      content.append(node('p', 'single-variant', t('researchPreview')));
    } else if (character.variants.length > 1) {
      const label = node('label', 'variant-label');
      label.append(node('span', '', t('variant')));
      const select = node('select', 'variant-select');
      select.dataset.character = character.id;
      for (const choice of character.variants) {
        if (state.filter !== 'all' && choice.renderMode !== state.filter) continue;
        const option = node('option', '', localized(choice.name));
        option.value = choice.id;
        option.selected = choice.id === variant.id;
        select.append(option);
      }
      select.addEventListener('change', () => {
        state.selected.set(character.id, select.value);
        const focusId = character.id;
        renderCards();
        for (const element of cards.querySelectorAll('.variant-select')) if (element.dataset.character === focusId) element.focus();
      });
      label.append(select);
      content.append(label);
    } else {
      content.append(node('p', 'single-variant', localized(variant.name)));
    }
    const actions = node('div', 'card-actions');
    const details = node('button', 'button button-outline', t('details'));
    details.type = 'button';
    details.dataset.character = character.id;
    details.addEventListener('click', () => showDetails(character, character.type === 'pack' ? selectedVariant(character) : null, details));
    actions.append(details);
    if (variant) {
      const archive = safeURL(variant.download?.path);
      if (archive) { const download = link(t('download') + ' ↓', archive, 'button button-dark'); download.setAttribute('download', ''); actions.append(download); }
    } else {
      const source = safeURL(character.sourceUrl);
      if (source) actions.append(link(t('researchSource') + ' ↗', source, 'button button-dark'));
    }
    content.append(actions);
    article.append(content);
    return article;
  }
  function updateStatus() {
    status.hidden = state.loadStatus === 'success' && state.resultCount > 0;
    if (state.loadStatus === 'loading') {
      status.textContent = t('loading');
    } else if (state.loadStatus === 'error') {
      const retry = node('button', 'button button-outline', t('retry'));
      retry.type = 'button';
      retry.addEventListener('click', load);
      status.replaceChildren(node('p', '', t('loadError')), retry);
    } else {
      status.textContent = state.resultCount ? '' : t('noResults');
    }
  }
  function renderCards() {
    stopAnimations();
    if (!state.catalog) return;
    const list = state.catalog.characters.filter(matches);
    list.sort(state.sort === 'alphabetic'
      ? (a, b) => a.name.localeCompare(b.name, state.lang)
      : (a, b) => latestDate(b) - latestDate(a) || a.name.localeCompare(b.name, state.lang));
    cards.replaceChildren(...list.map(card));
    state.resultCount = list.length;
    $('#results-label').textContent = t('showing')(list.length);
    updateStatus();
  }
  function detailRow(container, title, value) {
    const row = node('div', 'spec-row');
    row.append(node('dt', '', title), node('dd', '', value));
    container.append(row);
  }
  function showDetails(character, variant, opener) {
    state.opener = opener;
    state.activeDetail = { character, variant };
    const top = node('div', 'detail-top');
    const imageBox = node('div', 'detail-image');
    const image = node('img');
    image.src = character.type === 'research' ? safeURL(character.profile) || '' : safeURL(variant.preview?.idle) || '';
    image.alt = character.type === 'research' ? t('researchImageAlt')(character.name) : t('imageAlt')(character.name, localized(variant.name));
    imageBox.append(image);
    const intro = node('div', 'detail-intro');
    const title = node('h2', '', character.name);
    title.id = 'detail-title';
    intro.append(node('p', 'eyebrow', t(character.type === 'research' ? 'researchDetails' : 'packDetails')), title,
      node('p', 'detail-look', character.type === 'research' ? t('researchPreview') : localized(variant.name)),
      node('p', 'detail-author', `${t('creator')} ${character.author}`));
    top.append(imageBox, intro);
    const info = node('div', 'detail-info');
    if (character.type === 'research') {
      info.append(node('p', 'card-description', localized(character.description)));
      const resources = node('div', 'detail-resources');
      const license = safeURL(character.license?.path);
      if (license) resources.append(link(`${t('license')}: ${character.license.label} ↗`, license, 'resource-link'));
      const sourceTerms = safeURL(character.sourceTerms);
      if (sourceTerms) resources.append(link(`${t('sourceTerms')} ↗`, sourceTerms, 'resource-link'));
      const source = safeURL(character.sourceUrl);
      if (source) resources.append(link(`${t('researchSource')} ↗`, source, 'resource-link'));
      info.append(resources);
      $('#detail-body').replaceChildren(top, info);
      if (!dialog.open) dialog.showModal();
      $('#close-details').focus();
      return;
    }
    const specs = node('dl', 'spec-list');
    detailRow(specs, t('version'), variant.version);
    detailRow(specs, t('renderer'), t('format')(variant.renderMode));
    detailRow(specs, t('fileSize'), bytes(variant.download?.bytes));
    info.append(specs);
    const checksum = node('div', 'checksum');
    checksum.append(node('span', 'spec-label', t('checksum')));
    const hashLine = node('div', 'hash-line');
    const hash = node('input', 'hash-value');
    hash.type = 'text';
    hash.readOnly = true;
    hash.value = variant.download?.sha256 || '';
    hash.setAttribute('aria-label', t('checksum'));
    const copy = node('button', 'button button-outline copy-button', t('copy'));
    copy.type = 'button';
    copy.addEventListener('click', async () => {
      try {
        if (navigator.clipboard?.writeText) await navigator.clipboard.writeText(hash.value);
        else { hash.select(); if (!document.execCommand('copy')) throw new Error('Copy unavailable'); }
        copy.textContent = t('copied');
      } catch { hash.focus(); hash.select(); copy.textContent = t('copyFailed'); }
    });
    hashLine.append(hash, copy);
    checksum.append(hashLine);
    info.append(checksum);
    const resources = node('div', 'detail-resources');
    const license = safeURL(variant.license?.path);
    if (license) resources.append(link(`${t('license')}: ${variant.license.label} ↗`, license, 'resource-link'));
    const sourceTerms = safeURL(variant.sourceTerms);
    if (sourceTerms) resources.append(link(`${t('sourceTerms')} ↗`, sourceTerms, 'resource-link'));
    else if (variant.sourceTerms) resources.append(node('p', 'source-terms', `${t('sourceTerms')}: ${variant.sourceTerms}`));
    const repository = safeURL(state.catalog.repositoryUrl);
    if (repository) resources.append(link(`${t('source')} ↗`, repository, 'resource-link'));
    info.append(resources);
    const instructions = node('div', 'instructions');
    instructions.append(node('h3', '', t('importTitle')));
    const steps = node('ol');
    for (const step of t('importSteps')) steps.append(node('li', '', step));
    instructions.append(steps);
    info.append(instructions);
    const archive = safeURL(variant.download?.path);
    if (archive) { const download = link(t('download') + ' ↓', archive, 'button button-primary detail-download'); download.setAttribute('download', ''); info.append(download); }
    $('#detail-body').replaceChildren(top, info);
    if (!dialog.open) dialog.showModal();
    $('#close-details').focus();
  }
  function translate() {
    document.documentElement.lang = state.lang;
    for (const element of document.querySelectorAll('[data-i18n]')) {
      if (element === status) continue;
      if (element.dataset.i18n === 'heroTitle') {
        // This string is authored locally, never read from catalog data.
        element.innerHTML = t('heroTitle');
      } else element.textContent = t(element.dataset.i18n);
    }
    search.placeholder = t('searchPlaceholder');
    $('.filters').setAttribute('aria-label', t('rendererFilter'));
    cards.setAttribute('aria-label', t('collectionAria'));
    $('#close-details').setAttribute('aria-label', t('close'));
    for (const button of document.querySelectorAll('[data-lang]')) button.setAttribute('aria-pressed', String(button.dataset.lang === state.lang));
    updateTheme();
    if (state.loadStatus === 'success') renderCards();
    else updateStatus();
    if (dialog.open && state.activeDetail) showDetails(state.activeDetail.character, state.activeDetail.variant, state.opener);
  }
  function updateTheme() {
    document.documentElement.dataset.theme = state.theme;
    const label = t(state.theme === 'dark' ? 'themeLight' : 'themeDark');
    $('#theme-toggle').setAttribute('aria-label', label);
    $('#theme-toggle').title = label;
    $('#theme-icon').textContent = state.theme === 'dark' ? '☀' : '☾';
  }
  async function load() {
    state.loadStatus = 'loading';
    state.catalog = null;
    for (const id of ['submit-link', 'repository-link']) document.getElementById(id).hidden = true;
    updateStatus();
    try {
      const response = await fetch(catalogURL);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const catalog = await response.json();
      if (catalog.schemaVersion !== 1 || !Array.isArray(catalog.characters)) throw new Error('Unsupported catalog');
      state.catalog = catalog;
      state.loadStatus = 'success';
      renderCards();
      for (const [id, key] of [['submit-link', 'submissionUrl'], ['repository-link', 'repositoryUrl']]) {
        const url = safeURL(catalog[key]);
        if (url) { const anchor = document.getElementById(id); anchor.href = url; anchor.hidden = false; }
      }
    } catch (error) {
      state.catalog = null;
      state.loadStatus = 'error';
      stopAnimations();
      cards.replaceChildren();
      for (const id of ['submit-link', 'repository-link']) document.getElementById(id).hidden = true;
      updateStatus();
    }
  }

  for (const button of document.querySelectorAll('[data-lang]')) button.addEventListener('click', () => {
    state.lang = button.dataset.lang;
    savePreference('herdr-gallery-language', state.lang);
    translate();
  });
  $('#theme-toggle').addEventListener('click', () => { state.theme = state.theme === 'dark' ? 'light' : 'dark'; savePreference('herdr-gallery-theme', state.theme); updateTheme(); });
  systemDark.addEventListener('change', (event) => { if (!preference('herdr-gallery-theme')) { state.theme = event.matches ? 'dark' : 'light'; updateTheme(); } });
  reducedMotion.addEventListener('change', () => { if (reducedMotion.matches) stopAnimations(); });
  for (const button of document.querySelectorAll('[data-filter]')) button.addEventListener('click', () => {
    state.filter = button.dataset.filter;
    for (const choice of document.querySelectorAll('[data-filter]')) choice.setAttribute('aria-pressed', String(choice === button));
    renderCards();
  });
  search.addEventListener('input', renderCards);
  $('#sort').addEventListener('change', (event) => { state.sort = event.target.value; renderCards(); });
  $('#close-details').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', (event) => { if (event.target === dialog) dialog.close(); });
  dialog.addEventListener('close', () => {
    const opener = state.opener?.isConnected ? state.opener
      : [...cards.querySelectorAll('.card-actions button[data-character]')].find((button) => button.dataset.character === state.activeDetail?.character.id);
    (opener || search).focus();
    state.activeDetail = null;
    state.opener = null;
  });
  translate();
  load();
})();
