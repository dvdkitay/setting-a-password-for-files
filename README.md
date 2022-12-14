<div align="left">
<img src="https://img.shields.io/github/languages/code-size/dvdkitay/setting-a-password-for-files" />
<img src="https://img.shields.io/github/languages/top/dvdkitay/setting-a-password-for-files" />
<div>

![Иллюстрация к проекту](https://raw.githubusercontent.com/dvdkitay/setting-a-password-for-files/master/static/img/screen.png)

## Описание

Приложение для предоставления ссылки на файлы пользователям с доступом по паролю. Под каждый файл есть возможность установить свой пароль. Генерируется одна ссылка для всех файлов с уникальным адресом. В Административной панели можно управлять ссылками. 


## Установка настройка сервера

Обновляем систему

```
sudo apt update
```

Устанавливаем веб сервер

```
apt install nginx -y
```

## Настройка сервера

Открыть конфигурационный файл nginx 

```
nano /etc/nginx/sites-available/default 
```

Добавить в раздел `location /`

```
proxy_pass http://localhost:5001;
```

После этого перезагружаем nginx 

```
service nginx restart
```

Создать папку `setting-a-password-for-files` на сервере в директории `root` и перенести файлы проекта в данную папку

```
mkdir setting-a-password-for-files
```

Установить домен в конфигурационном файле `lib/config.py`

```
url_web_site = "https://ваш_домен.ru"
```

Запустить установочный файл `install/install.bash`

```
cd install
```

```
chmod +x install.bash
```

```
./install.bash
```

## Запуск

Запустить браузер и пройти по домену или ip сервера

```
https://ваш_домен.ru/generate_config
```

На данной странице необходимо установить пароль для администратора и после этого авторизоваться в административной панели

