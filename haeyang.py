<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>심해의 기록자: 도감 시스템</title>
    <script src="https://unpkg.com/html5-qrcode"></script>
    <style>
        /* 기본 스타일 */
        body { font-family: 'Malgun Gothic', sans-serif; background-color: #f0f8ff; text-align: center; padding: 20px; }
        .gallery { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; margin-top: 20px; }
        .card { background: white; padding: 10px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .card img { width: 100%; height: auto; border-radius: 5px; }
        
        /* 모달 및 로딩 */
        #storyModal { display: none; position: fixed; top:0; left:0; width:100%; height:100%; background: rgba(0,0,0,0.8); z-index: 100; }
        .modal-content { background: white; width: 90%; max-width: 400px; margin: 10% auto; padding: 20px; border-radius: 15px; }
        #loadingEffect { display: none; padding: 50px; font-size: 20px; font-weight: bold; color: #0066cc; }
    </style>
</head>
<body>

    <div id="authWrap">
        <h2>🌊 심해의 기록자</h2>
        <button onclick="startAsGuest()">시작하기</button>
    </div>

    <div id="appContainer">
        <h2 id="welcomeMsg"></h2>
        <button onclick="startScanner()">📷 QR 스캐너 켜기</button>
        <div id="reader" style="width:300px; margin: 20px auto;"></div>
        <div class="gallery" id="galleryContainer"></div>
    </div>

    <div id="storyModal">
        <div class="modal-content">
            <div id="step1">
                <h3 id="modalTitle"></h3>
                <div id="videoArea"></div>
                <p id="modalStory"></p>
                <button onclick="showRewardMotion()">보상 획득하기!</button>
            </div>
            <div id="step2" style="display:none;">
                <div id="loadingEffect">✨ 아치를 찾는 중...</div>
                <div id="resultArea" style="display:none;">
                    <h3 id="rewardTitle"></h3>
                    <img id="rewardImg" style="width:150px;">
                    <br><button onclick="closeModal()">도감 확인</button>
                </div>
            </div>
        </div>
    </div>

<script>
    // 캐릭터 63개 데이터 자동 생성
    const CHARACTERS = Array.from({ length: 63 }, (_, i) => ({
        id: i + 1,
        name: `아치${i + 1}`,
        img: `characters/${String(i + 1).padStart(2, '0')}.png`,
        rarity: i < 25 ? 'common' : i < 45 ? 'rare' : i < 57 ? 'epic' : 'legendary'
    }));

    const db = {
        "QR_JUNGBU": { title: "필리핀 방제", videoId: "jRX3fezEFIE", story: "필리핀 기름 유출 현장까지 파견된 해경!" },
        // ...나머지 QR 데이터 매핑
    };

    let currentUser = "";

    function startAsGuest() {
        const userCount = Object.keys(JSON.parse(localStorage.getItem('users') || '{}')).length + 1;
        currentUser = `아치${userCount}`;
        document.getElementById('authWrap').style.display = 'none';
        document.getElementById('appContainer').style.display = 'block';
        document.getElementById('welcomeMsg').innerText = `${currentUser}님 환영합니다`;
        renderGallery();
    }

    function showRewardMotion() {
        document.getElementById('step1').style.display = 'none';
        document.getElementById('step2').style.display = 'block';
        document.getElementById('loadingEffect').style.display = 'block';

        // 랜덤 뽑기 (이미지 파일명 기반)
        setTimeout(() => {
            const drawn = CHARACTERS[Math.floor(Math.random() * CHARACTERS.length)];
            document.getElementById('loadingEffect').style.display = 'none';
            document.getElementById('resultArea').style.display = 'block';
            document.getElementById('rewardTitle').innerText = `${drawn.name} 발견!`;
            document.getElementById('rewardImg').src = drawn.img;
        }, 2000); // 2초간 로딩 모션
    }

    function renderGallery() {
        const container = document.getElementById('galleryContainer');
        CHARACTERS.forEach(c => {
            container.innerHTML += `
                <div class="card">
                    <img src="${c.img}" onerror="this.src='placeholder.png'">
                    <div>${c.name}</div>
                </div>`;
        });
    }

    function closeModal() {
        document.getElementById('storyModal').style.display = 'none';
        location.reload();
    }

    function startScanner() { /* 기존 코드 유지 */ }
</script>
</body>
</html>
