from flask import (
    Flask, request, render_template, jsonify, redirect, url_for, flash, session
)

from flask_login import (
    LoginManager, UserMixin, login_user, login_required, logout_user, current_user
)

import uuid 

from bson.objectid import ObjectId
import pymongo

import logging

from lib.processing import Processing
from lib.config import url_web_site

from datetime import date

# Конфигурация приложения
app = Flask(__name__)
app.config['SECRET_KEY'] = '187da333a1304a91b6dfec86b3abe1a0!'

# Подключение к локальной базе данных
connect = pymongo.MongoClient(
    f'mongodb://localhost:27017/')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'main_page'

db = connect["database"]

db_info = db["info"]
db_users = db["users"]

processing = Processing()

@login_manager.user_loader
def load_user(admin_id):
    user_json = db_users.find_one({'_id': ObjectId(admin_id)})
    return User_object_id(user_json)

class User_object_id(UserMixin):
    def __init__(self, user_json):
        self.user_json = user_json

    def get_id(self):
        object_id = self.user_json.get('_id')
        return str(object_id)


def is_auth_admin(func):
    """
    Декаратор для проверки сессии на наличие _user_id администратора.
    :return Выполняем функцию иначе перенаправляем на страницу ошибки.
    """
    def wrapper():
        if session and '_user_id' in session:
            
            ADMIN = db_users.find_one({})
            if str(session['_user_id']) == str(ADMIN["_id"]):
                return func()
            else:
                return redirect(url_for('main'))
        return redirect(url_for('main'))
    wrapper.__name__ = func.__name__
    return wrapper


@app.route('/')
def main():
    return render_template(
                'index.html', title="Главная страница"
            ) 
  
@app.route('/generate_config', methods=['GET', 'POST'])
def generate_config():
    
    if request.method == "POST":
        password_admin = request.form["password"]
        
        admin = dict(
            user="admin",
            password=password_admin
        )
        
        db_users.insert_one(admin) 
        return redirect(url_for('auth'))
    
    admin = db_users.find_one({})
    
    if not admin:
        return render_template(
                    'generate_config.html', title="Создание конфигурации"
                ) 
    else:
        return redirect(url_for('main'))
  
@app.route('/logout')
@is_auth_admin
def logout():
    """
    Очищает сессию и делает редирект на страницу авторизации.
    :return redirect(url_for('sign_in')
    """
    logout_user()
    return redirect(url_for('auth'))


@app.route('/files/check-password', methods=['POST'])
def check_password():
    if request.method == "POST":
        
        link = request.form["link"]
        password = request.form["password"]
        
        link_db = db_info.find_one({"link": link})
        
        try:
            if password == link_db["password_1"]:
                
                file_1 = link_db["file_1"]
                return render_template(
                'files.html', title="Файлы для скачивания", file=file_1, url_web_site=url_web_site
            )
                
            elif password == link_db["password_2"]:
                file_2 = link_db["file_2"]
                return render_template(
                'files.html', title="Файлы для скачивания", file=file_2, url_web_site=url_web_site
            )
                
            elif password == link_db["password_3"]:
                
                file_3 = link_db["file_3"]
                return render_template(
                'files.html', title="Файлы для скачивания", file=file_3, url_web_site=url_web_site
            )
                
        except Exception as err:
            pass

        flash("Пароль не верный")
        return redirect(url_for('txns', link=link)) 
        
    
@app.route('/files/<string:link>', methods=['GET'])
def txns(link):
    
    link_output = db_info.find_one({"link": link})
    
    if not link_output:
        return redirect(url_for('main')) 
    
    return render_template(
                'password.html', title="Файлы для скачивания", link_output=link_output
            )
    
@app.route('/admin', methods=['GET'])
@is_auth_admin
def admin():
    return render_template(
                '/admin/admin.html', title="Административная панель"
            ) 


@app.route('/admin/auth', methods=['GET', 'POST'])
def auth():
    
    if request.method == "POST":
        password = request.form["password"]
        admin = db_users.find_one({"user": "admin"})
                
        if password != admin["password"]:
            return redirect(url_for("auth")) 
        
        loginuser = load_user(admin['_id'])
        login_user(loginuser, remember=True)
        
        return redirect(url_for("admin")) 
        
    return render_template(
                '/admin/auth.html', title="Авторизация"
            ) 


