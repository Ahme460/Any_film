import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime

def login():
    email = email_entry.get()
    password = password_entry.get()
    email='ahmeoon1234@gmail.com'
    password='Mm55555#####'
    
    if not email or not password:
        messagebox.showwarning("Input Error", "Please enter both email and password")
        return
    
    # إعداد الخيارات وتحديد مسار geckodriver
    options = webdriver.FirefoxOptions()
    driver = webdriver.Firefox(options=options)
    
    try:
        # فتح صفحة الويب
        driver.get('https://egy.almaviva-visa.it/')
        for i in range(2):
            # انتظار ظهور زر تسجيل الدخول
            login_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[.//mat-icon[text()="person_outline"]]'))
            )
            login_button.click()

            # الانتظار لبضع ثواني حتى يتم تحميل صفحة تسجيل الدخول
            time.sleep(5)

            # تحديد حقل الإدخال باستخدام id
            username_field = driver.find_element(By.ID, "username")
            username_field.send_keys(email)
            time.sleep(5)
            
            # تحديد وإرسال كلمة المرور
            pass_field = driver.find_element(By.ID, 'password')
            pass_field.send_keys(password)
            time.sleep(5)

            # الضغط على زر تسجيل الدخول باستخدام JavaScript
            login_button = driver.find_element(By.ID, 'kc-login')
            driver.execute_script("arguments[0].click();", login_button)

            # الانتظار لبضع ثواني حتى يتم تحميل الصفحة الجديدة
            time.sleep(5)

            # الانتقال إلى صفحة الحجز
            driver.get('https://egy.almaviva-visa.it/appointment')

        check_availability_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//mat-icon[@data-mat-icon-type="font" and text()="chevron_right"]'))
        )

        # تحديد زر "Check availability" والنقر عليه في الوقت المحدد
        while True:
            time_now = datetime.now()
            if time_now.hour == 8 and time_now.minute == 59 and time_now.second == 59 and time_now.strftime('%p') == 'AM':
                time.sleep(0.9)
                try:
                    check_availability_button.click()
                    print("Button clicked at 09:00:00")
                    break
                except Exception as e:
                    print(f"Error: {e}")
            # الانتظار لمدة ثانية قبل التحقق مرة أخرى لتجنب استهلاك المعالج بشكل مفرط
            time.sleep(1)
            

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        print(e)
    finally:
        driver.quit()

# إعداد نافذة التطبيق
root = tk.Tk()
root.title("Visa Appointment Booker")
root.geometry('500x450') 

# إنشاء إطار لتوسيط عناصر الإدخال
frame = tk.Frame(root)
frame.place(relx=0.5, rely=0.5, anchor='center')

tk.Label(frame, text="Email:").grid(row=0, column=0, pady=10)
email_entry = tk.Entry(frame)
email_entry.grid(row=0, column=1, pady=10)

tk.Label(frame, text="Password:").grid(row=1, column=0, pady=10)
password_entry = tk.Entry(frame, show="*")
password_entry.grid(row=1, column=1, pady=10)

login_button = tk.Button(frame, text="Login", command=login)
login_button.grid(row=2, columnspan=2, pady=10)

root.mainloop()


