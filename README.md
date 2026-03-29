# 🦷 Clinic Management v1.0 — ERPNext v16
## نظام إدارة عيادات الأسنان والليزر

> ✅ متوافق مع ERPNext **v16.11.0** | Python **3.12+** | MariaDB **11.8**

## التثبيت على ERPNext v16

### الخطوة 1: ارفع على GitHub
```bash
git init
git checkout -b version-16
git add .
git commit -m "feat: initial clinic app for ERPNext v16"
git remote add origin https://github.com/YOUR_USERNAME/clinic_management.git
git push -u origin version-16
```

### الخطوة 2: ثبّت على السيرفر
```bash
cd /home/frappe/frappe-bench
bench get-app https://github.com/YOUR_USERNAME/clinic_management.git --branch version-16
bench --site YOUR_SITE install-app clinic_management
bench --site YOUR_SITE migrate
bench build --app clinic_management
bench restart
```

## GitHub Actions — Auto Deploy
ضيف في GitHub Secrets:
- SERVER_HOST, SERVER_USER, SERVER_SSH_KEY, SITE_NAME
