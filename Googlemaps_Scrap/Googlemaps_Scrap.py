import time
import pandas as pd
import re
import random
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# ==========================================
# ⚙️ CONFIGURATION
# ==========================================
INPUT_FILE = "Nimman_ShopList_126store.csv"
OUTPUT_FILE = "Nimman_ShopList_126store_Output.csv" 
MAX_REVIEWS = 200
CHROME_PORT = "127.0.0.1:9222"

# ==========================================
# 🛠️ HELPER FUNCTIONS
# ==========================================

def get_existing_shops(filename):
    if not os.path.exists(filename):
        return set()
    try:
        df = pd.read_csv(filename)
        if 'Restaurant_Name' in df.columns:
            return set(df['Restaurant_Name'].unique())
    except:
        return set()
    return set()

def random_sleep(min_s, max_s):
    time.sleep(random.uniform(min_s, max_s))

def get_attributes_hybrid(card_soup):
    data = {
        "Service_Option": "", "Meal_Type": "", "Price_Range": "", 
        "Noise_Level": "", "Crowd_Size": "",
        "Score_Food": "", "Score_Service": "", "Score_Atmosphere": "",
        "Recommended_Dishes": "", "Parking_Options": "", 
        "Vegetarian_Options": "", "Kid_Friendliness": "", 
        "Wheelchair_Access": "", "Dietary_Restrictions": ""
    }
    full_text = card_soup.get_text(separator="\n", strip=True)
    lines = full_text.split('\n')
    
    for i, line in enumerate(lines):
        line = line.strip()
        if "Price per person" in line:
            target = line
            if i+1 < len(lines) and ("฿" in lines[i+1] or "$" in lines[i+1]): target = lines[i+1]
            match = re.search(r'[฿$€]\d+[-–]\d+|\d+\+', target)
            if match: data["Price_Range"] = match.group(0).replace('–', '-')

        if "Noise level" in line and i+1 < len(lines): data["Noise_Level"] = lines[i+1]
        if "Crowd size" in line and i+1 < len(lines): data["Crowd_Size"] = lines[i+1]

        for score in ["Food", "Service", "Atmosphere"]:
            if line.startswith(score):
                match = re.search(r'[:\s]+([1-5])', line)
                if match: data[f"Score_{score}"] = match.group(1)
                elif i+1 < len(lines) and lines[i+1].isdigit(): data[f"Score_{score}"] = lines[i+1]

        if "Recommended dishes" in line:
            dishes = []
            for j in range(1, 8):
                if i+j >= len(lines): break
                next_l = lines[i+j]
                if any(k in next_l for k in ["Parking", "Vegetarian", "Wheelchair", "Kid", "Dietary", "Service"]): break
                if not next_l.isdigit() and len(next_l) > 2: dishes.append(next_l)
            data["Recommended_Dishes"] = ", ".join(dishes)

        maps = {"Parking": "Parking_Options", "Vegetarian": "Vegetarian_Options", 
                "Kid-friendliness": "Kid_Friendliness", "Wheelchair": "Wheelchair_Access",
                "Dietary restrictions": "Dietary_Restrictions"}
        for k, v in maps.items():
            if k in line:
                if ":" in line: data[v] = line.split(":")[-1].strip()
                elif i+1 < len(lines): data[v] = lines[i+1]

        if line in ["Dine in", "Takeout", "Delivery"]: data["Service_Option"] = line
        if line in ["Breakfast", "Lunch", "Dinner", "Brunch"]: data["Meal_Type"] = line
    return data

