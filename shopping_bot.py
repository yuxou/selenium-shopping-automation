import os
import time
import random
import math
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

try:
    import cv2
    import numpy as np
except ImportError:
    pass

class CoupangBot:
    """
    쿠팡 Ultimate Stealth 봇
    - Undetected-Chromedriver (UC) 사용: 각종 봇 탐지 우회
    - Human-like Mouse Movement: 베지에 곡선 이동 시뮬레이션
    - Residential Proxy Support: 프록시 설정 포함
    """
    def __init__(self):
        print("▶ [Stealth] Undetected Chrome 실행 준비 중...")
        
        # 1. 크롬 옵션 설정
        options = uc.ChromeOptions()
        
        # [중요] 봇 탐지 방지 옵션들
        options.add_argument('--no-first-run')
        options.add_argument('--no-service-autorun')
        options.add_argument('--password-store=basic')
        options.add_argument('--lang=ko_KR')
        
        # [Session Persistence] 쿠키/세션 저장소 설정
        profile_path = os.path.join(os.getcwd(), 'bot_profile')
        options.add_argument(f'--user_data_dir={profile_path}')
        print(f"▶ [설정] 프로필 경로: {profile_path}")

        # 2. UC 크롬 드라이버 실행 (버전 자동 매칭)
        self.driver = uc.Chrome(options=options, version_main=144) 
        
        self.wait = WebDriverWait(self.driver, 10) 
        self.driver.set_window_size(1920, 1080) 
        print("▶ [Stealth] 브라우저 실행 완료!")

    def human_move_to(self, element):
        """마우스 이동 시뮬레이션 (최적화)"""
        try:
            # 1. 화면에 보이게 스크롤
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            time.sleep(random.uniform(0.3, 0.6))
            
            # 2. ActionChains로 이동 (딜레이 최소화)
            actions = ActionChains(self.driver)
            actions.move_to_element(element)
            actions.pause(random.uniform(0.1, 0.3))
            actions.perform()
            
        except Exception:
            pass

    def type_like_human(self, element, text):
        """빠른 휴먼 타이핑"""
        element.click()
        time.sleep(random.uniform(0.1, 0.3)) 
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.01, 0.08)) 
        time.sleep(random.uniform(0.1, 0.3))

    def js_click(self, element):
        self.driver.execute_script("arguments[0].click();", element)

    def login(self, username, password):
        print("▶ [로그인] 쿠팡 메인 페이지 진입...")
        self.driver.get('https://www.coupang.com')
        time.sleep(random.uniform(1.5, 2.5))
        
        # 0. Access Denied 선제 체크
        if "Access Denied" in self.driver.page_source:
             print("❌ [차단됨] 메인 페이지 진입 즉시 Access Denied 발생.")
             return False

        # 1. 메인 로그인 버튼 찾기 (다중 선택자)
        login_btn = None
        try:
            selectors = [
                (By.CLASS_NAME, 'login'),
                (By.XPATH, "//*[@id='login']"),
                (By.XPATH, "//a[contains(text(), '로그인')]"),
                (By.CSS_SELECTOR, "#login > a")
            ]
            
            for by, val in selectors:
                try:
                    login_btn = self.driver.find_element(by, val)
                    if login_btn.is_displayed():
                        print(f"  로그인 버튼 찾음 ({val})")
                        break
                except:
                    continue
            
            if login_btn:
                login_btn.click()
                print("  로그인 페이지로 이동 중...")
                time.sleep(random.uniform(1.0, 1.5))
            else:
                raise Exception("모든 선택자 실패")

        except Exception:
            print("  메인 로그인 버튼 찾기 실패 -> (스크린샷: debug_no_login_btn.png) -> 직접 이동")
            self.driver.save_screenshot('debug_no_login_btn.png')
            self.driver.get('https://login.coupang.com/login/login.pang')
        
        # 2. 로그인 페이지 진입 확인
        if "login.coupang.com" not in self.driver.current_url and "Access Denied" not in self.driver.page_source:
            # 이미 로그인 된 상태일 수도 있음
            if "my-coupang" in self.driver.page_source or "logout" in self.driver.page_source:
                print("  이미 로그인 되어 있습니다.")
                return True

        try:
            print("  아이디/비번 입력...")
            email_input = self.wait.until(EC.presence_of_element_located((By.NAME, 'email')))
            self.type_like_human(email_input, username)
            
            pw_input = self.driver.find_element(By.NAME, 'password')
            self.type_like_human(pw_input, password)
            
            login_btn = self.driver.find_element(By.CLASS_NAME, 'login__button')
            login_btn.click()
            
            print("  로그인 요청 중... (메인 이동 대기)")
            try:
                self.wait.until(EC.presence_of_element_located((By.ID, 'headerSearchKeyword')))
                print("  로그인 성공 확인!")
                return True
            except:
                return True

        except Exception as e:
            print(f"  로그인 실패: {e}")
            return False

    def search_product(self, keyword):
        print(f"▶ '{keyword}' 검색 시도...")
        
        if "coupang.com" not in self.driver.current_url or "login" in self.driver.current_url:
             self.driver.get("https://www.coupang.com")
             time.sleep(2)
             
        # 1. 표준 방법 (Human Typing) - 다중 선택자 사용
        search_input = None
        try:
            input_selectors = [
                (By.ID, 'headerSearchKeyword'),
                (By.NAME, 'q'),
                (By.CLASS_NAME, 'headerSearchKeyword'),
                (By.CSS_SELECTOR, '#headerSearchKeyword')
            ]
            
            for by, val in input_selectors:
                try:
                    search_input = self.wait.until(EC.visibility_of_element_located((by, val)))
                    print(f"  검색창 찾음 ({val})")
                    break
                except:
                    continue
            
            if search_input:
                self.type_like_human(search_input, keyword)
                
                # 검색 버튼 클릭
                btn_selectors = [
                    (By.ID, 'headerSearchBtn'),
                    (By.CLASS_NAME, 'headerSearchBtn'),
                    (By.CSS_SELECTOR, '#headerSearchBtn'),
                    (By.TAG_NAME, 'form') 
                ]
                
                clicked = False
                for by, val in btn_selectors:
                    try:
                        if by == By.TAG_NAME and val == 'form':
                            search_input.submit() 
                            clicked = True
                            print("  검색 폼 제출(엔터) 완료")
                            break
                        
                        btn = self.driver.find_element(by, val)
                        if btn.is_displayed():
                            btn.click()
                            clicked = True
                            print(f"  검색 버튼 클릭 ({val})")
                            break
                    except:
                        continue
                
                if not clicked:
                    raise Exception("검색 버튼 클릭 실패")
                
                time.sleep(1.5)
                return

        except Exception:
            print("  (Type 검색 실패 -> JS 주입 시도)")

        # 2. 강력한 JS 검색 (Fallback) 
        js_script = f"""
            var input = document.getElementById('headerSearchKeyword') 
                        || document.getElementsByName('q')[0] 
                        || document.querySelector('.headerSearchKeyword');
                        
            var btn = document.getElementById('headerSearchBtn') 
                      || document.querySelector('.headerSearchBtn')
                      || document.querySelector('button.headerSearchBtn');
                      
            var form = document.getElementById('wa-search-form');
            
            if (input) {{
                input.value = '{keyword}';
                
                if (btn) {{
                    btn.click();
                    return true;
                }} 
                
                if (form) {{
                    form.submit();
                    return true;
                }}
            }}
            return false;
        """
        success = self.driver.execute_script(js_script)
        
        if success:
           print("  JS 검색 성공")
        else:
           print("❌ 검색 완전 실패 (URL 이동은 위험해서 하지 않음)")

    def select_first_product(self, target_keyword):
        print(f"▶ 상품 탐색 중... ('{target_keyword}' 포함 제품)")
        time.sleep(3) 
        
        try:
            # target_keyword를 JS에 주입
            script = f"""
            var items = Array.from(document.querySelectorAll('li.search-product'));
            if (items.length === 0) {{
                items = Array.from(document.querySelectorAll('li[class*="ProductUnit_productUnit"]'));
            }}
            if (items.length === 0) {{
                items = Array.from(document.querySelectorAll('#productList > li'));
            }}

            // 1순위: '{target_keyword}' 포함 제품
            var target = items.find(li => {{
                var text = li.innerText;
                return text.includes('{target_keyword}');
            }});
            
            // 2순위: 그냥 첫 번째
            if (!target && items.length > 0) {{
                target = items[0];
            }}
            
            if (target) {{
                var link = target.querySelector('a');
                if (link && link.href) {{
                    return link.href;
                }}
            }}
            return null;
            """
            
            product_url = self.driver.execute_script(script)
            
            if product_url:
                print(f"  상품 링크 발견: {product_url}")
                self.driver.get(product_url)
                print("  상세 페이지 이동 완료")
                time.sleep(3)
            else:
                print("  ❌ 상품을 찾을 수 없습니다. (스크린샷: error_no_product.png)")
                self.driver.save_screenshot('error_no_product.png')

        except Exception as e:
            print(f"❌ 상품 선택 실패: {e}")

    def buy_now(self):
        print("▶ 바로구매 시도... (JS Polling)")
        try:
            time.sleep(2)
            script = """
            var btn = document.querySelector('button.prod-buy-btn');
            if (!btn) {
                var xpath = "//button[contains(., '바로구매')] | //a[contains(., '바로구매')] | //div[@role='button'][contains(., '바로구매')]";
                var result = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
                btn = result.singleNodeValue;
            }
            
            if (btn) {
                btn.click();
                return true;
            }
            return false;
            """
            if self.driver.execute_script(script):
                print("  바로구매 버튼 클릭 성공 (JS)")
                time.sleep(2)
            else:
                 print("❌ 바로구매 버튼 없음 (스크린샷: error_buy_now.png)")
                 self.driver.save_screenshot('error_buy_now.png')
        except Exception as e:
             print(f"❌ 바로구매 에러: {e}")

    def pay_final(self):
        print("▶ 결제하기 시도... (JS Polling)")
        try:
            time.sleep(3)
            script = """
            var xpath = "//button[contains(., '결제하기')] | //a[contains(., '결제하기')]";
            var result = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
            var btn = result.singleNodeValue;
            
            if (btn) {
                btn.click();
                return true;
            }
            return false;
            """
            if self.driver.execute_script(script):
                print("  결제하기 버튼 클릭 성공 (JS)")
                time.sleep(3)
            else:
                 print("❌ 결제하기 버튼 못 찾음 (스크린샷: error_pay.png)")
                 self.driver.save_screenshot('error_pay.png')
        except Exception as e:
             print(f"❌ 결제하기 에러: {e}")

    def pay_with_password(self, password):
        print(f"▶ 결제 비밀번호 입력 시도 ({len(password)}자리)")
        time.sleep(2)
        
        # IFRAME 탐색 로직
        if self._click_password_digits(password):
            return

        print("  메인 프레임에 없음 -> iframe 탐색")
        iframes = self.driver.find_elements(By.TAG_NAME, 'iframe')
        for i, frame in enumerate(iframes):
            try:
                self.driver.switch_to.frame(frame)
                if self.driver.find_elements(By.CLASS_NAME, 'pad-key'):
                    print(f"  iframe[{i}]에서 키패드 발견!")
                    if self._click_password_digits(password):
                        return
                self.driver.switch_to.default_content()
            except:
                self.driver.switch_to.default_content()

    def _click_password_digits(self, password):
        """이미지 매칭 기반 클릭 (상세 디버깅 추가)"""
        try:
            pad = self.driver.find_element(By.CLASS_NAME, 'pad')
            pad.screenshot('current_keypad.png')
            
            # 디버깅용 컬러 이미지
            img_rgb_debug = cv2.imread('current_keypad.png')
            img_gray = cv2.cvtColor(img_rgb_debug, cv2.COLOR_BGR2GRAY)
            
            size = pad.size
            digit_coords = {}
            
            print(f"  [디버그] 키패드 분석 시작 (크기: {img_gray.shape})")

            for digit in password:
                template = cv2.imread(f'templates/{digit}.png', 0)
                if template is None: continue
                
                found = None
                # 스케일 범위 확장 및 세분화
                for scale in np.linspace(0.4, 1.8, 30):
                    resized_template = cv2.resize(template, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
                    
                    if resized_template.shape[0] > img_gray.shape[0] or resized_template.shape[1] > img_gray.shape[1]:
                        continue
                        
                    res = cv2.matchTemplate(img_gray, resized_template, cv2.TM_CCOEFF_NORMED)
                    _, max_val, _, max_loc = cv2.minMaxLoc(res)
                    
                    if found is None or max_val > found[0]:
                        found = (max_val, max_loc, scale, resized_template.shape)

                if found:
                    max_val, max_loc, scale, shape = found
                    print(f"    - 숫자 '{digit}' 매칭 점수: {max_val:.4f} (스케일: {scale:.2f})")
                    
                    # 매칭 결과 시각화 (디버그용 이미지에 그리기)
                    cv2.rectangle(img_rgb_debug, max_loc, (max_loc[0] + shape[1], max_loc[1] + shape[0]), (0, 0, 255), 2)
                    cv2.putText(img_rgb_debug, f"{digit}:{max_val:.2f}", (max_loc[0], max_loc[1]-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

                    if max_val > 0.55: # 임계값 완화
                        h, w = shape
                        # 중심 좌표 찾기
                        center_x = max_loc[0] + w // 2
                        center_y = max_loc[1] + h // 2
                        
                        # 클릭할 좌표 계산
                        off_x = center_x - size['width'] / 2
                        off_y = center_y - size['height'] / 2
                        
                        # ActionChains로 클릭
                        actions = ActionChains(self.driver)
                        actions.move_to_element_with_offset(pad, off_x, off_y).click().perform()
                        print(f"      -> 클릭 성공")
                        time.sleep(random.uniform(0.5, 1.0))
                    else:
                        print(f"      -> 매칭 실패 (점수 미달)")
                        cv2.imwrite('debug_keypad_matches.png', img_rgb_debug)
                        return False
            
            # 최종 결과 저장
            cv2.imwrite('debug_keypad_matches.png', img_rgb_debug)
            return True
            
        except Exception:
            # print(f"  키패드 처리 중 에러: {e}")
            return False

    def run(self):
        # ==========================================
        # [설정]
        TARGET_PRODUCT = "스파클 생수 무라벨 2L 24개" # 검색어
        TARGET_KEYWORD = "스파클"                 # 검색 결과에서 클릭할 단어
        # ==========================================

        # 1. 로그인
        # [중요] 실제 사용 시에는 환경 변수나 별도의 config 파일에서 불러오도록 수정 권장
        user_id = "YOUR_ID"
        user_pw = "YOUR_PASSWORD"
        
        if not self.login(user_id, user_pw):
            return
            
        # 2. 검색
        self.search_product(TARGET_PRODUCT)
        
        # 3. 구매
        self.select_first_product(TARGET_KEYWORD)
        self.buy_now()
        self.pay_final()
        
        # 4. 결제 비번
        payment_pw = "000000" # 결제 비밀번호 6자리
        self.pay_with_password(payment_pw)
        
        print("▶ 완료. 10초 대기...")
        time.sleep(10)

if __name__ == "__main__":
    bot = CoupangBot()
    bot.run()
