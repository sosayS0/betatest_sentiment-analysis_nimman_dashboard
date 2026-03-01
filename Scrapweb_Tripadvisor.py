import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import re
import os
import math

# --- CONFIGURATION ---
INPUT_CSV = "tripadvisor_urls.csv"
OUTPUT_CSV = "tripadvisor_reviews_cleaned.csv"
COMPLETED_LOG = "completed_restaurants.txt"

# --- HELPER FUNCTIONS ---
def clean_text(text):
    if not text: return None
    return re.sub(r'\s+', ' ', text.replace('Read more', '')).strip()

def get_rating_from_svg(container):
    if not container: return None
    try:
        svg = container.find('svg')
        if svg and svg.find('title'):
            text = svg.find('title').get_text()
            match = re.search(r"(\d+(\.\d+)?)", text)
            if match: return float(match.group(1))
    except: pass
    return None

def normalize_url(url):
    url = url.replace("th.tripadvisor.com", "www.tripadvisor.com")
    url = url.replace("tripadvisor.co.th", "www.tripadvisor.com")
    url = url.split('?')[0] 
    return url + "?filterLang=ALL"

def generate_pagination_urls(base_url, total_reviews):
    urls = [base_url]
    parts = base_url.split('-Reviews-')
    if len(parts) != 2: return urls
    pages = math.ceil(total_reviews / 15)
    for i in range(1, pages):
        offset = i * 15
        urls.append(f"{parts[0]}-Reviews-or{offset}-{parts[1]}")
    return urls

def load_completed_restaurants():
    if os.path.exists(COMPLETED_LOG):
        with open(COMPLETED_LOG, 'r', encoding='utf-8') as f:
            return set(line.strip() for line in f)
    return set()

def mark_as_completed(restaurant_name):
    with open(COMPLETED_LOG, 'a', encoding='utf-8') as f:
        f.write(f"{restaurant_name}\n")

# --- CORE PARSER ---
def parse_review_card(card, restaurant_name):
    data = {'Restaurant_Name': restaurant_name}
    try:
        title_el = card.find('div', attrs={'data-test-target': 'review-title'})
        data['Topic'] = clean_text(title_el.get_text()) if title_el else "No Title"
        
        rating_container = title_el.find_previous('div', class_=lambda x: x and 'VVbkp' in x) if title_el else card
        data['Rating_Overall'] = get_rating_from_svg(rating_container)

        body_el = card.find('div', attrs={'data-test-target': 'review-body'})
        data['Detail'] = clean_text(body_el.get_text(separator=' ')) if body_el else None

        written_el = card.find(string=re.compile(r'Written', re.IGNORECASE))
        if written_el:
            full_text = written_el.find_parent('div').get_text(separator=' ')
            date_match = re.search(r'Written\s+(.+)', full_text, re.IGNORECASE)
            data['Date_Written'] = date_match.group(1).strip() if date_match else full_text.replace('Written', '').strip()
        else:
            data['Date_Written'] = None

        return data
    except Exception:
        return None

def save_to_csv(data_list):
    if not data_list: return
    df = pd.DataFrame(data_list)
    header = not os.path.exists(OUTPUT_CSV)
    df.to_csv(OUTPUT_CSV, mode='a', header=header, index=False, encoding='utf-8-sig')

# --- ANTI-BAN LAUNCHER ---
def launch_browser():
    """ เปิด Browser ใหม่ทุกครั้งเพื่อล้างคุกกี้ """
    options = uc.ChromeOptions()
    options.add_argument('--no-first-run')
    options.add_argument("--disable-extensions")
    # สุ่ม User-Agent เพื่อพรางตัว
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0"
    ]
    options.add_argument(f'user-agent={random.choice(user_agents)}')
    
    driver = uc.Chrome(options=options)
    driver.set_page_load_timeout(60)
    return driver

