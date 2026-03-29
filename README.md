# 1️⃣ ارفع على GitHub
git init && git add . && git commit -m "clinic app"
git remote add origin https://github.com/USERNAME/clinic_management.git
git push -u origin main

# 2️⃣ على السيرفر
cd /home/frappe/frappe-bench
bench get-app https://github.com/USERNAME/clinic_management.git
bench --site SITE_NAME install-app clinic_management
bench --site SITE_NAME migrate
bench restart
