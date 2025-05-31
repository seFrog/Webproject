// XSS 방지 함수
const escapeHtml = (text) => 
    text.replace(/[&<>"']/g, m => 
        ({ '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;' }[m]));

// API 엔드포인트 설정
const API_URL = 'https://9391-34-75-86-194.ngrok-free.app/correct';
let currentCorrection = null;

// 피드백 모달 관련 요소 선택
const modal = document.getElementById('feedbackModal');
const closeBtn = document.querySelector('.close');
const submitBtn = document.getElementById('submitFeedback');

// 모달 열기
function openFeedbackModal(original, corrected) {
    document.getElementById('modalOriginal').textContent = original;
    document.getElementById('modalCorrected').textContent = corrected;
    modal.style.display = 'block';
}

// 모달 닫기
function closeFeedbackModal() {
    modal.style.display = 'none';
    currentCorrection = null;
}

// 모달 닫기 이벤트
closeBtn.addEventListener('click', closeFeedbackModal);
window.addEventListener('click', (e) => {
    if (e.target === modal) closeFeedbackModal();
});

// 피드백 제출 이벤트 (제출 후 화면에 바로 반영)
submitBtn.addEventListener('click', async () => {
    const userInput = document.getElementById('userSuggestion').value;
    if (!userInput) {
        alert('수정할 내용을 입력해주세요!');
        return;
    }
    try {
        await fetch('https://9391-34-75-86-194.ngrok-free.app/api/feedback', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                original: currentCorrection.original,
                system: currentCorrection.corrected,
                user: userInput
            })
        });
        alert('피드백이 제출되었습니다!');
        // 화면에 바로 반영
        document.getElementById('suggestion').innerHTML = 
            `✅ 사용자가 직접 수정: <strong>${escapeHtml(userInput)}</strong>`;
        currentCorrection.corrected = userInput; // 내부 데이터 갱신
        closeFeedbackModal();
    } catch (error) {
        console.error('피드백 제출 오류:', error);
    }
});

// 검색 폼 제출 이벤트
// 기존 코드 일부 생략

document.getElementById('searchForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const query = document.getElementById('mainSearch').value.trim();
    
    if (!query) {
        document.getElementById('mainSearch').focus();
        return;
    }

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ text: query })
        });
        
        const data = await response.json();
        const correctedQuery = data.corrected || query;
        
        // ✅ 구글 검색 결과를 새 창/탭에서 엽니다
        window.open(`https://www.google.com/search?q=${encodeURIComponent(correctedQuery)}`, '_blank');
        
        // 아래는 기존의 피드백/수정 메시지 표시 코드
        if (data.corrected && data.corrected !== query) {
            const safeQuery = escapeHtml(query);
            const safeCorrected = escapeHtml(data.corrected);
            document.getElementById('suggestion').innerHTML = 
                `✅ 검색어가 <strong>${safeCorrected}</strong>로 수정되었습니다 
                <button onclick="openFeedbackModal('${safeQuery}', '${safeCorrected}')" 
                        class="feedback-btn">수정 제안</button>`;
            currentCorrection = { 
                original: query, 
                corrected: data.corrected 
            };
        }
    } catch (error) {
        console.error('API 오류:', error);
    }
});
