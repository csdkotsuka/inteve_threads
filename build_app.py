import json
import csv
from threads_api import load_env

def generate_app():
    env = load_env()
    
    # Read CSV as fallback initial data
    with open("sns_contents_140.csv", "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        posts = list(reader)

    posts_json = json.dumps(posts, ensure_ascii=False, indent=2)

    firebase_config = {
        "apiKey": env.get("FIREBASE_API_KEY", ""),
        "authDomain": env.get("FIREBASE_AUTH_DOMAIN", ""),
        "projectId": env.get("FIREBASE_PROJECT_ID", ""),
        "storageBucket": env.get("FIREBASE_STORAGE_BUCKET", ""),
        "messagingSenderId": env.get("FIREBASE_MESSAGING_SENDER_ID", ""),
        "appId": env.get("FIREBASE_APP_ID", "")
    }
    firebase_config_json = json.dumps(firebase_config, ensure_ascii=False, indent=2)

    html_content = f'''<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>Threads 運用ダッシュボード ｜ INTEVE × 理学療法教育DX</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700;800&family=Noto+Sans+JP:wght@400;500;600;700&display=swap" rel="stylesheet">
  
  <!-- Firebase SDK (Compat) -->
  <script src="https://www.gstatic.com/firebasejs/10.12.0/firebase-app-compat.js"></script>
  <script src="https://www.gstatic.com/firebasejs/10.12.0/firebase-firestore-compat.js"></script>

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
      --warning: #f59e0b;
      --warning-bg: #fffbeb;

      /* 6大カテゴリーカラー */
      --cat-edu: #e11d48;     /* 実習・教育の本音 */
      --cat-dx: #0d9488;      /* 医療教育DX・業務効率化 */
      --cat-career: #7c3aed;  /* PTのキャリア・未来 */
      --cat-clinical: #d97706;/* 臨床思考・リハビリのリアル */
      --cat-mind: #2563eb;    /* 教員室のつぶやき・マインド */
      --cat-gov: #4338ca;     /* 学校経営・教育ガバナンスDX */
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

    .header-wrap {{
      background: var(--header-bg);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--card-border);
      position: sticky;
      top: 0;
      z-index: 100;
      padding: 12px 16px 8px;
    }}

    .header-inner {{
      max-width: 900px;
      margin: 0 auto;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }}

    .header-top {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 8px;
    }}

    .brand-title {{
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 19px;
      font-weight: 800;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .brand-badge {{
      font-size: 11px;
      background: var(--primary-light);
      color: var(--primary);
      padding: 2px 8px;
      border-radius: 9999px;
      font-weight: 700;
    }}

    .sync-status {{
      font-size: 11px;
      display: inline-flex;
      align-items: center;
      gap: 5px;
      padding: 3px 8px;
      border-radius: 9999px;
      background: #f1f5f9;
      color: var(--text-muted);
      font-weight: 600;
    }}

    .sync-dot {{
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: #94a3b8;
    }}
    .sync-dot.connected {{
      background: #10b981;
      box-shadow: 0 0 6px #10b981;
    }}

    .action-bar {{
      display: flex;
      gap: 8px;
      align-items: center;
    }}

    .btn {{
      padding: 6px 12px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      border: 1px solid var(--card-border);
      background: #fff;
      color: var(--text-main);
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.15s ease;
    }}
    .btn:hover {{
      background: var(--card-hover);
    }}
    .btn-primary {{
      background: var(--primary);
      color: #fff;
      border-color: var(--primary);
    }}
    .btn-primary:hover {{
      background: var(--primary-hover);
    }}

    /* 進捗バー */
    .progress-section {{
      background: #f1f5f9;
      padding: 6px 10px;
      border-radius: 8px;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }}
    .progress-labels {{
      display: flex;
      justify-content: space-between;
      font-size: 11px;
      color: var(--text-muted);
      font-weight: 600;
    }}
    .progress-bar-bg {{
      height: 6px;
      background: #e2e8f0;
      border-radius: 9999px;
      overflow: hidden;
    }}
    .progress-bar-fill {{
      height: 100%;
      background: linear-gradient(90deg, #10b981, #0f766e);
      border-radius: 9999px;
      transition: width 0.3s ease;
    }}

    /* フィルターエリア */
    .filter-controls {{
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}

    .search-box {{
      width: 100%;
      padding: 8px 12px;
      font-size: 13px;
      border: 1px solid var(--card-border);
      border-radius: 8px;
      background: #fff;
      outline: none;
    }}
    .search-box:focus {{
      border-color: var(--primary);
      box-shadow: 0 0 0 2px rgba(15, 118, 110, 0.15);
    }}

    .filter-tabs {{
      display: flex;
      gap: 6px;
      overflow-x: auto;
      padding-bottom: 2px;
    }}

    .tab-btn {{
      padding: 5px 11px;
      border-radius: 9999px;
      font-size: 12px;
      font-weight: 600;
      border: 1px solid var(--card-border);
      background: #fff;
      color: var(--text-muted);
      white-space: nowrap;
      cursor: pointer;
      transition: all 0.15s ease;
    }}
    .tab-btn.active {{
      background: var(--text-main);
      color: #fff;
      border-color: var(--text-main);
    }}

    .category-select {{
      padding: 6px 10px;
      font-size: 12px;
      border-radius: 8px;
      border: 1px solid var(--card-border);
      background: #fff;
      color: var(--text-main);
      outline: none;
      cursor: pointer;
    }}

    /* メインリスト */
    .main-wrap {{
      max-width: 900px;
      margin: 16px auto;
      padding: 0 16px;
    }}

    .posts-container {{
      display: grid;
      grid-template-columns: 1fr;
      gap: 12px;
    }}
    @media (min-width: 680px) {{
      .posts-container {{
        grid-template-columns: repeat(2, 1fr);
      }}
    }}

    .post-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 14px 16px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      transition: all 0.2s ease;
      position: relative;
    }}
    .post-card:hover {{
      border-color: #cbd5e1;
      box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }}
    .post-card.status-published {{
      background: #fafafa;
      opacity: 0.85;
      border-color: #e2e8f0;
    }}
    .post-card.status-scheduled {{
      border-color: #93c5fd;
      background: #f8faff;
    }}

    .post-card-top {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 8px;
    }}

    .post-badges {{
      display: flex;
      align-items: center;
      gap: 6px;
      flex-wrap: wrap;
    }}

    .day-badge {{
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 11px;
      font-weight: 800;
      color: var(--text-muted);
    }}

    .cat-badge {{
      font-size: 11px;
      padding: 2px 7px;
      border-radius: 6px;
      font-weight: 700;
      color: #fff;
    }}
    .cat-edu {{ background-color: var(--cat-edu); }}
    .cat-dx {{ background-color: var(--cat-dx); }}
    .cat-career {{ background-color: var(--cat-career); }}
    .cat-clinical {{ background-color: var(--cat-clinical); }}
    .cat-mind {{ background-color: var(--cat-mind); }}
    .cat-gov {{ background-color: var(--cat-gov); }}

    .platform-badge {{
      font-size: 10px;
      font-weight: 700;
      padding: 2px 6px;
      border-radius: 4px;
      background: #f1f5f9;
      color: #334155;
      border: 1px solid #cbd5e1;
    }}

    .status-badge {{
      font-size: 10px;
      padding: 2px 6px;
      border-radius: 4px;
      font-weight: 700;
    }}
    .badge-stock {{ background: #f1f5f9; color: var(--text-muted); }}
    .badge-scheduled {{ background: #dbeafe; color: #1e40af; }}
    .badge-published {{ background: var(--success-bg); color: var(--success-text); border: 1px solid var(--success-border); }}

    .post-body {{
      font-size: 13px;
      line-height: 1.6;
      color: var(--text-main);
      white-space: pre-wrap;
      display: -webkit-box;
      -webkit-line-clamp: 4;
      -webkit-box-orient: vertical;
      overflow: hidden;
      cursor: pointer;
    }}

    .post-body:hover {{
      color: var(--primary);
    }}

    /* インサイトバッジ */
    .insights-row {{
      display: flex;
      gap: 8px;
      align-items: center;
      font-size: 11px;
      background: #f1f5f9;
      padding: 4px 8px;
      border-radius: 6px;
      color: var(--text-muted);
      font-weight: 600;
    }}
    .insight-item {{
      display: inline-flex;
      align-items: center;
      gap: 3px;
    }}

    .card-footer {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-top: 8px;
      border-top: 1px solid #f1f5f9;
      margin-top: auto;
    }}

    .check-toggle {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 12px;
      color: var(--text-muted);
      cursor: pointer;
      user-select: none;
    }}
    .check-toggle input {{
      cursor: pointer;
      accent-color: var(--primary);
      width: 16px;
      height: 16px;
    }}

    .edit-btn {{
      font-size: 12px;
      font-weight: 600;
      color: var(--accent);
      background: none;
      border: none;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 4px 6px;
      border-radius: 4px;
    }}
    .edit-btn:hover {{
      background: #e0f2fe;
    }}

    /* モーダル */
    .modal-overlay {{
      display: none;
      position: fixed;
      inset: 0;
      background: rgba(15, 23, 42, 0.6);
      backdrop-filter: blur(4px);
      z-index: 1000;
      align-items: center;
      justify-content: center;
      padding: 16px;
    }}
    .modal-overlay.active {{
      display: flex;
    }}

    .modal-box {{
      background: #fff;
      border-radius: 16px;
      width: 100%;
      max-width: 600px;
      max-height: 90vh;
      display: flex;
      flex-direction: column;
      box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2);
      overflow: hidden;
      animation: modalFadeIn 0.2s ease-out;
    }}

    @keyframes modalFadeIn {{
      from {{ transform: scale(0.96); opacity: 0; }}
      to {{ transform: scale(1); opacity: 1; }}
    }}

    .modal-header {{
      padding: 14px 18px;
      border-bottom: 1px solid var(--card-border);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    .modal-title-group {{
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .modal-close {{
      background: none;
      border: none;
      font-size: 20px;
      line-height: 1;
      cursor: pointer;
      color: var(--text-dim);
      padding: 4px;
    }}

    .modal-body {{
      padding: 16px 18px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 14px;
    }}

    .edit-textarea {{
      width: 100%;
      min-height: 180px;
      padding: 12px;
      border: 1px solid var(--card-border);
      border-radius: 8px;
      font-family: inherit;
      font-size: 13.5px;
      line-height: 1.6;
      resize: vertical;
      outline: none;
    }}
    .edit-textarea:focus {{
      border-color: var(--primary);
      box-shadow: 0 0 0 2px rgba(15, 118, 110, 0.15);
    }}

    .char-count {{
      font-size: 11px;
      color: var(--text-dim);
      text-align: right;
    }}

    /* 予約設定ブロック */
    .schedule-box {{
      background: #f8fafc;
      border: 1px solid var(--card-border);
      border-radius: 8px;
      padding: 12px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}
    .schedule-title {{
      font-size: 12px;
      font-weight: 700;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .schedule-row {{
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }}
    .schedule-input {{
      flex: 1;
      min-width: 200px;
      padding: 6px 10px;
      font-size: 13px;
      border: 1px solid var(--card-border);
      border-radius: 6px;
      background: #fff;
    }}

    .modal-footer {{
      padding: 12px 18px;
      border-top: 1px solid var(--card-border);
      background: #fafafa;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 8px;
    }}

    .rec-badge {{
      display: inline-block;
      font-size: 10px;
      font-weight: 800;
      line-height: 1;
      padding: 3px 6px;
      border-radius: 9999px;
      background: #f59e0b;
      color: #fff;
      margin-left: 4px;
      vertical-align: middle;
    }}

    .toast {{
      position: fixed;
      bottom: 24px;
      left: 50%;
      transform: translateX(-50%) translateY(100px);
      background: #1e293b;
      color: #fff;
      padding: 10px 18px;
      border-radius: 9999px;
      font-size: 13px;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 8px;
      box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
      z-index: 2000;
      transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1);
      pointer-events: none;
    }}
    .toast.show {{
      transform: translateX(-50%) translateY(0);
    }}
  </style>
</head>
<body>

  <!-- ヘッダー -->
  <header class="header-wrap">
    <div class="header-inner">
      <div class="header-top">
        <div class="brand-title">
          <span>🧵 Threads 運用ダッシュボード</span>
          <span class="brand-badge">理学療法教育DX</span>
          <span id="syncStatus" class="sync-status">
            <span id="syncDot" class="sync-dot"></span>
            <span id="syncText">接続中...</span>
          </span>
        </div>
        <div class="action-bar" style="display: flex; gap: 6px; flex-wrap: wrap;">
          <button class="btn" onclick="openRandomPicker()">🎲 ランダム選出</button>
          <button class="btn btn-primary" onclick="openBulkScheduleModal()">📅 ランダム一括予約</button>
        </div>
      </div>

      <!-- 進捗セクション -->
      <div class="progress-section">
        <div class="progress-labels">
          <span id="progressStats">進捗状況</span>
          <span id="progressText">0 / 100 完了 (0%)</span>
        </div>
        <div class="progress-bar-bg">
          <div id="progressBar" class="progress-bar-fill" style="width: 0%"></div>
        </div>
      </div>

      <!-- 検索 ＆ 絞り込みフィルター -->
      <div class="filter-controls">
        <input type="text" id="searchInput" class="search-box" placeholder="🔍 キーワード検索（例: 実習, AI, 歩行, 国家試験）" oninput="renderPosts()">

        <div style="display: flex; gap: 8px; flex-wrap: wrap; justify-content: space-between;">
          <div class="filter-tabs">
            <button class="tab-btn active" data-filter="all" onclick="setStatusFilter('all')">すべて (<span id="countAll">0</span>)</button>
            <button class="tab-btn" data-filter="stock" onclick="setStatusFilter('stock')">📝 ストック (<span id="countStock">0</span>)</button>
            <button class="tab-btn" data-filter="scheduled" onclick="setStatusFilter('scheduled')">📅 予約中 (<span id="countScheduled">0</span>)</button>
            <button class="tab-btn" data-filter="published" onclick="setStatusFilter('published')">✅ 投稿済み (<span id="countPublished">0</span>)</button>
          </div>

          <select id="catFilter" class="category-select" onchange="renderPosts()">
            <option value="all">📁 すべてのカテゴリー</option>
            <option value="実習・教育の本音">実習・教育の本音</option>
            <option value="医療教育DX・業務効率化">医療教育DX・業務効率化</option>
            <option value="PTのキャリア・未来">PTのキャリア・未来</option>
            <option value="臨床思考・リハビリのリアル">臨床思考・リハビリのリアル</option>
            <option value="教員室のつぶやき・マインド">教員室のつぶやき・マインド</option>
            <option value="学校経営・教育ガバナンスDX">学校経営・教育ガバナンスDX (LinkedIn/B2B)</option>
          </select>
        </div>
      </div>
    </div>
  </header>

  <!-- 投稿リスト一覧 -->
  <main class="main-wrap">
    <div id="postsContainer" class="posts-container">
      <div style="text-align: center; padding: 40px; color: #94a3b8; grid-column: 1/-1;">
        データを読み込み中...
      </div>
    </div>
  </main>

  <!-- トースト通知 -->
  <div id="toast" class="toast">
    <span>通知メッセージ</span>
  </div>

  <!-- 編集・予約モーダル -->
  <div id="modalOverlay" class="modal-overlay" onclick="closeModal(event)">
    <div class="modal-box" onclick="event.stopPropagation()">
      <div class="modal-header">
        <div class="modal-title-group">
          <span id="modalDayBadge" class="day-badge" style="font-size: 13px;"></span>
          <span id="modalCatBadge" class="cat-badge"></span>
          <span id="modalStatusBadge" class="status-badge"></span>
        </div>
        <button class="modal-close" onclick="closeModalDirect()">&times;</button>
      </div>

      <div class="modal-body">
        <div>
          <label style="font-size: 11px; font-weight: 700; color: var(--text-muted); display: block; margin-bottom: 4px;">
            投稿テキスト（オンライン編集・自動同期）
          </label>
          <textarea id="modalEditTextarea" class="edit-textarea" oninput="updateModalCharCount()"></textarea>
          <div id="modalCharCount" class="char-count">0 文字</div>
        </div>

        <!-- 予約設定 -->
        <div class="schedule-box">
          <div class="schedule-title">
            <span>📅 投稿日時の予約設定 ＆ 配信先</span>
          </div>
          <div style="margin-bottom: 8px; display: flex; align-items: center; gap: 8px;">
            <label style="font-size: 11.5px; font-weight: 700; color: var(--text-muted);">配信先:</label>
            <select id="modalPlatformSelect" class="category-select" style="width: auto; min-width: 190px;">
              <option value="threads">🧵 Threads のみ</option>
              <option value="linkedin">💼 LinkedIn のみ</option>
              <option value="both">🚀 Threads ＆ LinkedIn 両方</option>
            </select>
          </div>
          <div class="schedule-row">
            <input type="datetime-local" id="modalScheduleInput" class="schedule-input">
            <button class="btn btn-primary" onclick="saveScheduleTime()">予約日時を設定</button>
            <button id="modalClearScheduleBtn" class="btn" style="display: none;" onclick="clearScheduleTime()">予約解除</button>
          </div>
          <div style="font-size: 11px; color: var(--text-muted);">
            ※ 予約日時に設定すると「予約中」ステータスになり、自動投稿ワーカーの対象になります。投稿直前まで変更可能です。
          </div>
        </div>

        <!-- インサイト表示エリア（投稿済みの場合） -->
        <div id="modalInsightsBox" class="schedule-box" style="display: none; background: #ecfdf5; border-color: #a7f3d0;">
          <div class="schedule-title" style="color: #047857;">
            <span>📊 Threads インサイト（リアクション・閲覧数）</span>
          </div>
          <div id="modalInsightsDetail" style="font-size: 12px; color: #065f46; display: flex; gap: 12px; flex-wrap: wrap;"></div>
        </div>
      </div>

      <div class="modal-footer" style="flex-wrap: wrap;">
        <div style="display: flex; gap: 6px; flex-wrap: wrap;">
          <button class="btn" onclick="copyModalText()">📋 コピー</button>
          <a id="modalThreadsIntentBtn" href="#" target="_blank" rel="noopener noreferrer" class="btn" style="background: #0f172a; color: #fff; border-color: #0f172a;">
            🧵 Threadsで投稿<span id="modalThreadsRecBadge" class="rec-badge" style="display: none;">推奨</span>
          </a>
          <a id="modalLinkedInIntentBtn" href="#" target="_blank" rel="noopener noreferrer" class="btn" style="background: #0a66c2; color: #fff; border-color: #0a66c2;">
            💼 LinkedInで投稿<span id="modalLinkedInRecBadge" class="rec-badge" style="display: none;">推奨</span>
          </a>
          <a id="modalXIntentBtn" href="#" target="_blank" rel="noopener noreferrer" class="btn" style="background: #111827; color: #fff; border-color: #111827;">
            𝕏 Xで投稿<span id="modalXRecBadge" class="rec-badge" style="display: none;">推奨</span>
          </a>
        </div>
        <div style="display: flex; gap: 6px; flex-wrap: wrap;">
          <button id="modalTogglePublishBtn" class="btn" onclick="togglePublishFromModal()">
            ✅ 投稿済みにする
          </button>
          <button class="btn btn-primary" onclick="saveContentEdit()">💾 保存する</button>
        </div>
      </div>
    </div>
  </div>

  <!-- ランダム一括自動予約モーダル -->
  <div id="bulkModalOverlay" class="modal-overlay" onclick="if(event.target.id==='bulkModalOverlay') closeBulkModal()">
    <div class="modal-box" onclick="event.stopPropagation()" style="max-width: 460px;">
      <div class="modal-header">
        <div class="modal-title-group">
          <span style="font-weight: 800; font-size: 15px; color: #0f766e;">🎲 ランダム一括自動予約</span>
        </div>
        <button class="modal-close" onclick="closeBulkModal()">&times;</button>
      </div>
      <div class="modal-body" style="gap: 14px;">
        <p style="font-size: 12.5px; color: var(--text-muted); line-height: 1.5;">
          「ストック（未予約・未投稿）」の中から各ジャンルが偏らないようにランダム選出し、明日から毎日指定時刻に自動投稿予約をセットします。
        </p>
        <div>
          <label style="font-size: 12px; font-weight: 700; display: block; margin-bottom: 4px;">予約する日数</label>
          <select id="bulkDaysSelect" class="category-select">
            <option value="7">7日分（1週間）</option>
            <option value="14">14日分（2週間）</option>
            <option value="30">30日分（約1ヶ月）</option>
          </select>
        </div>
        <div>
          <label style="font-size: 12px; font-weight: 700; display: block; margin-bottom: 4px;">毎日の投稿時刻</label>
          <input type="time" id="bulkTimeInput" class="schedule-input" value="08:00" style="width: 100%;">
        </div>
        <div>
          <label style="font-size: 12px; font-weight: 700; display: block; margin-bottom: 4px;">配信先プラットフォーム</label>
          <select id="bulkPlatformSelect" class="category-select">
            <option value="threads">🧵 Threads のみ</option>
            <option value="both">🚀 Threads ＆ LinkedIn 両方</option>
            <option value="linkedin">💼 LinkedIn のみ</option>
          </select>
        </div>
      </div>
      <div class="modal-footer" style="justify-content: flex-end;">
        <button class="btn" onclick="closeBulkModal()">キャンセル</button>
        <button class="btn btn-primary" onclick="executeBulkSchedule()">一括予約を実行する</button>
      </div>
    </div>
  </div>

  <script>
    // Firebase Config
    const firebaseConfig = {firebase_config_json};
    
    // Category Color Mapping
    const CAT_CLASSES = {{
      '実習・教育の本音': 'cat-edu',
      '医療教育DX・業務効率化': 'cat-dx',
      'PTのキャリア・未来': 'cat-career',
      '臨床思考・リハビリのリアル': 'cat-clinical',
      '教員室のつぶやき・マインド': 'cat-mind',
      '学校経営・教育ガバナンスDX': 'cat-gov'
    }};

    const PLATFORM_LABELS = {{
      'threads': '🧵 Threads',
      'linkedin': '💼 LinkedIn',
      'both': '🚀 Threads+LI'
    }};

    const RECOMMENDED_BY_CATEGORY = {{
      '実習・教育の本音': ['threads', 'x'],
      '臨床思考・リハビリのリアル': ['threads', 'x'],
      '教員室のつぶやき・マインド': ['threads', 'x'],
      '医療教育DX・業務効率化': ['threads', 'linkedin', 'x'],
      'PTのキャリア・未来': ['threads', 'linkedin', 'x'],
      '学校経営・教育ガバナンスDX': ['linkedin']
    }};

    let postsData = [];
    let currentStatusFilter = 'all';
    let currentModalDocId = null;
    let db = null;

    // Initialize Firebase
    try {{
      if (firebaseConfig.apiKey) {{
        firebase.initializeApp(firebaseConfig);
        db = firebase.firestore();
        initFirestoreListener();
      }} else {{
        showToast('Firebase 設定が見つかりません');
      }}
    }} catch (e) {{
      console.error('Firebase init error:', e);
      document.getElementById('syncText').textContent = '同期エラー';
    }}

    function initFirestoreListener() {{
      const syncDot = document.getElementById('syncDot');
      const syncText = document.getElementById('syncText');

      db.collection('posts').onSnapshot((snapshot) => {{
        syncDot.classList.add('connected');
        syncText.textContent = '同期完了 (リアルタイム)';

        const loaded = [];
        snapshot.forEach(doc => {{
          const data = doc.data();
          loaded.push({{
            id: doc.id,
            ...data
          }});
        }});

        // Sort by dayNumber
        loaded.sort((a, b) => (a.dayNumber || 0) - (b.dayNumber || 0));
        postsData = loaded;

        updateCountsAndProgress();
        renderPosts();

        // If modal is open, refresh modal view
        if (currentModalDocId) {{
          const item = postsData.find(p => p.id === currentModalDocId);
          if (item) populateModal(item);
        }}
      }}, (error) => {{
        console.error('Firestore listener error:', error);
        syncDot.classList.remove('connected');
        syncText.textContent = '同期切断';
      }});
    }}

    function updateCountsAndProgress() {{
      let stock = 0, scheduled = 0, published = 0;
      postsData.forEach(p => {{
        const st = p.status || 'stock';
        if (st === 'published') published++;
        else if (st === 'scheduled') scheduled++;
        else stock++;
      }});

      document.getElementById('countAll').textContent = postsData.length;
      document.getElementById('countStock').textContent = stock;
      document.getElementById('countScheduled').textContent = scheduled;
      document.getElementById('countPublished').textContent = published;

      const total = postsData.length || 100;
      const pct = Math.round((published / total) * 100);
      document.getElementById('progressText').textContent = `${{published}} / ${{total}} 完了 (${{pct}}%)`;
      document.getElementById('progressBar').style.width = `${{pct}}%`;
    }}

    function setStatusFilter(status) {{
      currentStatusFilter = status;
      document.querySelectorAll('.tab-btn').forEach(btn => {{
        btn.classList.toggle('active', btn.dataset.filter === status);
      }});
      renderPosts();
    }}

    function renderPosts() {{
      const container = document.getElementById('postsContainer');
      const searchWord = document.getElementById('searchInput').value.trim().toLowerCase();
      const selectedCat = document.getElementById('catFilter').value;

      const filtered = postsData.filter(p => {{
        const st = p.status || 'stock';
        if (currentStatusFilter !== 'all' && st !== currentStatusFilter) return false;
        if (selectedCat !== 'all' && p.category !== selectedCat) return false;
        if (searchWord) {{
          const text = (p.day + ' ' + p.category + ' ' + (p.content || '')).toLowerCase();
          if (!text.includes(searchWord)) return false;
        }}
        return true;
      }});

      if (currentStatusFilter === 'scheduled') {{
        filtered.sort((a, b) => {{
          const ta = a.scheduledAt ? new Date(a.scheduledAt).getTime() : Number.MAX_SAFE_INTEGER;
          const tb = b.scheduledAt ? new Date(b.scheduledAt).getTime() : Number.MAX_SAFE_INTEGER;
          return ta !== tb ? ta - tb : (a.dayNumber || 0) - (b.dayNumber || 0);
        }});
      }} else if (currentStatusFilter === 'published') {{
        filtered.sort((a, b) => {{
          const ta = a.publishedAt ? new Date(a.publishedAt).getTime() : 0;
          const tb = b.publishedAt ? new Date(b.publishedAt).getTime() : 0;
          return tb !== ta ? tb - ta : (a.dayNumber || 0) - (b.dayNumber || 0);
        }});
      }}

      if (filtered.length === 0) {{
        container.innerHTML = '<div style="text-align: center; padding: 40px; color: #94a3b8; grid-column: 1/-1;">該当する投稿はありません</div>';
        return;
      }}

      container.innerHTML = filtered.map(item => {{
        const catClass = CAT_CLASSES[item.category] || 'cat-edu';
        const st = item.status || 'stock';
        const isPublished = st === 'published';
        const isScheduled = st === 'scheduled';

        let statusBadgeHtml = '<span class="status-badge badge-stock">📝 ストック</span>';
        if (isPublished) {{
          const pubTimeStr = item.publishedAt ? ` (${{formatDateTime(item.publishedAt)}})` : '';
          statusBadgeHtml = `<span class="status-badge badge-published">✅ 投稿済み${{pubTimeStr}}</span>`;
        }} else if (isScheduled) {{
          const timeStr = item.scheduledAt ? formatDateTime(item.scheduledAt) : '日時未設定';
          statusBadgeHtml = `<span class="status-badge badge-scheduled">📅 予約: ${{timeStr}}</span>`;
        }}

        // Insights HTML
        let insightsHtml = '';
        if (isPublished && item.insights && (item.insights.views || item.insights.likes)) {{
          insightsHtml = `
            <div class="insights-row">
              <span class="insight-item">👁️ ${{item.insights.views || 0}}</span>
              <span class="insight-item">❤️ ${{item.insights.likes || 0}}</span>
              <span class="insight-item">💬 ${{item.insights.replies || 0}}</span>
              <span class="insight-item">🔁 ${{item.insights.reposts || 0}}</span>
            </div>
          `;
        }}

        const pTarget = item.platforms || 'threads';
        const pLabel = PLATFORM_LABELS[pTarget] || '🧵 Threads';

        return `
          <div class="post-card status-${{st}}" id="card-${{item.id}}">
            <div class="post-card-top">
              <div class="post-badges">
                <span class="day-badge">${{item.day}}</span>
                <span class="cat-badge ${{catClass}}">${{item.category}}</span>
                <span class="platform-badge">${{pLabel}}</span>
              </div>
              <div>${{statusBadgeHtml}}</div>
            </div>

            <div class="post-body" onclick="openModal('${{item.id}}')">${{escapeHtml(item.content)}}</div>

            ${{insightsHtml}}

            <div class="card-footer">
              <label class="check-toggle">
                <input type="checkbox" ${{isPublished ? 'checked' : ''}} onchange="togglePublish('${{item.id}}', this.checked)">
                <span>${{isPublished ? '投稿完了' : '投稿済みにする'}}</span>
              </label>

              <button class="edit-btn" onclick="openModal('${{item.id}}')">
                ✏️ 編集・予約
              </button>
            </div>
          </div>
        `;
      }}).join('');
    }}

    function formatDateTime(isoStr) {{
      if (!isoStr) return '';
      const d = new Date(isoStr);
      const m = d.getMonth() + 1;
      const day = d.getDate();
      const h = String(d.getHours()).padStart(2, '0');
      const min = String(d.getMinutes()).padStart(2, '0');
      return `${{m}}/${{day}} ${{h}}:${{min}}`;
    }}

    function escapeHtml(str) {{
      if (!str) return '';
      return str.replace(/&/g, '&amp;')
                .replace(/</g, '&lt;')
                .replace(/>/g, '&gt;')
                .replace(/"/g, '&quot;');
    }}

    // Modal Operations
    function openModal(docId) {{
      currentModalDocId = docId;
      const item = postsData.find(p => p.id === docId);
      if (!item) return;

      populateModal(item);
      document.getElementById('modalOverlay').classList.add('active');
    }}

    function populateModal(item) {{
      document.getElementById('modalDayBadge').textContent = item.day;
      const catBadge = document.getElementById('modalCatBadge');
      catBadge.textContent = item.category;
      catBadge.className = `cat-badge ${{CAT_CLASSES[item.category] || 'cat-edu'}}`;

      const st = item.status || 'stock';
      const stBadge = document.getElementById('modalStatusBadge');
      if (st === 'published') {{
        stBadge.className = 'status-badge badge-published';
        stBadge.textContent = '✅ 投稿済み';
      }} else if (st === 'scheduled') {{
        stBadge.className = 'status-badge badge-scheduled';
        stBadge.textContent = '📅 予約中';
      }} else {{
        stBadge.className = 'status-badge badge-stock';
        stBadge.textContent = '📝 ストック';
      }}

      // Textarea
      const textarea = document.getElementById('modalEditTextarea');
      textarea.value = item.content || '';
      updateModalCharCount();

      // Platform Select & Recommended Badges
      document.getElementById('modalPlatformSelect').value = item.platforms || 'threads';
      const recList = RECOMMENDED_BY_CATEGORY[item.category] || [item.platforms || 'threads'];
      document.getElementById('modalThreadsRecBadge').style.display = recList.includes('threads') ? 'inline-block' : 'none';
      document.getElementById('modalLinkedInRecBadge').style.display = recList.includes('linkedin') ? 'inline-block' : 'none';
      document.getElementById('modalXRecBadge').style.display = recList.includes('x') ? 'inline-block' : 'none';

      // Schedule Input
      const scheduleInput = document.getElementById('modalScheduleInput');
      const clearBtn = document.getElementById('modalClearScheduleBtn');
      if (item.scheduledAt) {{
        // Format ISO to YYYY-MM-DDTHH:MM for datetime-local
        const d = new Date(item.scheduledAt);
        const yyyy = d.getFullYear();
        const mm = String(d.getMonth() + 1).padStart(2, '0');
        const dd = String(d.getDate()).padStart(2, '0');
        const hh = String(d.getHours()).padStart(2, '0');
        const min = String(d.getMinutes()).padStart(2, '0');
        scheduleInput.value = `${{yyyy}}-${{mm}}-${{dd}}T${{hh}}:${{min}}`;
        clearBtn.style.display = 'inline-block';
      }} else {{
        scheduleInput.value = '';
        clearBtn.style.display = 'none';
      }}

      // Intent links
      updateIntentLinks(item.content || '');

      // Toggle publish button text
      const toggleBtn = document.getElementById('modalTogglePublishBtn');
      toggleBtn.textContent = (st === 'published') ? '↩️ 未投稿に戻す' : '✅ 投稿済みにする';

      // Insights box
      const insightsBox = document.getElementById('modalInsightsBox');
      const insightsDetail = document.getElementById('modalInsightsDetail');
      if (st === 'published' && item.insights && (item.insights.views || item.insights.likes)) {{
        insightsBox.style.display = 'block';
        insightsDetail.innerHTML = `
          <span>👁️ 閲覧数: <strong>${{item.insights.views || 0}}</strong></span>
          <span>❤️ いいね: <strong>${{item.insights.likes || 0}}</strong></span>
          <span>💬 返信: <strong>${{item.insights.replies || 0}}</strong></span>
          <span>🔁 再投稿: <strong>${{item.insights.reposts || 0}}</strong></span>
        `;
      }} else {{
        insightsBox.style.display = 'none';
      }}
    }}

    function closeModal(e) {{
      if (e.target.id === 'modalOverlay') closeModalDirect();
    }}

    function closeModalDirect() {{
      document.getElementById('modalOverlay').classList.remove('active');
      currentModalDocId = null;
    }}

    function updateIntentLinks(text) {{
      const encoded = encodeURIComponent(text || '');
      document.getElementById('modalThreadsIntentBtn').href = `https://www.threads.net/intent/post?text=${{encoded}}`;
      document.getElementById('modalLinkedInIntentBtn').href = `https://www.linkedin.com/feed/?shareActive=true&text=${{encoded}}`;
      document.getElementById('modalXIntentBtn').href = `https://twitter.com/intent/tweet?text=${{encoded}}`;
    }}

    function updateModalCharCount() {{
      const val = document.getElementById('modalEditTextarea').value;
      const xNote = val.length > 140 ? 'X: 140文字超過' : 'X: 140文字以内';
      document.getElementById('modalCharCount').textContent = `${{val.length}} 文字 (Threads上限: 500文字 / ${{xNote}})`;
      updateIntentLinks(val);
    }}

    document.addEventListener('keydown', (e) => {{
      if (e.key === 'Escape') {{
        closeModalDirect();
        closeBulkModal();
      }}
    }});

    function copyModalText() {{
      const text = document.getElementById('modalEditTextarea').value;
      copyToClipboard(text);
    }}

    function saveContentEdit() {{
      if (!currentModalDocId || !db) return;
      const text = document.getElementById('modalEditTextarea').value;
      const platform = document.getElementById('modalPlatformSelect').value;

      db.collection('posts').doc(currentModalDocId).update({{
        content: text,
        platforms: platform
      }}).then(() => {{
        showToast('変更内容をクラウドに保存しました！');
      }}).catch(err => {{
        alert('保存に失敗しました: ' + err.message);
      }});
    }}

    function saveScheduleTime() {{
      if (!currentModalDocId || !db) return;
      const val = document.getElementById('modalScheduleInput').value;
      if (!val) {{
        alert('予約日時を選択してください');
        return;
      }}

      // convert to ISO string
      const isoStr = new Date(val).toISOString();
      const platform = document.getElementById('modalPlatformSelect').value;

      db.collection('posts').doc(currentModalDocId).update({{
        scheduledAt: isoStr,
        platforms: platform,
        status: 'scheduled'
      }}).then(() => {{
        showToast('予約日時を設定しました 📅');
        closeModalDirect();
      }}).catch(err => {{
        alert('予約設定に失敗しました: ' + err.message);
      }});
    }}

    function clearScheduleTime() {{
      if (!currentModalDocId || !db) return;
      db.collection('posts').doc(currentModalDocId).update({{
        scheduledAt: null,
        status: 'stock'
      }}).then(() => {{
        showToast('予約を解除しストックに戻しました');
      }}).catch(err => {{
        alert('解除に失敗しました: ' + err.message);
      }});
    }}

    function togglePublish(docId, isPublished) {{
      if (!db) return;
      const newStatus = isPublished ? 'published' : 'stock';
      const updateObj = {{ status: newStatus }};
      if (isPublished) {{
        updateObj.publishedAt = new Date().toISOString();
      }}

      db.collection('posts').doc(docId).update(updateObj).then(() => {{
        showToast(isPublished ? '投稿済みに更新しました ✅' : '未投稿に戻しました');
      }}).catch(err => {{
        alert('更新に失敗しました: ' + err.message);
      }});
    }}

    function togglePublishFromModal() {{
      if (!currentModalDocId) return;
      const item = postsData.find(p => p.id === currentModalDocId);
      if (!item) return;
      const willPublish = (item.status !== 'published');
      togglePublish(currentModalDocId, willPublish);
    }}

    function openRandomPicker() {{
      const unposted = postsData.filter(p => (p.status || 'stock') !== 'published');
      const pool = unposted.length > 0 ? unposted : postsData;
      if (pool.length === 0) return;
      const picked = pool[Math.floor(Math.random() * pool.length)];
      openModal(picked.id);
    }}

    function openBulkScheduleModal() {{
      document.getElementById('bulkModalOverlay').classList.add('active');
    }}

    function closeBulkModal() {{
      document.getElementById('bulkModalOverlay').classList.remove('active');
    }}

    function executeBulkSchedule() {{
      if (!db) return;
      const days = parseInt(document.getElementById('bulkDaysSelect').value, 10);
      const timeStr = document.getElementById('bulkTimeInput').value || '08:00';
      const platform = document.getElementById('bulkPlatformSelect').value;

      const stockPosts = postsData.filter(p => (p.status || 'stock') === 'stock');
      if (stockPosts.length === 0) {{
        alert('予約可能な「ストック」状態の投稿がありません。');
        return;
      }}

      // ジャンル偏りを防ぐため、カテゴリごとにシャッフルしてラウンドロビンで選出
      const byCat = {{}};
      stockPosts.forEach(p => {{
        const c = p.category || 'その他';
        if (!byCat[c]) byCat[c] = [];
        byCat[c].push(p);
      }});
      Object.values(byCat).forEach(arr => {{
        for (let i = arr.length - 1; i > 0; i--) {{
          const j = Math.floor(Math.random() * (i + 1));
          [arr[i], arr[j]] = [arr[j], arr[i]];
        }}
      }});

      const catKeys = Object.keys(byCat);
      for (let i = catKeys.length - 1; i > 0; i--) {{
        const j = Math.floor(Math.random() * (i + 1));
        [catKeys[i], catKeys[j]] = [catKeys[j], catKeys[i]];
      }}

      const selected = [];
      let idx = 0;
      while (selected.length < days) {{
        let addedInRound = false;
        for (const k of catKeys) {{
          if (byCat[k].length > 0 && selected.length < days) {{
            selected.push(byCat[k].pop());
            addedInRound = true;
          }}
        }}
        if (!addedInRound) break;
        idx++;
      }}

      const [hh, mm] = timeStr.split(':').map(Number);
      const batch = db.batch();
      const now = new Date();

      selected.forEach((post, i) => {{
        const targetDate = new Date(now.getFullYear(), now.getMonth(), now.getDate() + i + 1, hh, mm, 0);
        const ref = db.collection('posts').doc(post.id);
        batch.update(ref, {{
          status: 'scheduled',
          scheduledAt: targetDate.toISOString(),
          platforms: platform
        }});
      }});

      batch.commit().then(() => {{
        closeBulkModal();
        showToast(`${{selected.length}}日分のランダム予約を自動設定しました 🎉`);
      }}).catch(err => {{
        alert('一括予約に失敗しました: ' + err.message);
      }});
    }}

    function copyToClipboard(text) {{
      navigator.clipboard.writeText(text).then(() => {{
        showToast('本文をコピーしました！Threadsに貼り付けられます');
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
      }}, 2400);
    }}
  </script>
</body>
</html>
'''

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print("Successfully built index.html with Firebase Firestore integration!")

if __name__ == '__main__':
    generate_app()
