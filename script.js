/* INFOBYTE MASTER CONTENT HUB - DYNAMIC BATCH */

let newsData = [];
let phrasesData = [];
let quizzesData = [];
let currentView = 'news';
let activeIndex = -1;

async function loadData() {
    try {
        const newsResponse = await fetch('posts_content.json?t=' + Date.now());
        const newsJson = await newsResponse.json();
        newsData = newsJson.posts || [];
        document.getElementById('timestamp').innerText = `🕒 ACTUALIZADO: ${newsJson.generated_at || 'Hoy'}`;
    } catch (e) {
        console.warn("No se pudo cargar posts_content.json:", e);
        document.getElementById('timestamp').innerText = "⚠️ Noticias no disponibles";
    }

    try {
        const phrasesResponse = await fetch('frases_content.json?t=' + Date.now());
        const phrasesJson = await phrasesResponse.json();
        phrasesData = phrasesJson.phrases || [];
    } catch (e) {
        console.warn("No se pudo cargar frases_content.json:", e);
    }

    try {
        const quizResponse = await fetch('quizzes_content.json?t=' + Date.now());
        const quizJson = await quizResponse.json();
        quizzesData = quizJson.quizzes || [];
    } catch (e) {
        console.warn("No se pudo cargar quizzes_content.json:", e);
    }

    renderContent();
}

function renderContent() {
    const grid = document.getElementById('newsGrid');
    if (!grid) return;
    grid.innerHTML = '';
    
    let data = [];
    if (currentView === 'news') data = newsData;
    else if (currentView === 'phrases') data = phrasesData;
    else if (currentView === 'quizzes') data = quizzesData;

    data.forEach((item, index) => {
        const card = document.createElement('div');
        card.className = 'news-card';
        const displayId = item.id || (index + 1);
        
        if(currentView === 'news') {
            const imgHtml = item.image_path ? `<div class="card-img-container"><img src="${item.image_path}" class="card-img" alt="AI Generated Image"></div>` : '';
            card.innerHTML = `
                ${imgHtml}
                <div class="category-tag">#${displayId} | ${item.category || 'Noticia'}</div>
                <h3 class="card-title">${item.title || 'Sin Título'}</h3>
                <p style="font-size: 0.8em; color: #aaa; margin-bottom: 10px;">${item.image_text_hook || ''}</p>
                <div class="btn-group">
                    <button class="btn btn-read" onclick="openModal(${index})">📖 Leer Noticia (Bilingüe)</button>
                    <button class="btn btn-copy-en" onclick="copyEN(${index})">📋 Copiar Post (EN)</button>
                    <button class="btn btn-prompt" onclick="copyPrompt(${index})">🖼️ Prompt LUXURY</button>
                </div>`;
        } else if(currentView === 'quizzes') {
            card.innerHTML = `
                <div class="category-tag">#${displayId} | VIRAL QUIZ</div>
                <h3 class="card-title">${item.headline || 'Quiz Topic'}</h3>
                <p style="font-size: 0.8em; color: #aaa; margin-bottom: 10px;">${item.hook_question || ''}</p>
                <div class="btn-group">
                    <button class="btn btn-read" onclick="openModal(${index})">📖 Leer Reto (Bilingüe)</button>
                    <button class="btn btn-copy-en" onclick="copyQuizEN(${index})">📋 Copiar Post (EN)</button>
                    <button class="btn btn-prompt" onclick="copyQuizPrompt(${index})" style="background: #ff9800;">🖼️ Prompt QUIZ</button>
                </div>`;
        } else {
            card.innerHTML = `
                <div class="category-tag">#${displayId} | Apuntes del Alma</div>
                <h3 class="card-title" style="font-style: italic; font-size: 1em;">${(item.hook_text || '').split('\n')[0]}</h3>
                <div class="btn-group">
                    <button class="btn btn-read" onclick="openModal(${index})">📖 Leer Post (Bilingüe)</button>
                    <button class="btn btn-copy-en" onclick="copyPhraseEN(${index})">📋 Copiar Post (EN)</button>
                    <button class="btn btn-prompt" onclick="copyPhrasePrompt(${index})" style="background: #9c27b0;">🖼️ Prompt MINIMALISTA</button>
                </div>`;
        }
        grid.appendChild(card);
    });
}

function switchTab(view) {
    currentView = view;
    document.getElementById('tabNews').classList.toggle('active', view === 'news');
    document.getElementById('tabPhrases').classList.toggle('active', view === 'phrases');
    document.getElementById('tabQuizzes').classList.toggle('active', view === 'quizzes');
    
    let title = "Infobyte News Dashboard";
    if (view === 'phrases') title = "Apuntes del Alma";
    if (view === 'quizzes') title = "Viral Quizzes & Engagement";
    
    document.querySelector('.section-title').innerText = title;
    renderContent();
}

