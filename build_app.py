import json

with open("sns_contents_100.csv", "r", encoding="utf-8-sig") as f:
    import csv
    reader = csv.DictReader(f)
    posts = list(reader)

posts_json = json.dumps(posts, ensure_ascii=False, indent=2)

html_content = f'''<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>Threads投稿アシスタント ｜ INTEVE × 理学療法教育DX</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700;800&family=Noto+Sans+JP:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #f8fafc;
      --header-bg: rgba(255, 255, 255, 0.95);
      --card-bg: #ffffff;
      --card-border: #e2e8f0;
      --card-hover: #f1f5f9;
      --text-main: #0f172a;
      --text-muted: #64748b;
      --text-dim: #94a3b8;
      --primary: #0f766e;
      --primary-hover: #115e59;
      --primary-light: #ccfbf1;
      --accent: #0284c7;
      --success: #10b981;
      --success-bg: #ecfdf5;
      --success-border: #a7f3d0;
      --success-text: #047857;

      /* 5大カテゴリーカラー */
      --cat-edu: #e11d48;     /* 実習・教育の本音 (ローズ) */
      --cat-dx: #0d9488;      /* 医療教育DX・業務効率化 (ティール) */
      --cat-career: #7c3aed;  /* PTのキャリア・未来 (バイオレット) */
      --cat-clinical: #d97706;/* 臨床思考・リハビリのリアル (アンバー) */
      --cat-mind: #2563eb;    /* 教員室のつぶやき・マインド (ブルー) */
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-tap-highlight-color: transparent;
    }}

    body {{
      font-family: 'Noto Sans JP', -apple-system, BlinkMacSystemFont, sans-serif;
      background-color: var(--bg);
      color: var(--text-main);
      min-height: 100vh;
      line-height: 1.6;
      padding-bottom: 90px;
    }}

    /* 固定ヘッダー */
    .sticky-header {{
      position: sticky;
      top: 0;
      z-index: 100;
      background: var(--header-bg);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border-bottom: 1px solid var(--card-border);
      box-shadow: 0 4px 20px -5px rgba(0, 0, 0, 0.05);
    }}

    .header-inner {{
      max-width: 680px;
      margin: 0 auto;
      padding: 12px 16px;
    }}

    .profile-bar {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 10px;
    }}

    .profile-info {{
      display: flex;
      align-items: center;
      gap: 10px;
      min-width: 0;
    }}

    .avatar-wrap {{
      width: 44px;
      height: 44px;
      border-radius: 50%;
      background: linear-gradient(135deg, #0d9488, #0284c7);
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      font-weight: 800;
      font-size: 17px;
      flex-shrink: 0;
      box-shadow: 0 2px 8px rgba(13, 148, 136, 0.3);
    }}

    .profile-meta {{
      min-width: 0;
    }}

    .profile-meta .title {{
      font-size: 13.5px;
      font-weight: 700;
      color: var(--text-main);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .badge-pt {{
      font-size: 10px;
      background: #ccfbf1;
      color: #0f766e;
      padding: 1px 6px;
      border-radius: 9999px;
      font-weight: 700;
    }}

    .profile-meta .subtitle {{
      font-size: 11px;
      color: var(--text-muted);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}

    .header-links {{
      display: flex;
      gap: 6px;
      flex-shrink: 0;
    }}

    .ext-btn {{
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 5px 10px;
      border-radius: 20px;
      font-size: 11px;
      font-weight: 700;
      text-decoration: none;
      transition: all 0.2s ease;
    }}

    .ext-btn-threads {{
      background: #000000;
      color: #ffffff;
    }}
    .ext-btn-threads:hover {{
      background: #262626;
      transform: translateY(-1px);
    }}

    .ext-btn-note {{
      background: #249F80;
      color: #ffffff;
    }}
    .ext-btn-note:hover {{
      background: #1e876c;
      transform: translateY(-1px);
    }}

    /* ランダム投稿アクションバー */
    .random-action-bar {{
      display: flex;
      gap: 8px;
      margin-bottom: 12px;
    }}

    .random-btn {{
      flex: 1;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      padding: 10px 14px;
      background: linear-gradient(135deg, #0f766e, #0369a1);
      color: white;
      border: none;
      border-radius: 12px;
      font-size: 13px;
      font-weight: 700;
      cursor: pointer;
      box-shadow: 0 4px 12px rgba(15, 118, 110, 0.25);
      transition: all 0.2s;
    }}
    .random-btn:hover {{
      opacity: 0.95;
      transform: translateY(-1px);
    }}
    .random-btn:active {{
      transform: scale(0.98);
    }}

    .shuffle-toggle-btn {{
      display: inline-flex;
      align-items: center;
      gap: 5px;
      padding: 10px 14px;
      background: white;
      color: var(--text-main);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .shuffle-toggle-btn.active {{
      background: #f0fdf4;
      border-color: #86efac;
      color: #166534;
      font-weight: 700;
    }}

    /* 進捗バー */
    .progress-section {{
      margin-bottom: 10px;
    }}

    .progress-labels {{
      display: flex;
      justify-content: space-between;
      font-size: 11.5px;
      font-weight: 600;
      color: var(--text-muted);
      margin-bottom: 4px;
    }}

    .progress-bar-bg {{
      width: 100%;
      height: 7px;
      background-color: #e2e8f0;
      border-radius: 9999px;
      overflow: hidden;
    }}

    .progress-bar-fill {{
      height: 100%;
      background: linear-gradient(90deg, #0d9488, #0284c7);
      border-radius: 9999px;
      transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }}

    /* 検索 & フィルターバー */
    .filter-controls {{
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}

    .search-box {{
      width: 100%;
      padding: 8px 12px;
      border-radius: 10px;
      border: 1px solid var(--card-border);
      font-size: 13px;
      outline: none;
      background: #f1f5f9;
      color: var(--text-main);
      transition: all 0.2s;
    }}
    .search-box:focus {{
      background: #ffffff;
      border-color: var(--primary);
      box-shadow: 0 0 0 3px rgba(15, 118, 110, 0.15);
    }}

    .filter-tabs {{
      display: flex;
      gap: 6px;
      overflow-x: auto;
      padding-bottom: 2px;
      scrollbar-width: none;
    }}
    .filter-tabs::-webkit-scrollbar {{
      display: none;
    }}

    .tab-btn {{
      padding: 5px 12px;
      font-size: 11.5px;
      font-weight: 600;
      color: var(--text-muted);
      background: white;
      border: 1px solid var(--card-border);
      border-radius: 20px;
      white-space: nowrap;
      cursor: pointer;
      transition: all 0.15s ease;
    }}
    .tab-btn.active {{
      background: var(--text-main);
      color: #ffffff;
      border-color: var(--text-main);
    }}

    .category-select {{
      width: 100%;
      padding: 6px 10px;
      border-radius: 10px;
      border: 1px solid var(--card-border);
      font-size: 12px;
      font-weight: 600;
      color: var(--text-main);
      background: white;
      outline: none;
    }}

    /* メインコンテンツ */
    .main-wrap {{
      max-width: 680px;
      margin: 16px auto 0;
      padding: 0 16px;
    }}

    .posts-container {{
      display: flex;
      flex-direction: column;
      gap: 14px;
    }}

    /* 投稿カード */
    .post-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 16px;
      position: relative;
      transition: all 0.2s ease;
      cursor: pointer;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
    }}

    .post-card:hover {{
      border-color: #cbd5e1;
      transform: translateY(-1px);
      box-shadow: 0 6px 16px -4px rgba(0, 0, 0, 0.06);
    }}

    .post-card:active {{
      transform: scale(0.995);
    }}

    .post-card.completed {{
      background: #fafaf9;
      border-color: #e5e5e5;
      opacity: 0.78;
    }}

    .card-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 12px;
      gap: 8px;
    }}

    .card-meta-left {{
      display: flex;
      align-items: center;
      gap: 6px;
      flex-wrap: wrap;
    }}

    .day-badge {{
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 11px;
      font-weight: 800;
      background: #0f172a;
      color: #ffffff;
      padding: 2px 8px;
      border-radius: 6px;
      letter-spacing: -0.2px;
    }}

    .cat-badge {{
      font-size: 11px;
      font-weight: 700;
      padding: 2px 8px;
      border-radius: 6px;
      color: #ffffff;
    }}

    .cat-edu {{ background-color: var(--cat-edu); }}
    .cat-dx {{ background-color: var(--cat-dx); }}
    .cat-career {{ background-color: var(--cat-career); }}
    .cat-clinical {{ background-color: var(--cat-clinical); }}
    .cat-mind {{ background-color: var(--cat-mind); }}

    .char-count {{
      font-size: 10.5px;
      color: var(--text-dim);
      font-family: 'Plus Jakarta Sans', sans-serif;
    }}

    .check-wrapper {{
      display: inline-flex;
      align-items: center;
      gap: 5px;
      background: #f1f5f9;
      padding: 4px 9px;
      border-radius: 20px;
      cursor: pointer;
      user-select: none;
      transition: background 0.2s ease;
    }}

    .check-wrapper:hover {{
      background: #e2e8f0;
    }}

    .post-card.completed .check-wrapper {{
      background: var(--success-bg);
      border: 1px solid var(--success-border);
    }}

    .check-input {{
      accent-color: var(--success);
      width: 14px;
      height: 14px;
      cursor: pointer;
    }}

    .check-label {{
      font-size: 11px;
      font-weight: 700;
      color: var(--text-muted);
    }}

    .post-card.completed .check-label {{
      color: var(--success-text);
    }}

    .card-content {{
      font-size: 13.5px;
      line-height: 1.7;
      color: #1e293b;
      white-space: pre-wrap;
      word-break: break-word;
      margin-bottom: 14px;
    }}

    .card-footer {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-top: 1px solid #f1f5f9;
      padding-top: 10px;
      gap: 10px;
    }}

    .copy-hint {{
      font-size: 11.5px;
      color: var(--primary);
      font-weight: 600;
      display: inline-flex;
      align-items: center;
      gap: 5px;
    }}

    .copy-hint svg {{
      width: 14px;
      height: 14px;
    }}

    .direct-threads-btn {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: #000000;
      color: #ffffff;
      padding: 6px 12px;
      border-radius: 20px;
      font-size: 11.5px;
      font-weight: 700;
      text-decoration: none;
      transition: all 0.15s ease;
      box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
    }}

    .direct-threads-btn:hover {{
      background: #262626;
      transform: translateY(-1px);
    }}

    .direct-threads-btn svg {{
      width: 13px;
      height: 13px;
      fill: currentColor;
    }}

    /* トースト通知 */
    .toast {{
      position: fixed;
      bottom: 24px;
      left: 50%;
      transform: translateX(-50%) translateY(100px);
      background: rgba(15, 23, 42, 0.92);
      color: #ffffff;
      padding: 10px 18px;
      border-radius: 30px;
      font-size: 13px;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 8px;
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
      backdrop-filter: blur(8px);
      z-index: 1000;
      opacity: 0;
      transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
      pointer-events: none;
      white-space: nowrap;
    }}

    .toast.show {{
      transform: translateX(-50%) translateY(0);
      opacity: 1;
    }}

    /* ランダムピックアップ モーダル */
    .modal-overlay {{
      display: none;
      position: fixed;
      inset: 0;
      background: rgba(15, 23, 42, 0.6);
      backdrop-filter: blur(4px);
      z-index: 2000;
      align-items: center;
      justify-content: center;
      padding: 16px;
    }}
    .modal-overlay.active {{
      display: flex;
    }}

    .modal-box {{
      background: white;
      width: 100%;
      max-width: 540px;
      border-radius: 20px;
      padding: 20px;
      box-shadow: 0 20px 40px rgba(0,0,0,0.25);
      animation: popIn 0.25s cubic-bezier(0.16, 1, 0.3, 1);
      display: flex;
      flex-direction: column;
      max-height: 90vh;
    }}

    @keyframes popIn {{
      0% {{ transform: scale(0.9); opacity: 0; }}
      100% {{ transform: scale(1); opacity: 1; }}
    }}

    .modal-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 12px;
    }}

    .modal-title {{
      font-size: 15px;
      font-weight: 800;
      display: flex;
      align-items: center;
      gap: 6px;
      color: #0f766e;
    }}

    .modal-close-btn {{
      background: #f1f5f9;
      border: none;
      width: 28px;
      height: 28px;
      border-radius: 50%;
      font-size: 16px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--text-muted);
    }}

    .modal-body {{
      overflow-y: auto;
      margin-bottom: 16px;
      background: #f8fafc;
      padding: 14px;
      border-radius: 12px;
      border: 1px solid #e2e8f0;
      font-size: 13.5px;
      line-height: 1.7;
      white-space: pre-wrap;
    }}

    .modal-footer {{
      display: flex;
      gap: 8px;
    }}

    .modal-btn {{
      flex: 1;
      padding: 10px;
      border-radius: 12px;
      font-size: 13px;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      text-decoration: none;
      border: none;
      transition: all 0.15s;
    }}

    .modal-btn-copy {{
      background: #0f766e;
      color: white;
    }}
    .modal-btn-copy:hover {{
      background: #115e59;
    }}

    .modal-btn-threads {{
      background: #000000;
      color: white;
    }}
    .modal-btn-threads:hover {{
      background: #262626;
    }}

    .modal-btn-reroll {{
      background: #f1f5f9;
      color: var(--text-main);
      flex: 0 0 44px;
    }}
    .modal-btn-reroll:hover {{
      background: #e2e8f0;
    }}

    .empty-state {{
      text-align: center;
      padding: 40px 16px;
      color: var(--text-muted);
      font-size: 14px;
    }}
  </style>
</head>
<body>

  <!-- 固定ヘッダー -->
  <header class="sticky-header">
    <div class="header-inner">
      <div class="profile-bar">
        <div class="profile-info">
          <div class="avatar-wrap">大</div>
          <div class="profile-meta">
            <div class="title">
              カズヒロ｜医療教育DX <span class="badge-pt">PT歴22年</span>
            </div>
            <div class="subtitle">@csdkotsuka ｜ 臨床実習・教育改革・INTEVE</div>
          </div>
        </div>

        <div class="header-links">
          <a href="https://www.threads.net/@csdkotsuka" target="_blank" rel="noopener noreferrer" class="ext-btn ext-btn-threads">
            Threads
          </a>
          <a href="https://note.com/csdkazuhiro" target="_blank" rel="noopener noreferrer" class="ext-btn ext-btn-note">
            note
          </a>
        </div>
      </div>

      <!-- ランダム & シャッフル操作バー -->
      <div class="random-action-bar">
        <button class="random-btn" onclick="openRandomPicker()">
          🎲 今日の投稿をランダム選出！
        </button>
        <button id="shuffleToggleBtn" class="shuffle-toggle-btn" onclick="toggleShuffle()">
          🔀 シャッフル表示: <span id="shuffleStateText">OFF</span>
        </button>
      </div>

      <!-- 進捗セクション -->
      <div class="progress-section">
        <div class="progress-labels">
          <span>進捗状況</span>
          <span id="progressText">0 / 100 完了 (0%)</span>
        </div>
        <div class="progress-bar-bg">
          <div id="progressBar" class="progress-bar-fill" style="width: 0%"></div>
        </div>
      </div>

      <!-- 検索 ＆ 絞り込みフィルター -->
      <div class="filter-controls">
        <input type="text" id="searchInput" class="search-box" placeholder="🔍 キーワード検索（例: 実習, AI, 歩行, 国家試験）" oninput="renderPosts()">

        <div style="display: flex; gap: 8px;">
          <div class="filter-tabs">
            <button class="tab-btn active" data-filter="all" onclick="setFilter('all')">すべて (100)</button>
            <button class="tab-btn" data-filter="unposted" onclick="setFilter('unposted')">未投稿 (100)</button>
            <button class="tab-btn" data-filter="posted" onclick="setFilter('posted')">完了 (0)</button>
          </div>
        </div>

        <select id="catFilter" class="category-select" onchange="renderPosts()">
          <option value="all">📁 すべてのカテゴリー（全5ジャンル）</option>
          <option value="実習・教育の本音">実習・教育の本音 (20本)</option>
          <option value="医療教育DX・業務効率化">医療教育DX・業務効率化 (20本)</option>
          <option value="PTのキャリア・未来">PTのキャリア・未来 (20本)</option>
          <option value="臨床思考・リハビリのリアル">臨床思考・リハビリのリアル (20本)</option>
          <option value="教員室のつぶやき・マインド">教員室のつぶやき・マインド (20本)</option>
        </select>
      </div>
    </div>
  </header>

  <!-- 投稿リスト一覧 -->
  <main class="main-wrap">
    <div id="postsContainer" class="posts-container"></div>
  </main>

  <!-- トースト通知 -->
  <div id="toast" class="toast">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#34d399" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
      <polyline points="20 6 9 17 4 12"></polyline>
    </svg>
    <span>本文をクリップボードにコピーしました！</span>
  </div>

  <!-- ランダム選出モーダル -->
  <div id="modalOverlay" class="modal-overlay" onclick="closeModal(event)">
    <div class="modal-box" onclick="event.stopPropagation()">
      <div class="modal-header">
        <div class="modal-title">
          <span>🎲 本日のおすすめ投稿</span>
          <span id="modalMetaBadge" class="cat-badge" style="font-size: 10px;"></span>
        </div>
        <button class="modal-close-btn" onclick="closeModalDirect()">&times;</button>
      </div>
      <div id="modalContent" class="modal-body"></div>
      <div class="modal-footer">
        <button class="modal-btn modal-btn-reroll" onclick="rerollRandom()" title="もう一度引く">🎲</button>
        <button id="modalCopyBtn" class="modal-btn modal-btn-copy" onclick="copyModalContent()">コピーする</button>
        <a id="modalThreadsBtn" href="#" target="_blank" rel="noopener noreferrer" class="modal-btn modal-btn-threads">Threadsで投稿</a>
      </div>
    </div>
  </div>

  <script>
    const POSTS_DATA = {posts_json};

    const CAT_CLASSES = {{
      '実習・教育の本音': 'cat-edu',
      '医療教育DX・業務効率化': 'cat-dx',
      'PTのキャリア・未来': 'cat-career',
      '臨床思考・リハビリのリアル': 'cat-clinical',
      '教員室のつぶやき・マインド': 'cat-mind'
    }};

    const STORAGE_KEY = 'threads_pt_edu_completed_v1';
    let completedSet = new Set(JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]'));
    let currentFilter = 'all';
    let isShuffled = false;
    let shuffledIndices = [];
    let currentModalItem = null;

    function saveCompleted() {{
      localStorage.setItem(STORAGE_KEY, JSON.stringify(Array.from(completedSet)));
      updateProgress();
    }}

    function toggleComplete(day, event) {{
      if (event) event.stopPropagation();
      if (completedSet.has(day)) {{
        completedSet.delete(day);
      }} else {{
        completedSet.add(day);
      }}
      saveCompleted();
      renderPosts();
    }}

    function handleCardClick(day) {{
      const item = POSTS_DATA.find(p => p.Day === day);
      if (!item) return;
      copyToClipboard(item.Content);
    }}

    function copyToClipboard(text) {{
      navigator.clipboard.writeText(text).then(() => {{
        showToast('本文をコピーしました！Threadsに貼り付けて投稿できます');
      }}).catch(() => {{
        const textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        document.body.appendChild(textarea);
        textarea.select();
        try {{
          document.execCommand('copy');
          showToast('本文をコピーしました！');
        }} catch (err) {{
          alert('コピーに失敗しました');
        }}
        document.body.removeChild(textarea);
      }});
    }}

    let toastTimer = null;
    function showToast(msg) {{
      const toast = document.getElementById('toast');
      toast.querySelector('span').textContent = msg;
      toast.classList.add('show');
      if (toastTimer) clearTimeout(toastTimer);
      toastTimer = setTimeout(() => {{
        toast.classList.remove('show');
      }}, 2200);
    }}

    function setFilter(filter) {{
      currentFilter = filter;
      document.querySelectorAll('.tab-btn').forEach(btn => {{
        btn.classList.toggle('active', btn.dataset.filter === filter);
      }});
      renderPosts();
    }}

    function toggleShuffle() {{
      isShuffled = !isShuffled;
      const btn = document.getElementById('shuffleToggleBtn');
      const text = document.getElementById('shuffleStateText');
      if (isShuffled) {{
        btn.classList.add('active');
        text.textContent = 'ON';
        // Fisher-Yates shuffle
        shuffledIndices = POSTS_DATA.map((_, i) => i);
        for (let i = shuffledIndices.length - 1; i > 0; i--) {{
          const j = Math.floor(Math.random() * (i + 1));
          [shuffledIndices[i], shuffledIndices[j]] = [shuffledIndices[j], shuffledIndices[i]];
        }}
        showToast('投稿をランダム順に並び替えました 🔀');
      }} else {{
        btn.classList.remove('active');
        text.textContent = 'OFF';
        showToast('通常の並び順に戻しました');
      }}
      renderPosts();
    }}

    function openRandomPicker() {{
      const unposted = POSTS_DATA.filter(p => !completedSet.has(p.Day));
      const pool = unposted.length > 0 ? unposted : POSTS_DATA;
      const picked = pool[Math.floor(Math.random() * pool.length)];
      showModalFor(picked);
    }}

    function rerollRandom() {{
      const unposted = POSTS_DATA.filter(p => !completedSet.has(p.Day) && p.Day !== (currentModalItem ? currentModalItem.Day : ''));
      const pool = unposted.length > 0 ? unposted : POSTS_DATA;
      const picked = pool[Math.floor(Math.random() * pool.length)];
      showModalFor(picked);
    }}

    function showModalFor(item) {{
      currentModalItem = item;
      const catClass = CAT_CLASSES[item.CategoryShort] || 'cat-edu';
      const badge = document.getElementById('modalMetaBadge');
      badge.textContent = `${{item.Day}} ｜ ${{item.CategoryShort}}`;
      badge.className = `cat-badge ${{catClass}}`;
      
      document.getElementById('modalContent').textContent = item.Content;

      const encodedText = encodeURIComponent(item.Content);
      document.getElementById('modalThreadsBtn').href = `https://www.threads.net/intent/post?text=${{encodedText}}`;

      document.getElementById('modalOverlay').classList.add('active');
    }}

    function closeModal(e) {{
      if (e.target.id === 'modalOverlay') {{
        closeModalDirect();
      }}
    }}

    function closeModalDirect() {{
      document.getElementById('modalOverlay').classList.remove('active');
    }}

    function copyModalContent() {{
      if (!currentModalItem) return;
      copyToClipboard(currentModalItem.Content);
    }}

    function updateProgress() {{
      const total = POSTS_DATA.length;
      const completed = completedSet.size;
      const pct = Math.round((completed / total) * 100);
      
      document.getElementById('progressText').textContent = `${{completed}} / ${{total}} 完了 (${{pct}}%)`;
      document.getElementById('progressBar').style.width = `${{pct}}%`;

      const unpostedCount = total - completed;
      document.querySelector('[data-filter="all"]').textContent = `すべて (${{total}})`;
      document.querySelector('[data-filter="unposted"]').textContent = `未投稿 (${{unpostedCount}})`;
      document.querySelector('[data-filter="posted"]').textContent = `完了 (${{completed}})`;
    }}

    function renderPosts() {{
      const container = document.getElementById('postsContainer');
      const catFilter = document.getElementById('catFilter').value;
      const searchKeyword = (document.getElementById('searchInput').value || '').trim().toLowerCase();

      let items = isShuffled 
        ? shuffledIndices.map(idx => POSTS_DATA[idx])
        : [...POSTS_DATA];

      const filtered = items.filter(item => {{
        const isCompleted = completedSet.has(item.Day);
        if (currentFilter === 'unposted' && isCompleted) return false;
        if (currentFilter === 'posted' && !isCompleted) return false;
        if (catFilter !== 'all' && item.CategoryShort !== catFilter) return false;
        if (searchKeyword && !item.Content.toLowerCase().includes(searchKeyword) && !item.CategoryShort.toLowerCase().includes(searchKeyword)) {{
          return false;
        }}
        return true;
      }});

      if (filtered.length === 0) {{
        container.innerHTML = '<div class="empty-state">該当する投稿がありません 🩺</div>';
        return;
      }}

      container.innerHTML = filtered.map(item => {{
        const isCompleted = completedSet.has(item.Day);
        const catClass = CAT_CLASSES[item.CategoryShort] || 'cat-edu';
        const charCount = item.Content.length;
        const encodedText = encodeURIComponent(item.Content);
        const threadsIntentUrl = `https://www.threads.net/intent/post?text=${{encodedText}}`;

        return `
          <article class="post-card ${{isCompleted ? 'completed' : ''}}" onclick="handleCardClick('${{item.Day}}')">
            <div class="card-header">
              <div class="card-meta-left">
                <span class="day-badge">${{item.Day}}</span>
                <span class="cat-badge ${{catClass}}">${{item.CategoryShort}}</span>
                <span class="char-count">${{charCount}}文字</span>
              </div>
              <label class="check-wrapper" onclick="event.stopPropagation()">
                <input type="checkbox" class="check-input" ${{isCompleted ? 'checked' : ''}} onchange="toggleComplete('${{item.Day}}', event)">
                <span class="check-label">${{isCompleted ? '投稿済み ✓' : '未投稿'}}</span>
              </label>
            </div>

            <div class="card-content">${{escapeHtml(item.Content)}}</div>

            <div class="card-footer">
              <span class="copy-hint">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                  <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                </svg>
                タップでコピー
              </span>

              <a href="${{threadsIntentUrl}}" target="_blank" rel="noopener noreferrer" class="direct-threads-btn" onclick="event.stopPropagation()">
                <svg viewBox="0 0 192 192">
                  <path d="M141.537 88.9883C140.71 88.5919 139.87 88.2104 139.019 87.8451C137.537 60.5382 122.616 44.905 97.5619 44.745C97.4484 44.7443 97.3355 44.7443 97.222 44.7443C82.2364 44.7443 69.7731 51.1409 62.102 62.7807L75.6026 72.8105C80.8936 64.7818 89.2618 61.2721 97.222 61.2721C110.155 61.2721 118.892 70.0769 119.988 88.4239C112.984 87.5606 105.474 87.4913 97.5619 88.2238C69.3789 90.8354 53.6483 105.748 53.9483 125.795C54.2383 145.185 69.9572 159.256 90.3541 159.256C104.996 159.256 116.368 152.483 122.951 140.065C127.356 148.657 134.793 154.512 144.383 156.974C148.243 157.965 152.378 158.461 156.685 158.461C164.795 158.461 172.484 156.386 179.373 152.277L171.745 137.818C166.861 140.73 161.439 142.193 155.673 142.193C148.718 142.193 143.766 139.73 141.229 135.006C138.868 130.609 137.95 124.364 138.358 116.142C146.435 111.458 152.614 104.797 156.402 96.6579C160.708 87.4055 161.859 76.5161 159.732 65.0934C156.887 49.8118 147.269 37.6046 133.09 31.0666C121.285 25.6231 107.502 22.7557 92.115 22.7557C76.728 22.7557 62.9452 25.6231 51.1402 31.0666C36.9612 37.6046 27.3432 49.8118 24.4982 65.0934C22.2592 77.1205 23.6302 89.0494 28.4872 99.6644C33.6262 110.895 42.0622 119.897 52.8802 125.704L61.0262 110.518C53.3852 106.417 47.4272 100.063 43.7992 92.1274C40.3542 84.5975 39.3812 76.1368 40.9712 67.6022C43.0032 56.6811 49.8732 47.9621 60.0002 43.2925C69.3732 38.9701 80.3162 36.6897 92.5402 36.6897C104.764 36.6897 115.707 38.9701 125.08 43.2925C135.207 47.9621 142.077 56.6811 144.109 67.6022C145.625 75.7486 144.808 83.5186 141.745 90.0963C139.757 94.3643 136.671 97.9048 132.748 100.618C132.84 96.6579 132.616 92.7451 132.076 88.9328C135.26 90.3194 138.435 91.8016 141.537 93.3645V88.9883ZM91.4332 143.084C78.4332 143.084 69.9572 134.57 69.7572 122.955C69.5372 110.174 79.5292 103.585 97.9372 101.884C104.811 101.248 111.391 101.554 117.485 102.732C115.176 130.655 104.144 143.084 91.4332 143.084Z"/>
                </svg>
                Threadsで投稿
              </a>
            </div>
          </article>
        `;
      }}).join('');
    }}

    function escapeHtml(str) {{
      return str
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
    }}

    updateProgress();
    renderPosts();
  </script>
</body>
</html>
'''

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Successfully generated index.html")