def scrape_one_shop(driver, shop_name, initial_url):
    print(f"\n🏠 Start: {shop_name}")
    
    driver.get(initial_url)
    try:
        WebDriverWait(driver, 20).until(lambda d: "maps" in d.current_url and "search" not in d.current_url)
    except:
        print("   ⚠️ Redirect timeout. Proceeding anyway...")

    if "Sign in" in driver.title:
        print("   🚨 LOGIN REQUIRED! Waiting 60s...")
        time.sleep(60)

    if "hl=en" not in driver.current_url:
        sep = "&" if "?" in driver.current_url else "?"
        driver.get(driver.current_url + sep + "hl=en")
        random_sleep(3, 5)

    # =========================================================
    # 🌟 แก้ไขใหม่: ระบบ Retry & รอ 15 วินาที
    # =========================================================
    print("   👉 Clicking Reviews...")
    reviews_loaded = False
    
    for attempt in range(2): # ลอง 2 รอบ ถ้าเน็ตช้า
        try:
            # ใช้ JS กดปุ่ม
            driver.execute_script("""
                let tabs = document.querySelectorAll('button[role="tab"], button');
                for (let tab of tabs) {
                    if (tab.textContent.includes('Reviews') || (tab.getAttribute('aria-label') && tab.getAttribute('aria-label').includes('Reviews'))) {
                        tab.click();
                        return;
                    }
                }
            """)
            random_sleep(2, 3)
            
            # รอ 15 วินาที แทน 5 วินาที
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'jftiEf')))
            reviews_loaded = True
            print("   ✅ Reviews loaded successfully!")
            break # โหลดสำเร็จ หลุดจาก loop retry
            
        except Exception as e:
            print(f"   ⚠️ Attempt {attempt+1} failed to load reviews. Retrying...")
            try:
                # ลองใช้วิธีกดผ่าน XPath เป็นตัวสำรอง
                wait = WebDriverWait(driver, 5)
                xpath = "//button[contains(@aria-label, 'Reviews')]"
                btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                btn.click()
                random_sleep(2, 3)
            except: pass

    if not reviews_loaded:
        print("   ❌ Reviews not loaded after multiple attempts. Skipping this shop.")
        return []
    # =========================================================

    scrollable_div = None
    try:
        wait = WebDriverWait(driver, 5)
        scrollable_div = driver.find_element(By.CSS_SELECTOR, 'div.m6QErb[aria-label*="Reviews"], div.m6QErb.DxyBCb')
    except:
        try:
            scrollable_div = driver.find_element(By.XPATH, "//div[contains(@class, 'm6QErb')][.//div[@class='jftiEf']]")
        except: pass

    print("   ⏳ Scrolling (JS Mode)...")
    prev_count = 0
    stuck_count = 0
    
    while True:
        cards = driver.find_elements(By.CLASS_NAME, 'jftiEf')
        count = len(cards)
        
        if scrollable_div:
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
        else:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
        random_sleep(1.5, 2.5)

        if count >= MAX_REVIEWS: break
        if count == prev_count:
            stuck_count += 1
            if stuck_count >= 5:
                if count == 0: 
                     print("   ⚠️ No reviews found (0 count).")
                     break
                print("   🛑 Reached end.")
                break
        else:
            stuck_count = 0
            prev_count = count
            
    print("   🔍 Expanding Text...")
    driver.execute_script("""
        document.querySelectorAll('button[aria-label*="More"], button[aria-label*="See more"], button.w8nwRe').forEach(b => b.click());
    """)
    random_sleep(1, 2)
    
    driver.execute_script("""
        let buttons = document.querySelectorAll('button');
        for (let btn of buttons) { 
            if (btn.textContent.includes('See original')) btn.click(); 
        }
    """)
    random_sleep(2, 3)

    print(f"   📝 Extracting {len(driver.find_elements(By.CLASS_NAME, 'jftiEf'))} reviews...")
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    shop_data = []
    
    for card in soup.find_all('div', class_='jftiEf'):
        try:
            user_stats = card.find('div', class_='RfnDt') or card.find('div', class_='nsN1j')
            stats_text = user_stats.get_text() if user_stats else ""
            is_local = 1 if "Local Guide" in stats_text else 0
            rev_count = 0
            match = re.search(r'(\d+)\s*reviews?', stats_text.replace(',',''))
            if match: rev_count = int(match.group(1))

            rating = 0
            star = card.find('span', class_='kvMYJc')
            if star: 
                m = re.search(r'(\d+)', star.get('aria-label',''))
                if m: rating = int(m.group(1))

            date = card.find('span', class_='rsqaWe').get_text().strip() if card.find('span', class_='rsqaWe') else ""
            text_span = card.find('span', class_='wiI7pd')
            review_text = text_span.get_text().strip() if text_span else ""

            attr_data = get_attributes_hybrid(card)

            shop_data.append({
                "Restaurant_Name": shop_name,
                "URL": driver.current_url,
                "Is_Local_Guide": is_local,
                "Total_User_Reviews": rev_count,
                "Rating": rating,
                "Date": date,
                "Review_Original": review_text,
                **attr_data
            })
        except: continue
        
    return shop_data

# ==========================================
# 🚀 MAIN LOOP
# ==========================================
def main():
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Input file not found: {INPUT_FILE}")
        return

    completed_shops = get_existing_shops(OUTPUT_FILE)
    print(f"📂 Found {len(completed_shops)} shops already completed in {OUTPUT_FILE}")

    df_shops = pd.read_csv(INPUT_FILE)
    total_shops = len(df_shops)

    print("🚀 Connecting Chrome...")
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", CHROME_PORT)
    try:
        driver = webdriver.Chrome(options=chrome_options)
    except:
        print("❌ Connect failed. Check port 9222.")
        return

    for index, row in df_shops.iterrows():
        shop_name = row['Restaurant_Name']
        url = row['URL']
        
        if shop_name in completed_shops:
            print(f"⏭️ Skipping {shop_name} (Already done)")
            continue

        print(f"------------------------------------------------")
        print(f"Processing {index+1}/{total_shops}: {shop_name}")

        try:
            reviews = scrape_one_shop(driver, shop_name, url)
            
            if reviews:
                df_new = pd.DataFrame(reviews)
                if not os.path.exists(OUTPUT_FILE):
                    df_new.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig', mode='w')
                else:
                    df_new.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig', mode='a', header=False)
                
                print(f"   ✅ Saved {len(reviews)} reviews to {OUTPUT_FILE}")
                completed_shops.add(shop_name)
            else:
                print("   ⚠️ No reviews found.")

        except Exception as e:
            print(f"   ❌ Critical Error on this shop: {e}")
            continue

        random_sleep(2, 4)

    print("\n✅✅✅ All Tasks Completed!")

if __name__ == "__main__":
    main()