# 🛒 Selenium Shopping Automation (KR)

파이썬과 Selenium, 그리고 OpenCV를 활용한 **쿠팡(Coupang) 자동 구매 봇**입니다.  
봇 탐지를 우회하는 **Stealth 기술**과 보안 키패드 입력을 위한 **이미지 매칭** 기술이 적용되어 있습니다.

> **주의**: 이 코드는 학습 및 테스트 목적으로 작성되었습니다. 과도한 사용으로 인한 계정 정지나 불이익에 대해 개발자는 책임을 지지 않습니다.

---

## 주요 기능 (Features)

*   **고급 탐지 우회 (Stealth Mode)**
    *   `undetected-chromedriver` 라이브러리 사용
    *   사람과 유사한 마우스 이동 경로(Bezier Curve) 시뮬레이션
    *   무작위 딜레이 타이핑 적용

*   **세션 유지 및 자동 로그인 (Session Persistence)**
    *   최초 로그인 시 쿠키와 세션을 로컬(`bot_profile` 폴더)에 저장
    *   재실행 시 **완전 자동 로그인** 처리되어 캡차 및 로그인 번거로움을 제거

*   **보안 키패드 대응 (Secure Keypad)**
    *   OpenCV 템플릿 매칭 기술 적용
    *   화면에 무작위로 위치하는 보안 키패드(숫자)를 인식하여 클릭
    *   iFrame 내부의 키패드까지 탐색 및 처리

*   **스마트 검색 및 구매**
    *   다양한 CSS/XPath 선택자를 활용한 요소 탐색
    *   Human-like Typing과 JavaScript Injection(Fallback) 방식 병행
    *   검색 -> 상품 선택 -> 바로 구매 -> 결제하기 -> 비밀번호 입력의 전 과정 자동화

---

## 🛠️ 설치 방법 (Installation)

### 1. 환경 설정
*   **Python**: 3.9 이상 권장
*   **Operating System**: macOS / Windows / Linux

### 2. 프로젝트 클론 및 라이브러리 설치

```bash
# 필수 라이브러리 설치
pip install -r requirements.txt
```

> **Requirements**:
> *   `undetected-chromedriver>=3.5.0`
> *   `selenium`
> *   `opencv-python`
> *   `numpy`

### 3. Chrome 버전 확인
이 봇은 `shopping_bot.py` 내부에 **Chrome 버전 144**로 설정되어 있습니다.  
본인의 Chrome 브라우저 버전에 맞춰 코드를 수정해야 할 수 있습니다.

```python
# shopping_bot.py
self.driver = uc.Chrome(options=options, version_main=144) 
```

### 4. 템플릿 이미지 준비 (필수)
보안 키패드 인식을 위해 `templates/` 폴더에 `0.png` ~ `9.png` 이미지가 반드시 있어야 합니다.
*   경로 예시: `templates/0.png`, `templates/1.png` ...

---

## ⚙️ 설정 (Configuration)

`shopping_bot.py` 파일을 열어 아래 **[설정]** 부분을 본인의 정보에 맞게 수정하세요.

### 1. 상품 및 검색어 설정
```python
# ==========================================
# [설정]
TARGET_PRODUCT = "구매할 상품 전체명" # 검색창에 입력할 전체 검색어
TARGET_KEYWORD = "핵심 키워드"      # 검색 결과 리스트에서 식별할 핵심 키워드
# ==========================================
```

### 2. 로그인 정보 수정
```python
# 반드시 본인의 아이디와 비밀번호로 변경하세요.
if not self.login("your_email@domain.com", "your_password"):
    return
```

### 3. 결제 비밀번호 수정
```python
# 본인의 결제 비밀번호 6자리
self.pay_with_password("123456")
```

---

## 🚀 사용 방법 (Usage)

터미널에서 아래 명령어로 스크립트를 실행합니다.

```bash
python shopping_bot.py
```

1.  **실행**: 스크립트가 실행되면 브라우저가 열리고 자동으로 로그인을 시도합니다.
2.  **세션 저장**: 최초 성공 시 세션이 `bot_profile`에 저장되어, 이후 실행부터는 로그인 과정 없이 즉시 구매 단계로 넘어갑니다.
3.  **구매 진행**:
    *   상품 검색 -> 결과 클릭 -> 상세 페이지 -> 바로구매 -> 결제하기 -> 비밀번호 입력 -> **완료**

---

## ⚠️ 문제 해결 (Troubleshooting)

### Q. IP 차단 (Access Denied)
*   사이트의 보안 정책에 의해 IP가 일시적으로 차단된 경우입니다.
*   **해결책**: 모바일 핫스팟(테더링)을 사용하여 IP를 변경하고 다시 시도하세요. 

### Q. 키패드 인식 실패
*   `debug_keypad_matches.png` 이미지를 확인하여 매칭 실패 원인을 분석하세요.
*   `templates/` 폴더의 이미지를 본인의 화면에서 직접 캡처한 이미지로 교체하면 인식률이 향상됩니다.
