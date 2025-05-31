# Webproject
세종대학교 2학년 웹프로그래밍 프로젝트_ WebFix
# WebProject

✨ **AI 기반 오타 자동 수정 검색 시스템**

---

## 프로젝트 소개

이 프로젝트는 사용자가 입력한 검색어의 오타를 AI가 자동으로 수정해주고,  
수정된 검색어로 구글 검색 결과를 새 창/탭에서 보여주는 웹 애플리케이션입니다.  
또한, 사용자가 직접 수정 결과를 제안할 수 있는 피드백 기능이 포함되어 있습니다.

---

## 주요 기능

- **AI 오타 자동 수정**
  - Hugging Face의 한국어 맞춤법 교정 모델 사용
- **검색 결과 새 창/탭에서 열기**
  - 수정된 검색어로 구글 검색 결과 자동 열기
- **피드백 시스템**
  - 사용자가 직접 수정 결과 제안 가능
- **데이터베이스 연동**
  - 오타 수정 기록 및 피드백 저장

---

## 프로젝트 구조

```plaintext
WebProject/
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── backend/
│   └── main.py
├── README.md
└── .gitignore

undefined
---

## 실행 방법

1. **백엔드 서버 실행**
- Colab에서 실행 시, ngrok 공개 URL이 출력됩니다.
- 로컬에서 실행 시, `http://localhost:8000`으로 접속 가능합니다.

2. **프론트엔드 실행**
- `frontend/index.html`을 브라우저로 열기
- 반드시 **Live Server** 또는 웹서버 환경에서 실행하세요.

3. **검색 테스트**
- 검색창에 검색어 입력 → 엔터
- 오타가 수정되면 구글 검색 결과가 새 창/탭에서 열립니다.
- "수정 제안" 버튼으로 피드백 제출 가능

---

## 기술 스택

- **프론트엔드**: HTML, CSS, JavaScript
- **백엔드**: FastAPI (Python)
- **데이터베이스**: SQLite
- **AI 모델**: Hugging Face Transformers (ET5 기반 한국어 맞춤법 교정 모델)
- **배포**: ngrok (Colab 환경)

---

## 라이선스

MIT License

---

## 기여 방법

1. 저장소를 Fork하세요.
2. 새로운 브랜치를 만드세요 (`git checkout -b feature/your-feature`)
3. 변경사항을 커밋하세요 (`git commit -am 'Add some feature'`)
4. 브랜치에 Push하세요 (`git push origin feature/your-feature`)
5. Pull Request를 보내주세요.

---

## 문의

궁금한 점이 있으면 [이슈](https://github.com/seFrog/WebProject/issues)로 남겨주세요!

---

🛠️ **즐거운 코딩 되세요!**