@app.route('/admin/link-generation', methods=['GET'])
@is_auth_admin
def link_generation():
    return render_template(
                '/admin/link-generation.html', title="Генерация ссылки"
            ) 
 

@app.route('/admin/status_true', methods=['POST'])
@is_auth_admin
def status_true():
    
    if request.method == "POST":
        
        id = request.form["id"]
        db_info.update_one({'_id': ObjectId(id)}, {"$set": {
                                                "status": True}}, upsert=True)
    
    flash("Ссылка успешно включена")
    return redirect(url_for('links')) 


@app.route('/admin/status_false', methods=['POST'])
@is_auth_admin
def status_false():
    
    if request.method == "POST":
        
        id = request.form["id"]
        db_info.update_one({'_id': ObjectId(id)}, {"$set": {
                                                "status": False}}, upsert=True)
    
    flash("Ссылка успешно включена")
    return redirect(url_for('links')) 
 

@app.route('/admin/delete_link', methods=['POST'])
@is_auth_admin
def delete_link():
    if request.method == "POST":
        
        id = request.form["id"]
        
        db_info.delete_one({'_id': ObjectId(id)})

    flash("Ссылка успешно удалена")
    return redirect(url_for('links'))    

@app.route('/admin/links', methods=['GET'])
@is_auth_admin
def links():
    
    is_link = db_info.find_one({})
    links = db_info.find({})
    
    return render_template(
                '/admin/links.html', title="Доступные ссылки", is_link=is_link, links=links, url_web_site=url_web_site
            ) 
    
    
@app.route('/admin/generation', methods=['POST'])
@is_auth_admin
def generation():
    
    if request.method == "POST":
        
        name = request.form["name"]
        
        password_1 = request.form["password_1"]
        password_2 = request.form["password_2"]
        password_3 = request.form["password_3"]
        
        file_1 = request.files["file_1"]
        file_2 = request.files["file_2"]
        file_3 = request.files["file_3"]
        
        current_datetime = str(date.today())
        
        if file_1 and file_2 and file_3:
            
            status_save_file_1 = processing.save_file(file_1)
            status_save_file_2 = processing.save_file(file_2)
            status_save_file_3 = processing.save_file(file_3)
            
            if not status_save_file_1 or not status_save_file_2 or not status_save_file_3:
                flash("Ошибка сохранения файлов. Ссылка не сгенерирована")
                return redirect(url_for('link_generation')) 
            
            link = str(uuid.uuid4().int)[:21]
            
            try:
                new_link = dict(
                    name=name,
                    file_1=status_save_file_1,
                    file_2=status_save_file_2,
                    file_3=status_save_file_3,
                    password_1=password_1,
                    password_2=password_2,
                    password_3=password_3,
                    current_datetime = current_datetime,
                    link=link,
                    status=False,
                )
                
                db_info.insert_one(new_link)
            except Exception as err:
                flash("Ошибка генерации ссылки")
                return redirect(url_for('link_generation'))
            
        elif file_1 and file_2:
            
            status_save_file_1 = processing.save_file(file_1)
            status_save_file_2 = processing.save_file(file_2)
            
            if not status_save_file_1 or not status_save_file_2:
                flash("Ошибка сохранения файлов. Ссылка не сгенерирована")
                return redirect(url_for('link_generation')) 
            
            link = str(uuid.uuid4().int)[:12]
            
            try:
                new_link = dict(
                    name=name,
                    file_1=status_save_file_1,
                    file_2=status_save_file_2,
                    password_1=password_1,
                    password_2=password_2,
                    current_datetime = current_datetime,
                    link=link,
                    status=False,
                )
                
                db_info.insert_one(new_link)
            except Exception as err:
                print(err)
                flash("Ошибка генерации ссылки")
                return redirect(url_for('link_generation'))
        else:
            flash("Ошибка генерации ссылки. Необходимо добавить 2 или 3 файла")
            return redirect(url_for('link_generation'))
        
    flash(f"Успешная генерация ссылки {link}")
    return redirect(url_for('links')) 


app.run(debug=True, port=5001)