function openModal(index) {
    activeIndex = index;
    let data = [];
    if (currentView === 'news') data = newsData;
    else if (currentView === 'phrases') data = phrasesData;
    else if (currentView === 'quizzes') data = quizzesData;
    
    const item = data[index];
    const displayId = item.id || (index + 1);
    
    document.getElementById('modalCategory').innerText = `#${displayId} | ` + (item.category || item.topic || 'Infobyte Content');
    document.getElementById('modalTitle').innerText = item.title || item.headline || '';
    
    let bodyHTML = '';
    if (item.image_path) {
        bodyHTML += `<div style="text-align:center; margin-bottom:20px;"><img src="${item.image_path}" style="max-width:100%; border-radius:8px; box-shadow:0 10px 30px rgba(0,0,0,0.5);"></div>`;
    }
    
    let typeLabel = "CONTENIDO";
    if (currentView === 'quizzes') typeLabel = "RETO VIRAL";
    if (currentView === 'phrases') typeLabel = "POST ESPIRITUAL";

    // Formatear Post EN
    let postEN_Text = "";
    if (typeof item.postEN === 'object' && item.postEN !== null) {
        postEN_Text = (item.postEN.post_title || item.postEN.title || '') + '\n\n' + 
                      (item.postEN.post_body || item.postEN.body || '') + '\n\n' + 
                      (Array.isArray(item.postEN.hashtags) ? item.postEN.hashtags.join(' ') : item.postEN.hashtags || '');
    } else {
        postEN_Text = (item.postEN || '');
    }

    // Formatear Post ES
    let postES_Text = "";
    if (typeof item.postES === 'object' && item.postES !== null) {
        postES_Text = (item.postES.post_title || item.postES.title || '') + '\n\n' + 
                      (item.postES.post_body || item.postES.body || '') + '\n\n' + 
                      (item.postES.hashtags || '');
    } else {
        postES_Text = (item.postES || '');
    }

    bodyHTML += `<div style="display: flex; gap: 20px; text-align: left;">`;
    
    // Columna Inglés
    bodyHTML += `<div style="flex: 1; background:#1a1a2e; border-left:3px solid #00f2fe; padding:15px; border-radius:4px; max-height: 50vh; overflow-y: auto;">`;
    bodyHTML += `<small style="color:#00f2fe; font-weight:bold; display:block; margin-bottom:10px;">🇺🇸 ${typeLabel} (English)</small>`;
    bodyHTML += `<span style="color:#ccc; line-height: 1.6; display: block; white-space: pre-wrap;">${postEN_Text}</span></div>`;

    // Columna Español
    bodyHTML += `<div style="flex: 1; background:#1a1a2e; border-left:3px solid #2e7d32; padding:15px; border-radius:4px; max-height: 50vh; overflow-y: auto;">`;
    bodyHTML += `<small style="color:#2e7d32; font-weight:bold; display:block; margin-bottom:10px;">🇪🇸 ${typeLabel} (Español)</small>`;
    bodyHTML += `<span style="color:#ccc; line-height: 1.6; display: block; white-space: pre-wrap;">${postES_Text}</span></div>`;

    bodyHTML += `</div>`;
    
    document.getElementById('modalBody').innerHTML = bodyHTML;
    document.getElementById('modalOverlay').classList.add('active');
}

function closeModal() { document.getElementById('modalOverlay').classList.remove('active'); }

function copyEN(index) { 
    const item = newsData[index];
    const postEN = typeof item.postEN === 'object' 
        ? `${item.postEN.post_title||item.postEN.title||''}\n\n${item.postEN.post_body||item.postEN.body||''}\n\n${item.postEN.post_question||item.postEN.question||''}\n\n${item.postEN.post_authority||item.postEN.authority||''}\n\n${Array.isArray(item.postEN.hashtags) ? item.postEN.hashtags.join(' ') : item.postEN.hashtags||''}`
        : (item.postEN || item.postES || '');
    navigator.clipboard.writeText(postEN); 
    showToast("✅ English post copied!"); 
}

function copyES(index) { 
    const item = newsData[index];
    const postES = typeof item.postES === 'object' 
        ? `${item.postES.post_title||item.postES.title||''}\n\n${item.postES.post_body||item.postES.body||''}\n\n${item.postES.post_question||item.postES.question||''}\n\n${item.postES.post_authority||item.postES.authority||''}\n\n${Array.isArray(item.postES.hashtags) ? item.postES.hashtags.join(' ') : item.postES.hashtags||''}`
        : (item.postES || '');
    navigator.clipboard.writeText(postES); 
    showToast("✅ Post en Español copiado!"); 
}

function copyQuizEN(index) {
    navigator.clipboard.writeText(quizzesData[index].postEN || '');
    showToast("✅ Quiz post (EN) copied!");
}

function copyQuizES(index) {
    navigator.clipboard.writeText(quizzesData[index].postES || '');
    showToast("✅ Quiz post (ES) copiado!");
}

function copyPhraseEN(index) {
    const item = phrasesData[index];
    navigator.clipboard.writeText(item.postEN || '');
    showToast("✅ English post copied!");
}

function copyPhraseES(index) {
    const item = phrasesData[index];
    navigator.clipboard.writeText(item.postES || item.postEN || '');
    showToast("✅ Post en Español copiado!");
}

function copyPrompt(index) { navigator.clipboard.writeText(newsData[index].visual_prompt || newsData[index].prompt); showToast("🎨 Art Prompt LUXURY copiado"); }
function copyQuizPrompt(index) { navigator.clipboard.writeText(quizzesData[index].visual_prompt || quizzesData[index].prompt); showToast("🎨 Prompt QUIZ copiado"); }
function copyPhrasePrompt(index) { navigator.clipboard.writeText(phrasesData[index].visual_prompt || phrasesData[index].prompt); showToast("🎨 Prompt Minimalista copiado"); }

function showToast(msg) {
    const toast = document.getElementById('toast');
    if(!toast) return;
    toast.innerText = msg;
    toast.classList.add('active');
    setTimeout(() => toast.classList.remove('active'), 2500);
}

window.onload = loadData;

window.onload = loadData;
