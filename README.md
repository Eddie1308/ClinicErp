# 🦷 Clinic Management - ERPNext Custom App
## نظام إدارة عيادات الأسنان والليزر

---

## المميزات
- ✅ ملف مريض كامل (بيانات شخصية + سجل طبي)
- ✅ حجز مواعيد مفصل (أسنان / ليزر)
- ✅ تحديد الأسنان المعالجة بالرقم
- ✅ الإجراء الطبي الكامل داخل كل مقابلة
- ✅ ربط تلقائي بفاتورة المبيعات
- ✅ دفع جزئي وأقساط مجدولة
- ✅ جدول الدكاترة وإتاحتهم
- ✅ تذكير تلقائي بالمواعيد
- ✅ إحصائيات ولوحة تحكم

---

## طريقة التثبيت على السيرفر

### الخطوة 1: رفع الكود على GitHub
```bash
git init
git add .
git commit -m "Initial clinic management app"
git remote add origin https://github.com/Eddie1308/clinicerp.git
git push -u origin main
```

### الخطوة 2: تثبيت App على ERPNext
اتصل بالسيرفر وشغّل الأوامر دي:

```bash
# الدخول على مجلد bench
cd /home/frappe/frappe-bench

# تنزيل الـ App من GitHub
bench get-app https://github.com/Eddie1308/clinicerp.git

# تثبيت الـ App على الـ Site بتاعك
bench --site YOUR_SITE_NAME install-app clinicerp

# تحديث الـ Site
bench --site YOUR_SITE_NAME migrate

# إعادة تشغيل الـ bench
bench restart
```

### الخطوة 3: إعداد الصلاحيات
في ERPNext اعمل الـ Roles دي:
- `Clinic Receptionist` - للاستقبال
- `Clinic Doctor` - للدكاترة

---

## هيكل الـ Doctypes

| Doctype | الوصف |
|---------|-------|
| Clinic Patient | ملف المريض الكامل |
| Clinic Appointment | الحجز والمقابلة الطبية |
| Tooth Treatment Detail | تفاصيل الأسنان المعالجة |
| Treatment Service Item | الخدمات والأسعار |
| Appointment Installment | جدول الأقساط |
| Doctor Schedule | إتاحة الدكاترة |

---

## ربط الفاتورة تلقائياً
عند تأكيد (Submit) الحجز، يتم تلقائياً:
1. إنشاء Sales Invoice في ERPNext
2. ربطها بالمريض كعميل
3. إضافة الخدمات كبنود في الفاتورة
4. تطبيق الخصم إن وجد

---

## للدعم والتطوير
تواصل مع مطوّر النظام لإضافة:
- تكامل WhatsApp API للتذكيرات
- تقارير مخصصة
- صورة الأسنان (Dental Chart)
