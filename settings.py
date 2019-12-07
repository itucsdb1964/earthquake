DEBUG = True
PORT = 8080
SECRET_KEY = "secret"
WTF_CSRF_ENABLED = True
# admin : passwordofadmin  // normaluser : passwordofuser
PASSWORDS = {
    "admin": "$pbkdf2-sha256$29000$LSVkzBnjHCOk1Nqb01pLKQ$5QaEe0mMR2Q.c8ouz3mDEy5MBhGSCY.j1bWNCmUlL1c",
    "normaluser": "$pbkdf2-sha256$29000$mBMixJgzRggBoJQyBkCIUQ$U/veUNTlVY8cbStzMH5QttiA.37LT8jCYoRk7p7e8qM",
}

ADMIN_USERS = ["admin"]