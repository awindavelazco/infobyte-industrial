/* INFOBYTE MASTER CONTENT HUB - DYNAMIC BATCH */

let newsData = [];
let phrasesData = [];
let quizzesData = [];
let videosData = [];
let currentView = 'news';
let activeIndex = -1;

async function loadData() {
    try {
        const newsResponse = await fetch('posts_content.json?t=' + Date.now());
        const newsJson = await newsResponse.json();
        newsData = newsJson.posts || [];
        const generatedAt = newsJson.generated_at || 'Fecha no disponible';
        document.getElementById('timestamp').innerText = `Ultima generacion: ${generatedAt} | ${newsData.length} noticias`;
    } catch (e) {
        console.warn("No se pudo cargar posts_content.json:", e);
        document.getElementById('timestamp').innerText = "Error de carga";
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

    try {
        const videosResponse = await fetch('videos_content.json?t=' + Date.now());
        const videosJson = await videosResponse.json();
        videosData = videosJson.videos || [];
    } catch (e) {
        console.warn("No se pudo cargar videos_content.json:", e);
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
    else if (currentView === 'videos') data = videosData;

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
        } else if(currentView === 'phrases') {
            card.innerHTML = `
                <div class="category-tag">#${displayId} | Apuntes del Alma</div>
                <h3 class="card-title" style="font-style: italic; font-size: 1em;">${(item.hook_text || '').split('\n')[0]}</h3>
                <div class="btn-group">
                    <button class="btn btn-read" onclick="openModal(${index})">📖 Leer Post (Bilingüe)</button>
                    <button class="btn btn-copy-en" onclick="copyPhraseEN(${index})">📋 Copiar Post (EN)</button>
                    <button class="btn btn-prompt" onclick="copyPhrasePrompt(${index})" style="background: #9c27b0;">🖼️ Prompt MINIMALISTA</button>
                </div>`;
        } else if(currentView === 'videos') {
            card.innerHTML = `
                <div class="category-tag">#${displayId} | VIDEO SCRIPT</div>
                <h3 class="card-title">${item.topic_es || 'Video'}</h3>
                <p style="font-size: 0.8em; color: #aaa; margin-bottom: 10px;">3 escenas - 15 seg</p>
                <div class="btn-group">
                    <button class="btn btn-read" onclick="openModal(${index})">📖 Leer Plan (ES/EN)</button>
                    <button class="btn btn-copy-en" onclick="copyVideoVoiceover(${index})" style="background: #e91e63;">🎤 Copiar Voz (EN)</button>
                    <button class="btn btn-prompt" onclick="copyVideoPrompts(${index})" style="background: #00bcd4; color: black;">🎬 Copiar Prompts Luma/Kling</button>
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
    document.getElementById('tabVideos').classList.toggle('active', view === 'videos');
    
    let title = "Infobyte News Dashboard";
    if (view === 'phrases') title = "Apuntes del Alma";
    if (view === 'quizzes') title = "Viral Quizzes & Engagement";
    if (view === 'videos') title = "Video Scripts (Luma/Kling)";
    
    document.querySelector('.section-title').innerText = title;
    renderContent();
}

function openModal(index) {
    activeIndex = index;
    let data = [];
    if (currentView === 'news') data = newsData;
    else if (currentView === 'phrases') data = phrasesData;
    else if (currentView === 'quizzes') data = quizzesData;
    else if (currentView === 'videos') data = videosData;
    
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
    if (currentView === 'videos') typeLabel = "PLAN DE VIDEO";

    if (currentView === 'videos') {
        bodyHTML += `<div style="background:#1a1a2e; border-left:3px solid #00f2fe; padding:15px; border-radius:4px; margin-bottom:15px;">`;
        bodyHTML += `<small style="color:#00f2fe; font-weight:bold; display:block; margin-bottom:5px;">🇪🇸 PLAN DEL VIDEO (ES)</small>`;
        bodyHTML += `<span style="color:#ccc;">${item.video_plan_es}</span></div>`;

        bodyHTML += `<div style="background:#1a1a2e; border-left:3px solid #e91e63; padding:15px; border-radius:4px; margin-bottom:15px;">`;
        bodyHTML += `<small style="color:#e91e63; font-weight:bold; display:block; margin-bottom:5px;">🎤 VOICEOVER (EN) - 15 seg</small>`;
        bodyHTML += `<span style="color:#ccc;">${item.voiceover_en}</span></div>`;

        bodyHTML += `<div style="display:flex; gap:10px; margin-bottom:15px;">`;
        bodyHTML += `<div style="flex:1; background:#111; padding:10px; border-radius:4px; border:1px solid #333;"><small style="color:#ffeb3b; display:block; margin-bottom:5px;">🎬 Escena 1 (0-5s)</small><span style="font-size:0.85em; color:#aaa;">${item.scene_1_prompt_en}</span></div>`;
        bodyHTML += `<div style="flex:1; background:#111; padding:10px; border-radius:4px; border:1px solid #333;"><small style="color:#ffeb3b; display:block; margin-bottom:5px;">🎬 Escena 2 (5-10s)</small><span style="font-size:0.85em; color:#aaa;">${item.scene_2_prompt_en}</span></div>`;
        bodyHTML += `<div style="flex:1; background:#111; padding:10px; border-radius:4px; border:1px solid #333;"><small style="color:#ffeb3b; display:block; margin-bottom:5px;">🎬 Escena 3 (10-15s)</small><span style="font-size:0.85em; color:#aaa;">${item.scene_3_prompt_en}</span></div>`;
        bodyHTML += `</div>`;

        bodyHTML += `<div style="background:#1a1a2e; border-left:3px solid #2e7d32; padding:15px; border-radius:4px;">`;
        bodyHTML += `<small style="color:#2e7d32; font-weight:bold; display:block; margin-bottom:5px;">📋 POST CAPTION (EN)</small>`;
        bodyHTML += `<span style="color:#ccc; white-space: pre-wrap;">${item.post_text_en}</span></div>`;
    } else {
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
    }
    
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

function copyVideoVoiceover(index) {
    const item = videosData[index];
    navigator.clipboard.writeText(item.voiceover_en || '');
    showToast("🎤 Voz en off copiada!");
}

function copyVideoPrompts(index) {
    const item = videosData[index];
    const prompts = `Scene 1 (0-5s): ${item.scene_1_prompt_en}\n\nScene 2 (5-10s): ${item.scene_2_prompt_en}\n\nScene 3 (10-15s): ${item.scene_3_prompt_en}`;
    navigator.clipboard.writeText(prompts);
    showToast("🎬 Prompts copiados para Kling/Luma!");
}

function showToast(msg) {
    const toast = document.getElementById('toast');
    if(!toast) return;
    toast.innerText = msg;
    toast.classList.add('active');
    setTimeout(() => toast.classList.remove('active'), 2500);
}

window.onload = loadData;

window.onload = loadData;
