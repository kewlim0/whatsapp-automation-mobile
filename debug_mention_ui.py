from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Appium connection settings
options = UiAutomator2Options()
options.platform_name = "Android"
options.automation_name = "UiAutomator2"
options.device_name = "AndroidDevice"
options.app_package = "com.whatsapp.w4b"
options.app_activity = "com.whatsapp.home.ui.HomeActivity"
options.no_reset = True
options.new_command_timeout = 300

print("[DEBUG] Connecting to Appium...")
driver = webdriver.Remote('http://localhost:4723', options=options)
print("[DEBUG] ✓ Connected to Appium")

try:
    # Wait for WhatsApp to load
    time.sleep(3)

    # Step 1: Find the input field and type '@'
    print("\n[STEP 1] Looking for caption input field...")
    input_selectors = [
        (AppiumBy.ID, "com.whatsapp.w4b:id/caption_row"),
        (AppiumBy.ID, "com.whatsapp.w4b:id/input_layout"),
        (AppiumBy.ID, "com.whatsapp.w4b:id/entry"),
        (AppiumBy.XPATH, "//android.widget.EditText")
    ]

    input_field = None
    for selector_type, selector in input_selectors:
        try:
            print(f"[DEBUG] Trying selector: {selector}")
            input_field = driver.find_element(selector_type, selector)
            if input_field:
                print(f"[DEBUG] ✓ Found input field with: {selector}")
                break
        except:
            continue

    if not input_field:
        print("[ERROR] Could not find input field. Make sure you're on a chat screen with caption field open!")
        driver.quit()
        exit(1)

    # Type '@' to open mention list
    print("\n[STEP 2] Typing '@' to open mention list...")
    input_field.click()
    time.sleep(0.5)
    input_field.send_keys("@")
    time.sleep(2)  # Wait for mention list to appear
    print("[DEBUG] ✓ Typed '@'")

    # Step 2: Check if mention list container exists
    print("\n[STEP 3] Checking for mention list container...")
    try:
        list_container = driver.find_element(AppiumBy.ID, "com.whatsapp.w4b:id/list")
        print(f"[DEBUG] ✓ Found mention list container")
        print(f"[DEBUG] Container visible: {list_container.is_displayed()}")
    except Exception as e:
        print(f"[ERROR] Could not find mention list container: {e}")

    # Step 3: Get the full page source
    print("\n[STEP 4] Dumping UI hierarchy...")
    print("="*80)
    page_source = driver.page_source

    # Save to file for detailed inspection
    with open("mention_ui_hierarchy.xml", "w", encoding="utf-8") as f:
        f.write(page_source)
    print("[DEBUG] ✓ Full UI hierarchy saved to 'mention_ui_hierarchy.xml'")

    # Step 4: Check various LinearLayout instances
    print("\n[STEP 5] Checking LinearLayout instances in mention list area...")
    print("="*80)
    try:
        # Get all LinearLayouts
        linear_layouts = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.LinearLayout")
        print(f"[DEBUG] Total LinearLayouts found: {len(linear_layouts)}")

        # Check first 10 instances
        for i in range(min(10, len(linear_layouts))):
            try:
                element = linear_layouts[i]
                print(f"\n[LinearLayout instance {i}]")
                print(f"  Visible: {element.is_displayed()}")
                print(f"  Location: {element.location}")
                print(f"  Size: {element.size}")

                # Try to get resource-id
                try:
                    resource_id = element.get_attribute("resource-id")
                    print(f"  Resource-ID: {resource_id}")
                except:
                    print(f"  Resource-ID: None")

                # Try to get text content
                try:
                    text = element.get_attribute("text")
                    if text:
                        print(f"  Text: {text}")
                except:
                    pass

                # Check for child elements
                try:
                    children = element.find_elements(AppiumBy.XPATH, "./*")
                    print(f"  Children count: {len(children)}")
                    if len(children) > 0:
                        print(f"  Child types: {[child.get_attribute('class') for child in children[:3]]}")
                except:
                    pass

            except Exception as e:
                print(f"  Error inspecting instance {i}: {str(e)[:50]}")

    except Exception as e:
        print(f"[ERROR] Error checking LinearLayouts: {e}")

    # Step 5: Check for TextView elements (contact names)
    print("\n[STEP 6] Checking for TextViews (possible contact names)...")
    print("="*80)
    try:
        text_views = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")
        print(f"[DEBUG] Total TextViews found: {len(text_views)}")

        visible_texts = []
        for tv in text_views:
            try:
                if tv.is_displayed():
                    text = tv.get_attribute("text")
                    resource_id = tv.get_attribute("resource-id")
                    if text and text.strip():
                        visible_texts.append({
                            'text': text,
                            'resource_id': resource_id,
                            'location': tv.location
                        })
            except:
                continue

        print(f"\n[DEBUG] Found {len(visible_texts)} visible TextViews with text:")
        for idx, item in enumerate(visible_texts[:15]):  # Show first 15
            print(f"  {idx+1}. Text: '{item['text']}' | ID: {item['resource_id']} | Y: {item['location']['y']}")

    except Exception as e:
        print(f"[ERROR] Error checking TextViews: {e}")

    # Step 6: Check specific resource IDs commonly used for contacts
    print("\n[STEP 7] Checking common contact-related resource IDs...")
    print("="*80)
    contact_ids = [
        "com.whatsapp.w4b:id/contact_row_container",
        "com.whatsapp.w4b:id/contact_row",
        "com.whatsapp.w4b:id/contactpicker_row",
        "com.whatsapp.w4b:id/row",
        "com.whatsapp.w4b:id/conversation_contact_name",
        "com.whatsapp.w4b:id/conversations_row",
        "com.whatsapp:id/contact_row_container",
        "com.whatsapp:id/contact_row",
        "com.whatsapp:id/contactpicker_row",
        "com.whatsapp:id/row"
    ]

    for rid in contact_ids:
        try:
            elements = driver.find_elements(AppiumBy.ID, rid)
            if elements:
                print(f"  ✓ Found {len(elements)} elements with ID: {rid}")
                if len(elements) > 0:
                    print(f"    First element visible: {elements[0].is_displayed()}")
            else:
                print(f"  ✗ No elements with ID: {rid}")
        except Exception as e:
            print(f"  ✗ Error checking {rid}: {str(e)[:50]}")

    # Step 7: Try UiSelector approach
    print("\n[STEP 8] Testing UiSelector approaches...")
    print("="*80)
    try:
        # Try finding by UiSelector with className
        selectors_to_test = [
            'new UiSelector().className("android.widget.LinearLayout")',
            'new UiSelector().className("android.widget.RelativeLayout")',
            'new UiSelector().className("android.view.ViewGroup")',
            'new UiSelector().resourceIdMatches(".*contact.*")',
            'new UiSelector().resourceIdMatches(".*row.*")'
        ]

        for selector_str in selectors_to_test:
            try:
                xpath = f'//android.widget.*[@text]'
                elements = driver.find_elements(AppiumBy.ANDROID_UIAUTOMATOR, selector_str)
                print(f"  {selector_str}")
                print(f"    Found: {len(elements)} elements")
            except Exception as e:
                print(f"  {selector_str}")
                print(f"    Error: {str(e)[:80]}")

    except Exception as e:
        print(f"[ERROR] Error testing UiSelectors: {e}")

    print("\n" + "="*80)
    print("[COMPLETE] Check the 'mention_ui_hierarchy.xml' file for full details!")
    print("="*80)

    # Keep session open for 10 seconds
    print("\n[DEBUG] Keeping session open for 10 seconds for manual inspection...")
    time.sleep(10)

except Exception as e:
    print(f"\n[ERROR] Script failed: {e}")
    import traceback
    traceback.print_exc()

finally:
    print("\n[DEBUG] Closing driver...")
    driver.quit()
    print("[DEBUG] ✓ Driver closed")
