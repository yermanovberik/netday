from pathlib import Path

from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR, ".env"))

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = bool(os.getenv('DEBUG', True))
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(' ')

CORS_ORIGIN_ALLOW_ALL = bool(os.getenv('CORS_ORIGIN_ALLOW_ALL', True))
CORS_ORIGIN_WHITELIST = os.getenv('CORS_ORIGIN_WHITELIST').split(' ')

if not DEBUG and not CORS_ORIGIN_ALLOW_ALL:
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

FRONTEND_INDEX_PAGE_URL = os.getenv("FRONTEND_INDEX_PAGE_URL")
PAYMENT_CONFIRMATION_URL = os.getenv("PAYMENT_CONFIRMATION_URL")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "paypalrestsdk",
    "paypal.standard.ipn",
    "rest_framework",
    "netday",
    "corsheaders",
]

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_PORT = int(os.getenv("EMAIL_PORT"))
EMAIL_BACKEND = os.getenv("EMAIL_BACKEND")
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS")

PAYMENT_AMOUNT = os.getenv("PAYMENT_AMOUNT")
PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID")
PAYPAL_CLIENT_SECRET = os.getenv("PAYPAL_CLIENT_SECRET")
PAYPAL_MODE = os.getenv("PAYPAL_MODE")
PAYPAL_RECEIVER_EMAIL = os.getenv("PAYPAL_RECEIVER_EMAIL")
PAYPAL_TEST = bool(os.getenv("PAYPAL_TEST"))

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]

ROOT_URLCONF = "netday.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates']
        ,
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "netday.wsgi.application"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
SITE_ID = 1
USE_TZ = True

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

STATIC_URL = '/staticfiles/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

EMAIL_MESSAGE = """
Dear participant,

It is our pleasure to have you as a participant in the NetDay event!
Here is information about the first round of the Olympiad.

The date of the first (preliminary) tour is on the 4th of November
Time: start login time: 18:00 - end login time: 19:00 UTC+06:00 (+6)
(you can start anytime during 18:00-19:00, e.g if you start the exam at 18:10, the exam finishes at 19:10 for you)
Duration: 1 hour
Format: Online, multiple-choice, True and False, Fill-in questions
 
The day of the exam:

You will receive a link to the exam on the day of the preliminary tour. In case of the successful completion of the exam, a limited amount of students will be forwarded to the next tour, which will be offline at the SDU campus. 
Before starting the exam make sure of 3 rules:
·        Good internet connection
·        Quiet place and being alone during preliminary exam
·        No gadgets and headphones (earphones, AirPods and etc)
 
For instructions and rules of the first round of NetDay, see the link https://docs.google.com/document/d/1dMC2RCKnpZ4_uhNHabZshdIgaSIN9Ahaac7zJ8qeIh0/edit?usp=sharing 

Wait for updates and news from our official telegram: https://t.me/sdunetday 
Contact us for any questions and concerns at netday2@sdu.edu.kz or telegram

******
Құрметті Олимпиада қатысушысы,
 
Сізді NetDay олимпиадасының қатысушысы ретінде көргенімізге қуаныштымыз.
Осы хабарламада олимпиаданың бірінші туры туралы ақпарат берілген
 
Бірінші тур 4 қарашада болады
Жүйеге кірудің басталу уақыты: 18:00 - кірудің аяқталу уақыты: 19:00 UTC+06:00 (+6) 
(сіз 18:00-ден 19:00-ге дейін кез келген уақытта бастай аласыз, мысалы, емтиханды 18:10-да бастасаңыз, емтихан сіз үшін 19:10-да аяқталады)
Емтихан ұзақтығы: 1 сағат
Форматы: онлайн

Емтихан алдында:
Сіз емтиханға сілтемені алдын ала Бірінші тур өтетін күні аласыз. Емтиханды сәтті тапсырған жағдайда үздік студенттер СДУ кампусында офлайн режимде өтетін келесі турға жіберіледі.
 
Емтиханды бастамас бұрын мына 3 ережені орындағаныңызға көз жеткізіңіз:
·        Жақсы интернет байланыстың болуы
·        Емтихан кезінде тыныш әрі жалғыз болу
·        Гаджеттер немесе құлаққаптардың (airPods, т.б.) болмауы
 
NetDay бірінші раундының нұсқаулары мен ережелері осы сілтемеден қараңыз https://docs.google.com/document/d/1dMC2RCKnpZ4_uhNHabZshdIgaSIN9Ahaac7zJ8qeIh0/edit?usp=sharing 

Жаңартулар мен жаңалықтар біздің ресми телеграм каналда жарияланады: https://t.me/sdunetday 
Сұрақтарыңызды электронды поштаға (netday2@sdu.edu.kz) немесе телеграм арқылы қойсаңыз болады
 

******
Уважаемый участник,
 
Мы рады видеть вас в качестве участника Олимпиады NetDay.
Перед Вами информация о первом туре олимпиады
 
Дата первого (предварительного) тура - 4 ноября.
Время начала входа: 18:00 - время окончания входа: 19:00 UTC+06:00 (+6) 
(вы можете начать экзамен с 18:00 до 19:00, например, если вы начнете экзамен в 18:10, экзамен заканчивается для вас в 19:10)
Продолжительность экзамена: 1 час
Формат: онлайн 
 
В день олимпиады:
Ссылку на экзамен Вы получите в день предварительного тура. В случае успешной сдачи ограниченное количество студентов будут направлены на следующий тур, который будет проходить в формате оффлайн на кампусе СДУ.
 
Перед началом экзамена убедитесь в соблюдении 3х правил:
·   Хорошее интернет соединение
·   Тихое место во время предварительного экзамена
·   Никаких гаджетов и наушников (наушники, airPods и т.п.)
 
Инструкции и правила первого тура NetDay смотрите по ссылке https://docs.google.com/document/d/1dMC2RCKnpZ4_uhNHabZshdIgaSIN9Ahaac7zJ8qeIh0/edit?usp=sharing 

Новости и обновления можете отследить у нас в официальном телеграм канале: https://t.me/sdunetday
При возникновении вопросов пишите на netday2@sdu.edu.kz или в чат телеграм канала
"""