# --- MAIN ENGINE ---
def main():
    print("🚀 เริ่มต้นเดินเครื่อง TripAdvisor Scraper (V.3 Anti-Ban Stealth Mode)")
    
    try:
        df_input = pd.read_csv(INPUT_CSV)
    except FileNotFoundError:
        print(f"❌ ไม่พบไฟล์ {INPUT_CSV}")
        return

    completed_rests = load_completed_restaurants()

    for index, row in df_input.iterrows():
        rest_name = str(row['Restaurant_Name']).strip()
        total_reviews = int(str(row['number_review']).replace(',', ''))
        raw_url = str(row['URL']).strip()

        if rest_name in completed_rests:
            continue # ถ้ามีใน Log แล้ว ข้ามเงียบๆ ไม่ต้อง print รกจอ

        print(f"\n==========================================")
        print(f"🎯 กำลังดึงข้อมูล: {rest_name} (เป้าหมาย: ~{total_reviews} รีวิว)")
        
        base_url = normalize_url(raw_url)
        page_urls = generate_pagination_urls(base_url, total_reviews)
        print(f"🔗 สร้าง URL ทั้งหมด {len(page_urls)} หน้า")

        # เปิด Browser สดใหม่สำหรับร้านนี้โดยเฉพาะ
        print("⏳ กำลังเปิด Chrome (ล้าง Session ใหม่)...")
        driver = launch_browser()

        try:
            for page_idx, page_url in enumerate(page_urls):
                print(f"   📄 หน้าที่ {page_idx + 1}/{len(page_urls)}...")
                
                driver.get(page_url)
                
                # หน่วงเวลาแบบมนุษย์ (สำคัญมาก!)
                sleep_time = random.uniform(5.5, 9.5) 
                time.sleep(sleep_time) 

                try:
                    driver.execute_script("""
                        document.querySelectorAll('[role="dialog"]').forEach(e => e.remove());
                        document.body.style.overflow = 'auto';
                    """)
                except: pass

                # เลื่อนจอแบบเนียนๆ
                try:
                    driver.execute_script("window.scrollBy(0, 400);")
                    time.sleep(1)
                    driver.execute_script("window.scrollBy(0, 400);")
                    time.sleep(1)
                    driver.execute_script("""
                        document.querySelectorAll('span.biGQs._P.ezezH').forEach(el => {
                            if(el.innerText.includes('Read more')) el.click();
                        });
                    """)
                    time.sleep(2)
                except: pass

                soup = BeautifulSoup(driver.page_source, 'html.parser')
                
                # เช็คว่าโดนบล็อกไหม
                if "Are you a robot?" in soup.get_text() or "Access Denied" in soup.get_text():
                    print("   🚨 โดนจับได้ว่าเป็นบอท! (โดนบล็อกหน้าเว็บ)")
                    break # ออกจากลูปย่อยทันทีเพื่อปิดเบราว์เซอร์

                cards = soup.find_all('div', attrs={'data-automation': 'reviewCard'})
                
                if not cards:
                    print("   ⚠️ ไม่พบรีวิวในหน้านี้ ข้าม...")
                    continue

                page_data = []
                for card in cards:
                    r_data = parse_review_card(card, rest_name)
                    if r_data: page_data.append(r_data)
                
                save_to_csv(page_data)
                print(f"   ✅ เก็บได้ {len(page_data)} รีวิว (พัก {sleep_time:.1f} วิ)")

            # ถ้าหลุดลูปออกมาแบบปกติดี (ไม่โดนบล็อก)
            mark_as_completed(rest_name)
            print(f"🎉 ดูดข้อมูลร้าน '{rest_name}' เสร็จสมบูรณ์!")
            
        except Exception as e:
            print(f"   [!] Error ระหว่างดึงร้านนี้: {e}")
        finally:
            print("🛑 ปิด Browser ประจำร้านนี้ (เตรียมล้างคุกกี้)")
            try: driver.quit()
            except: pass
            
            # พักยาวๆ ก่อนขึ้นร้านใหม่
            long_rest = random.uniform(15, 25)
            print(f"⏳ พักหายใจยาว {long_rest:.0f} วินาที ก่อนลุยร้านถัดไป...")
            time.sleep(long_rest)

if __name__ == "__main__":
    main()   