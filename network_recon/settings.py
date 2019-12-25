"""
Django settings for network_recon project.

Generated by 'django-admin startproject' using Django 2.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'wgg8n0hfceqw6rkvj)1kvitc71ifhowyi_i!_@wcpw%(mu%1yb'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'recon.apps.ReconConfig',
    'django_crontab'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'network_recon.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'network_recon.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'recon',
        'USER': 'root',         # 数据库用户名
        'PASSWORD': '123456',     # 密码
        'HOST': '127.0.0.1',    # 主机
        'PORT': '3306',
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

# 定时任务配置, 每日批量探测开始时间点, 日志存储位置
# python3 manage.py crontab add      添加crontab任务
# python3 manage.py crontab show     显示当前定时任务
# python3 manage.py crontab remove   移除定时任务
CRONJOBS = [
    ('1 0 * * *', 'recon.views.batch_scan', '>> /tmp/receive_scan.log')
]

# 扫描相关配置
zmap_result_path = '/opt/recon/zmap/'
banner_save_path = '/opt/recon/zgrab/'
ztag_save_path = '/opt/recon/ztag/'
report_save_path = '/opt/recon/report/'

zmap_white_path = '/opt/recon/scan/'
temp_file_path = '/opt/recon/temp/'
scan_file_path = '/opt/recon/fasts/'
# 单个任务最大IP数量
record_max_ips = 10000

# 即时扫描的发包速度(速度越快准确率越低)
fast_scan_rate = '1000'
# 正常接收扫描的发包速度(考虑扫描效率和预留出上传结果的带宽后尽量设置最大)
normal_scan_rate = '10000'

# sftp相关配置
sftp_host = '192.168.0.1'
sftp_port = 22333
sftp_username = 'root'
sftp_password = '12!QAZ2wsx'
sftp_remote = '/data/scan_receive/d1/'

# kafka相关配置
# kafka_host = '192.168.5.169:9092,192.168.5.169:9093'
# kafka_topics_prior = 'TOPSIGHT-AUTO-SCAN-PRIOR'
# kafka_topics_normal = 'TOPSIGHT-AUTO-SCAN'
