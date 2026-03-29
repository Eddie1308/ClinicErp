from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

setup(
    name="clinic_management",
    version="1.0.0",
    description="Dental & Laser Clinic Management for ERPNext",
    author="Clinic",
    author_email="admin@clinic.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires,
)
