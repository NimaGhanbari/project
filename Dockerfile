# انتخاب تصویر پایه
FROM python:3.10

# تنظیم دایرکتوری کاری
WORKDIR /app

# کپی کردن فایل‌های پروژه
COPY requirements.txt /app/

# نصب وابستگی‌ها
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# کپی کردن باقی‌مانده‌ی فایل‌های پروژه
COPY . /app/

# تنظیمات برای اجرا
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
