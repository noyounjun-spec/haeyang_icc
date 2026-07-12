<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>해양경찰 심해의 기록자</title>
    <script src="https://unpkg.com/html5-qrcode"></script>
    <style>
        body { font-family: 'Malgun Gothic', sans-serif; background-color: #f0f8ff; margin: 0; padding: 10px; text-align: center; padding-bottom: 50px; color: #333; }
        h2 { color: #003366; margin-bottom: 5px; }
        .desc { font-size: 14px; color: #555; margin-bottom: 20px; }

        /* 인증 및 메인 UI */
        .auth-container { max-width: 300px; margin: 30px auto; background: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        .auth-input { width: 90%; padding: 10px; margin: 10px 0; border: 1px solid #ccc; border-radius: 5px; box-sizing: border-box; }
        .auth-btn { background: #003366; color: white; border: none; padding: 12px; border-radius: 5px; width: 100%; font-weight: bold; cursor: pointer; margin-top: 10px; }
        .reset-btn { background: #dc3545; color: white; border: none; padding: 10px; border-radius: 5px; width: 100%; font-size: 12px; cursor: pointer; margin-top: 20px; }

        #appContainer { display: none; }
        .header-bar { display: flex; justify-content: space-between; align-items: center; padding: 10px 20px; background: white; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 10px; font-size: 14px; font-weight: bold;}
        .logout-btn { background: #dc3545; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer; font-size: 12px; }
        #startScannerBtn { background: #ff9900; color: white; border: none; padding: 15px; border-radius: 10px; width: 100%; max-width: 400px; font-size: 18px; font-weight: bold; cursor: pointer; margin-bottom: 20px; }
        #reader { width: 100%; max-width: 400px; margin: 0 auto; border-radius: 10px; overflow: hidden; display: none; }

        /* 도감 진행률 */
        .progress-bar-wrap { max-width: 400px; margin: 0 auto 20px; background: white; border-radius: 10px; padding: 10px 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .progress-text { font-size: 13px; font-weight: bold; color: #003366; margin-bottom: 6px; }
        .progress-track { width: 100%; height: 10px; background: #e0e8f0; border-radius: 10px; overflow: hidden; }
        .progress-fill { height: 100%; background: linear-gradient(90deg,#0066cc,#00b4d8); transition: width 0.4s; }

        .gallery { display: flex; flex-wrap: wrap; justify-content: center; gap: 10px; margin-top: 20px; }
        .character-card { position: relative; width: 100px; height: 140px; background: white; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 5px; border: 2px solid transparent; }
        .character-img { width: 75px; height: 75px; object-fit: contain; filter: grayscale(100%); opacity: 0.3; transition: 0.5s; border-radius: 8px; background:#f2f2f2; }
        .character-img.active { filter: grayscale(0%); opacity: 1; }
        .char-name { font-size: 11px; font-weight: bold; margin-top: 5px; text-align: center; word-break: keep-all; }
        .char-rarity-badge { position: absolute; top: 4px; right: 4px; font-size: 9px; font-weight: bold; padding: 2px 5px; border-radius: 6px; color: white; }
        .dup-count { font-size: 10px; color: #888; margin-top: 2px; }

        #storyModal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.9); z-index: 1000; overflow-y: auto; }
        .modal-content { position: relative; margin: 10% auto; background: white; color: #333; padding: 20px; border-radius: 15px; width: 90%; max-width: 400px; text-align: center; }
        .video-wrapper { position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; background: #000; margin-bottom: 15px; }
        .video-wrapper iframe { position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none; }
        .action-btn { background: #0056b3; color: white; border: none; padding: 15px; border-radius: 8px; width: 100%; font-size: 16px; font-weight: bold; cursor: pointer; }
        .reward-img { width: 180px; height: 180px; object-fit: contain; margin: 0 auto 10px; border-radius: 12px; background:#f2f2f2; }
        .reward-rarity { display:inline-block; font-size: 13px; font-weight:bold; padding: 4px 12px; border-radius: 20px; color:white; margin-bottom: 10px; }
        .reward-new-tag { font-size: 13px; color:#28a745; font-weight:bold; margin-bottom: 8px; }
        .reward-dup-tag { font-size: 13px; color:#888; font-weight:bold; margin-bottom: 8px; }
        .demo-qr-section { margin-top: 50px; padding-top: 20px; border-top: 2px dashed #bbb; display: none; }
        .qr-grid { display: flex; flex-wrap: wrap; justify-content: center; gap: 15px; margin-top: 15px; }
    </style>
</head>
<body>

    <div id="authWrap">
        <h2>🌊 심해의 기록자</h2>
        <div id="loginBox" class="auth-container">
            <h3>로그인</h3>
            <input type="text" id="loginId" class="auth-input" placeholder="아이디">
            <input type="password" id="loginPw" class="auth-input" placeholder="비밀번호">
            <button class="auth-btn" onclick="login()">로그인</button>
            <button class="reset-btn" onclick="hardReset()">전체 데이터 초기화</button>
        </div>
    </div>

    <div id="appContainer">
        <div class="header-bar">
            <span id="welcomeMsg"></span>
            <button class="logout-btn" onclick="logout()">로그아웃</button>
        </div>
        <button id="startScannerBtn" onclick="startScanner()">📷 QR 스캐너 켜기</button>
        <div id="reader"></div>

        <div class="progress-bar-wrap">
            <div class="progress-text" id="progressText">수집한 캐릭터: 0 / 63</div>
            <div class="progress-track"><div class="progress-fill" id="progressFill" style="width:0%"></div></div>
        </div>

        <div class="gallery" id="galleryContainer"></div>

        <div class="demo-qr-section" id="demoQrArea">
            <h3>🖥️ 데모 테스트용 QR</h3>
            <div class="desc">아래 QR을 스캐너로 찍으면 스토리 영상 후 캐릭터를 랜덤 획득합니다.</div>
            <div class="qr-grid">
                <div class="qr-item"><img src="https://api.qrserver.com/v1/create-qr-code/?size=80x80&data=QR_JUNGBU"><br><small>중부</small></div>
                <div class="qr-item"><img src="https://api.qrserver.com/v1/create-qr-code/?size=80x80&data=QR_SEOHAE"><br><small>서해</small></div>
                <div class="qr-item"><img src="https://api.qrserver.com/v1/create-qr-code/?size=80x80&data=QR_NAMHAE"><br><small>남해</small></div>
                <div class="qr-item"><img src="https://api.qrserver.com/v1/create-qr-code/?size=80x80&data=QR_DONGHAE"><br><small>동해</small></div>
                <div class="qr-item"><img src="https://api.qrserver.com/v1/create-qr-code/?size=80x80&data=QR_JEJU"><br><small>제주</small></div>
                <div class="qr-item"><img src="https://api.qrserver.com/v1/create-qr-code/?size=80x80&data=QR_MAIN"><br><small>본청</small></div>
            </div>
            <button class="reset-btn" onclick="hardReset()" style="margin-top:20px;">시스템 전체 데이터 초기화</button>
        </div>
    </div>

    <div id="storyModal">
        <div class="modal-content">
            <div id="step1">
                <div id="modalTitle" style="font-size:20px; font-weight:bold; margin-bottom:10px;"></div>
                <div class="video-wrapper"><iframe id="modalVideo" src="" allow="autoplay"></iframe></div>
                <div id="modalText" style="margin-bottom:20px; font-size:14px; text-align:left;"></div>
                <button class="action-btn" onclick="showReward()">보상 획득하기!</button>
            </div>
            <div id="step2" style="display: none;">
                <h3 style="color:#ff9900;">🎉 캐릭터 획득!</h3>
                <img id="rewardImg" class="reward-img" src="">
                <div><span id="rewardRarity" class="reward-rarity"></span></div>
                <div id="rewardName" style="font-size:16px; font-weight:bold; margin-bottom:6px;"></div>
                <div id="rewardStatus"></div>
                <button class="action-btn" onclick="closeModal()">도감에 추가</button>
            </div>
        </div>
    </div>

<script>
    /* =========================================================
       QR → 스토리/영상 매핑 (기존 6개 지역 QR 그대로 유지)
       QR을 찍으면 이 스토리/영상이 먼저 나오고,
       "보상 획득하기" 버튼을 누르면 아래 CHARACTERS 풀에서
       희귀도 가중치로 캐릭터 1개를 랜덤 추첨합니다.
    ========================================================= */
    const db = {
        "QR_JUNGBU": { title: "수도권 해양 오염 방제", story: "필리핀 기름 유출 현장까지 파견된 해경! 세계의 바다를 지키는 해양경찰의 땀방울을 확인하세요.", videoId: "jRX3fezEFIE" },
        "QR_SEOHAE": { title: "불법 조업 어선 단속", story: "거친 파도를 뚫고 불법 조업 어선을 단속하는 실제 바디캠 영상입니다. 어민들의 소중한 생업을 지킵니다.", videoId: "p0N1MhwUgmo" },
        "QR_NAMHAE": { title: "해상 조난 선박 구조", story: "부상을 딛고 다시 바다로 돌아간 김진영 대원! 국민의 생명을 구하기 위한 헌신과 열정을 만나보세요.", videoId: "gE7VunbFeHw" },
        "QR_DONGHAE":{ title: "해양 레저 안전 확보", story: "일촉즉발의 상황! 거친 파도 속 표류자를 구출하는 현장 바디캠입니다. 든든한 해상 순찰로 안전을 책임집니다.", videoId: "OEUUeHKepco" },
        "QR_JEJU":   { title: "해양 생태계 보호", story: "제주의 아름다운 바다와 생태계를 지키는 해양경찰의 또 다른 활약상! 생명 존중의 가치를 실천합니다.", videoId: "7CwtSgJvFdM" },
        "QR_MAIN":   { title: "해양 안전 캠페인", story: "바다의 안전은 구명조끼부터! 해양경찰과 함께하는 안전한 바다 만들기 캠페인에 동참해 주셔서 감사합니다.", videoId: "9XLddsY_KQI" }
    };

    /* =========================================================
       ▼▼▼ 캐릭터 63개 등록 자리 (여기에 직접 추가하세요) ▼▼▼
       - id: 고유 번호 (중복 금지)
       - name: 도감에 표시될 이름
       - img: 이미지 파일 경로 (예: "characters/01_구명조끼.png")
              → 이미지 파일을 웹사이트 폴더의 characters/ 안에 넣고
                파일명만 맞춰서 img 값을 채워주세요.
       - rarity: "common"(일반) | "rare"(레어) | "epic"(에픽) | "legendary"(레전더리)
                 희귀할수록 나올 확률이 낮아집니다 (아래 RARITY_WEIGHT 참고)
    ========================================================= */
    const CHARACTERS = [
        // ---- 일반 (common) : 25개 ----
        { id: 1,  name: "요리사 아치",         img: "characters/01.png", rarity: "common" },
        { id: 2,  name: "학생 아치",           img: "characters/02.png", rarity: "common" },
        { id: 3,  name: "뮤지션 아치",         img: "characters/03.png", rarity: "common" },
        { id: 4,  name: "소방관 아치",         img: "characters/04.png", rarity: "common" },
        { id: 5,  name: "축구선수 아치",       img: "characters/05.png", rarity: "common" },
        { id: 6,  name: "택배기사 아치",       img: "characters/06.png", rarity: "common" },
        { id: 7,  name: "농부 아치",           img: "characters/07.png", rarity: "common" },
        { id: 8,  name: "바리스타 아치",       img: "characters/08.png", rarity: "common" },
        { id: 9,  name: "화가 아치",           img: "characters/09.png", rarity: "common" },
        { id: 10, name: "사진작가 아치",       img: "characters/10.png", rarity: "common" },
        { id: 11, name: "라이프가드 아치",     img: "characters/11.png", rarity: "common" },
        { id: 12, name: "우비 입은 아치",      img: "characters/12.png", rarity: "common" },
        { id: 13, name: "선원 아치",           img: "characters/13.png", rarity: "common" },
        { id: 14, name: "꽃집 아치",           img: "characters/14.png", rarity: "common" },
        { id: 15, name: "사진작가 아치 (야외)",img: "characters/15.png", rarity: "common" },
        { id: 16, name: "바리스타 아치 (매장)",img: "characters/16.png", rarity: "common" },
        { id: 17, name: "화가 아치 (스케치)",  img: "characters/17.png", rarity: "common" },
        { id: 18, name: "잠옷 입은 아치",      img: "characters/18.png", rarity: "common" },
        { id: 19, name: "우체부 아치",         img: "characters/19.png", rarity: "common" },
        { id: 20, name: "농부 아치 (텃밭)",    img: "characters/20.png", rarity: "common" },
        { id: 21, name: "소방관 아치 (출동)",  img: "characters/21.png", rarity: "common" },
        { id: 22, name: "건설 아치",           img: "characters/22.png", rarity: "common" },
        { id: 23, name: "배달 아치",           img: "characters/23.png", rarity: "common" },
        { id: 24, name: "라이프가드 아치 (해변)", img: "characters/24.png", rarity: "common" },
        { id: 25, name: "가드너 아치",         img: "characters/25.png", rarity: "common" },

        // ---- 레어 (rare) : 20개 ----
        { id: 26, name: "구명조끼 아치",       img: "characters/26.png", rarity: "rare" },
        { id: 27, name: "봄 벚꽃 아치",        img: "characters/27.png", rarity: "rare" },
        { id: 28, name: "여름 바캉스 아치",    img: "characters/28.png", rarity: "rare" },
        { id: 29, name: "가을 단풍 아치",      img: "characters/29.png", rarity: "rare" },
        { id: 30, name: "겨울 눈사람 아치",    img: "characters/30.png", rarity: "rare" },
        { id: 31, name: "스쿠버 다이버 아치",  img: "characters/31.png", rarity: "rare" },
        { id: 32, name: "잠수부 아치",         img: "characters/32.png", rarity: "rare" },
        { id: 33, name: "의사 아치",           img: "characters/33.png", rarity: "rare" },
        { id: 34, name: "수의사 아치",         img: "characters/34.png", rarity: "rare" },
        { id: 35, name: "한복 입은 아치",      img: "characters/35.png", rarity: "rare" },
        { id: 36, name: "한복 입은 아치 (전통)", img: "characters/36.png", rarity: "rare" },
        { id: 37, name: "탐정 아치",           img: "characters/37.png", rarity: "rare" },
        { id: 38, name: "탐정 아치 (돋보기)",  img: "characters/38.png", rarity: "rare" },
        { id: 39, name: "공룡 옷 입은 아치",   img: "characters/39.png", rarity: "rare" },
        { id: 40, name: "셰프 아치",           img: "characters/40.png", rarity: "rare" },
        { id: 41, name: "양봉가 아치",         img: "characters/41.png", rarity: "rare" },
        { id: 42, name: "과학자 아치",         img: "characters/42.png", rarity: "rare" },
        { id: 43, name: "DJ 아치",             img: "characters/43.png", rarity: "rare" },
        { id: 44, name: "게이머 아치",         img: "characters/44.png", rarity: "rare" },
        { id: 45, name: "골프선수 아치",       img: "characters/45.png", rarity: "rare" },

        // ---- 에픽 (epic) : 12개 ----
        { id: 46, name: "크리스마스 산타 아치",img: "characters/46.png", rarity: "epic" },
        { id: 47, name: "할로윈 마법사 아치",  img: "characters/47.png", rarity: "epic" },
        { id: 48, name: "마법사 아치",         img: "characters/48.png", rarity: "epic" },
        { id: 49, name: "사무라이 아치",       img: "characters/49.png", rarity: "epic" },
        { id: 50, name: "스님 아치",           img: "characters/50.png", rarity: "epic" },
        { id: 51, name: "요정 아치",           img: "characters/51.png", rarity: "epic" },
        { id: 52, name: "해양경찰 제복 아치",  img: "characters/52.png", rarity: "epic" },
        { id: 53, name: "세일러복 아치",       img: "characters/53.png", rarity: "epic" },
        { id: 54, name: "파일럿 아치",         img: "characters/54.png", rarity: "epic" },
        { id: 55, name: "조종사 아치",         img: "characters/55.png", rarity: "epic" },
        { id: 56, name: "재즈 아치",           img: "characters/56.png", rarity: "epic" },
        { id: 57, name: "바이올리니스트 아치", img: "characters/57.png", rarity: "epic" },

        // ---- 레전더리 (legendary) : 6개 ----
        { id: 58, name: "왕 아치",             img: "characters/58.png", rarity: "legendary" },
        { id: 59, name: "우주비행사 아치",     img: "characters/59.png", rarity: "legendary" },
        { id: 60, name: "우주인 아치",         img: "characters/60.png", rarity: "legendary" },
        { id: 61, name: "히어로 아치",         img: "characters/61.png", rarity: "legendary" },
        { id: 62, name: "산타 아치",           img: "characters/62.png", rarity: "legendary" },
        { id: 63, name: "기사(騎士) 아치",     img: "characters/63.png", rarity: "legendary" }
    ];
    /* ▲▲▲ 캐릭터 등록 끝 ▲▲▲ ========================================= */

    // 희귀도별 가챠 가중치 (숫자가 클수록 잘 나옴) - 필요하면 숫자만 조절하세요
    const RARITY_WEIGHT = { common: 100, rare: 40, epic: 15, legendary: 5 };
    const RARITY_LABEL  = { common: "일반", rare: "레어", epic: "에픽", legendary: "레전더리" };
    const RARITY_COLOR  = { common: "#8a9ba8", rare: "#2e86de", epic: "#a55eea", legendary: "#f7b731" };

    let usersDB = JSON.parse(localStorage.getItem('archieUsersDB')) || {};
    let currentUser = null;
    let scanLocked = false; // 모달이 떠 있는 동안 중복 스캔 방지

    function hardReset() {
        if (confirm("모든 유저 데이터와 도감이 완전히 삭제됩니다. 정말 하시겠습니까?")) {
            localStorage.clear();
            location.reload();
        }
    }

    function login() {
        const id = document.getElementById('loginId').value.trim();
        const pw = document.getElementById('loginPw').value.trim();
        if (!id) return;
        if (!usersDB[id]) usersDB[id] = { password: pw, collected: {} }; // collected: { charId: count }
        if (!usersDB[id].collected) usersDB[id].collected = {};
        currentUser = id;
        document.getElementById('authWrap').style.display = 'none';
        document.getElementById('appContainer').style.display = 'block';
        document.getElementById('demoQrArea').style.display = 'block';
        document.getElementById('welcomeMsg').innerText = id + "님 환영합니다";
        renderGallery();
    }

    function logout() {
        location.reload();
    }

    function startScanner() {
        document.getElementById('startScannerBtn').style.display = 'none';
        document.getElementById('reader').style.display = 'block';
        new Html5QrcodeScanner("reader", { fps: 10, qrbox: 250 }).render(onScanSuccess, () => {});
    }

    // 희귀도 가중치 기반 랜덤 캐릭터 뽑기
    function drawRandomCharacter() {
        const total = CHARACTERS.reduce((sum, c) => sum + RARITY_WEIGHT[c.rarity], 0);
        let r = Math.random() * total;
        for (const c of CHARACTERS) {
            r -= RARITY_WEIGHT[c.rarity];
            if (r <= 0) return c;
        }
        return CHARACTERS[CHARACTERS.length - 1];
    }

    function renderGallery() {
        const collected = usersDB[currentUser].collected;
        const container = document.getElementById("galleryContainer");
        container.innerHTML = "";

        const collectedCount = Object.keys(collected).length;
        document.getElementById("progressText").innerText = `수집한 캐릭터: ${collectedCount} / ${CHARACTERS.length}`;
        document.getElementById("progressFill").style.width = (collectedCount / CHARACTERS.length * 100) + "%";

        CHARACTERS.forEach(c => {
            const isCollected = !!collected[c.id];
            const count = collected[c.id] || 0;
            const badgeColor = RARITY_COLOR[c.rarity];
            container.innerHTML += `
                <div class="character-card" style="border-color:${isCollected ? badgeColor : 'transparent'}">
                    <span class="char-rarity-badge" style="background:${badgeColor}">${RARITY_LABEL[c.rarity]}</span>
                    <img src="${c.img}" class="character-img ${isCollected ? 'active' : ''}">
                    <div class="char-name">${isCollected ? c.name : '???'}</div>
                    ${isCollected && count > 1 ? `<div class="dup-count">x${count}</div>` : ``}
                </div>`;
        });
    }

    function onScanSuccess(decodedText) {
        if (scanLocked) return;
        if (db[decodedText]) {
            scanLocked = true;
            const data = db[decodedText];
            document.getElementById("modalTitle").innerText = data.title;
            document.getElementById("modalVideo").src = "https://www.youtube.com/embed/" + data.videoId + "?autoplay=1";
            document.getElementById("modalText").innerText = data.story;
            document.getElementById("step1").style.display = "block";
            document.getElementById("step2").style.display = "none";
            document.getElementById("storyModal").style.display = "block";
        }
    }

    function showReward() {
        document.getElementById("modalVideo").src = "";

        const drawn = drawRandomCharacter();
        document.getElementById("storyModal").dataset.drawnId = drawn.id;

        const alreadyOwned = !!(usersDB[currentUser].collected[drawn.id]);

        document.getElementById("rewardImg").src = drawn.img;
        document.getElementById("rewardName").innerText = drawn.name;
        const rarityEl = document.getElementById("rewardRarity");
        rarityEl.innerText = RARITY_LABEL[drawn.rarity];
        rarityEl.style.background = RARITY_COLOR[drawn.rarity];

        document.getElementById("rewardStatus").innerHTML = alreadyOwned
            ? `<div class="reward-dup-tag">이미 보유 중인 캐릭터예요 (중복)</div>`
            : `<div class="reward-new-tag">NEW! 도감에 새로 추가돼요</div>`;

        document.getElementById("step1").style.display = "none";
        document.getElementById("step2").style.display = "block";
    }

    function closeModal() {
        const id = document.getElementById("storyModal").dataset.drawnId;
        const collected = usersDB[currentUser].collected;
        collected[id] = (collected[id] || 0) + 1;
        localStorage.setItem('archieUsersDB', JSON.stringify(usersDB));
        document.getElementById("storyModal").style.display = "none";
        scanLocked = false;
        renderGallery();
    }
</script>
</body>
</html>
