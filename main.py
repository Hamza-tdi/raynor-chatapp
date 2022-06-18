import time
import os
import json
from cryptography.fernet import Fernet
from flask import Flask, render_template, url_for, redirect, flash, request, Response, jsonify
from flask_socketio import SocketIO, send, leave_room, join_room
from werkzeug.exceptions import abort
from wtf_forms import *
from models import *
from passlib.hash import pbkdf2_sha256
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from werkzeug.utils import secure_filename
from flask import send_from_directory


# CONSTANTS
WD_PATH = os.path.dirname(os.path.realpath(__file__))
NAME_KEY = 'name'
ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET')
socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")


# DATA BASE
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['FILE_UPLOADS'] = os.path.join(WD_PATH, 'static/files/upload')
app.config['ALLOWED_FILES_EXTENSIONS'] = ['DOCX', 'DOC', 'DOTX', 'XLSX', 'PPTX', 'PPT', 'XLS', 'PDF', 'PNG', 'JPG', 'JPEG', 'GIF']

db = SQLAlchemy(app)


# Configure flask login
login = LoginManager(app)
login.init_app(app)


# Generate Keys
public_key = 123456789
private_key = 987654321


@login.user_loader
def load_user(user_id):

    return User.query.get(int(user_id))


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    # Logout user
    logout_user()
    flash('You have logged out successfully', 'success')
    return redirect(url_for('login'))


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if not current_user.is_authenticated:
        flash('Please login', 'danger')
        return redirect(url_for('login'))
    elif current_user.account_status == 'disabled':
        return 'disabled page'

    # load room list
    rooms = Room.query.all()
    room_list = []
    for room in rooms:
        room_list.append({'room_name': room.room_name, 'is_active': room.is_active})

    return render_template("chat.html", username=current_user.full_name, rooms=room_list)


@app.route('/dashboard/add_room', methods=['GET', 'POST'])
def add_room():
    print(request.method)
    if request.method == 'POST':
        if request.form.get('room_name'):
            # store new room to db
            room = Room(room_name=request.form.get('room_name'), nbr_users=0, is_active='YES')
            db.session.add(room)
            db.session.commit()
            db.session.remove()
    return redirect(url_for('manage_rooms'))


@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    """ upload file to server and send it to clients """
    def allowed_files(filename):
        if not '.' in filename:
            return False
        ext = filename.rsplit('.', 1)[1]
        if ext.upper() in app.config['ALLOWED_FILES_EXTENSIONS']:
            return True
        else:
            return False

    if request.method == 'POST':
        if request.files:
            file = request.files['file']
            if not file.filename == '':
                if allowed_files(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['FILE_UPLOADS'], filename))
    return redirect(url_for('chat'))


@app.route('/get-file/<path:file_name>', methods=['GET', 'POST'])
def get_file(file_name):
    try:
        print(app.config['FILE_UPLOADS'], '\n', file_name)
        return send_from_directory(
            app.config['FILE_UPLOADS'],
            file_name,
            as_attachment=False
        )
    except FileNotFoundError:
        abort(404)


@app.route('/download_history/<room>', methods=['GET', 'POST'])
def get_history(room):
    messages = Message.query.filter_by(message_room=room).all()
    messages_list = []
    for message in messages:
        if message.message_type == 'TEXT':
            # decrypt message
            crypter = Fernet(os.environ.get('KEY'))
            decrypted_msg = crypter.decrypt(message.message_text.encode())
            _dict = {'id': message.id, 'message_sender': message.message_sender, 'message_time': message.message_time,
                     'message_room': message.message_room, 'message_text': decrypted_msg.decode()}
            messages_list.append(_dict)

    return {'messages_list': messages_list}


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if not current_user.is_authenticated:
        flash('Please login.', 'danger')
        return redirect(url_for('login'))

    if current_user.role != 'admin':
        return redirect(url_for('chat'))

    return render_template('dashboard.html')


@app.route('/dashboard/manage_rooms', methods=['GET', 'POST'])
def manage_rooms():
    if current_user.is_authenticated and current_user.role == 'admin':
        rooms = Room.query.all()
        rooms_list = []
        for room in rooms:
            _dict = {'id': room.id, 'room_name': room.room_name, 'nbr_users': room.nbr_users, 'is_active': room.is_active}
            rooms_list.append(_dict)
        print(rooms_list)
        return render_template('manage_rooms.html', data=rooms_list)
    else:
        rooms = Room.query.all()
        room_list = []
        for room in rooms:
            room_list.append(room.room_name)
        return render_template('chat.html', username=current_user.full_name, rooms=room_list)


@app.route('/dashboard/manage_users', methods=['GET', 'POST'])
def manage_users():
    if current_user.is_authenticated and current_user.role == 'admin':
        users = User.query.all()
        users_list = []
        for user in users:
            _dict = {'id': user.id, 'username': user.full_name, 'role': user.role, 'account_status': user.account_status}
            users_list.append(_dict)
        return render_template('manage_users.html', data=users_list)
    else:
        rooms = Room.query.all()
        room_list = []
        for room in rooms:
            room_list.append(room.room_name)
        return render_template('chat.html', username=current_user.full_name, rooms=room_list)


@app.route('/register',  methods=['GET', 'POST'])
def register():
    reg_form = RegistrationForm()
    print('test')
    print(reg_form.validate_on_submit())
    if reg_form.validate_on_submit():
        print('valid')
        first_name = reg_form.first_name.data
        last_name = reg_form.last_name.data
        birth_date = reg_form.birth_date.data
        phone_number = reg_form.phone_number.data
        email_address = reg_form.email_address.data
        address = reg_form.address.data
        zipcode = reg_form.zipcode.data
        genre = reg_form.genre.data
        title = reg_form.title.data
        department = reg_form.department.data
        password = reg_form.password.data
        hashed_pswd = pbkdf2_sha256.hash(password)

        user = User(first_name=first_name, last_name=last_name, full_name=f'{first_name} {last_name}',
                    birth_date=f'{birth_date.day}/{birth_date.month}/{birth_date.year}', phone_number=phone_number,
                    email_address=email_address, address=address, zipcode=zipcode, genre=genre, title=title,
                    department=department, password=hashed_pswd, role='user', account_status='enabled')
        db.session.add(user)
        db.session.commit()
        db.session.remove()
        flash('Registered successfully. Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=reg_form)


@app.route('/',  methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if not current_user.is_authenticated:
        login_form = LoginForm()
        if login_form.validate_on_submit():
            user_object = User.query.filter_by(full_name=login_form.full_name.data).first()
            login_user(user_object)
            if current_user.is_authenticated and current_user.account_status == 'enabled':
                flash('You are logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                return 'account disabled page'

        return render_template('login.html', form=login_form)
    else:
        # load room list
        rooms = Room.query.all()
        room_list = []
        for room in rooms:
            room_list.append(room.room_name)
        return render_template('chat.html', username=current_user.full_name, rooms=room_list)


@socketio.on('incoming-msg')
def on_message(data):
    """Broadcast messages"""
    if data['message_type'] == 'FILE':
        msg = data["msg"]
        msg = msg.split('\\')[-1]
    else:
        msg = data["msg"]
    username = data["username"]
    room = data["room"]
    msg_type = data["message_type"]
    # Set timestamp
    time_stamp = time.strftime('%b-%d %I:%M%p', time.localtime())
    if not data['message_type'] == 'FILE':
        send({"username": username, "msg": msg, "time_stamp": time_stamp}, room=room)
    # decrypting and storing message instance

    crypter = Fernet(os.environ.get('KEY'))
    msg = crypter.encrypt(msg.encode())
    message_db = Message(message_text=msg.decode(), message_sender=username, message_time=time_stamp, message_room=room, message_type=msg_type)
    db.session.add(message_db)
    db.session.commit()
    db.session.remove()


@socketio.on('promote_user')
def on_promote(data):
    """ promote user to admin"""
    if 'user' in data['user'].lower():
        """ promote user to admin """
        username, role = data['user'].split('_')
        user = User.query.filter_by(username=username).first()
        user.role = 'admin'
        db.session.merge(user)
        db.session.commit()
        db.session.remove()
    else:
        """ demote user """
        username, role = data['user'].split('_')
        user = User.query.filter_by(username=username).first()
        user.role = 'user'
        db.session.merge(user)
        db.session.commit()
        db.session.remove()


@socketio.on('disable_room')
def on_disable_room(data):
    """ disable room """
    if not 'NO' in data['room']:
        room = Room.query.filter_by(room_name=data['room'].split('_')[0]).first()
        room.is_active = 'NO'
        db.session.merge(room)
        db.session.commit()
        db.session.remove()
    else:
        room = Room.query.filter_by(room_name=data['room'].split('_')[0]).first()
        room.is_active = 'YES'
        db.session.merge(room)
        db.session.commit()
        db.session.remove()


@socketio.on('disable_user')
def on_disable(data):
    """ delete user or admin"""
    if data:
        username, role = data['user'].split('_')
        user = User.query.filter_by(username=username).first()
        if user:
            if user.account_status == 'enabled':
                user.account_status = 'disabled'
                db.session.merge(user)
                db.session.commit()
                db.session.remove()
            else:
                user.account_status = 'enabled'
                db.session.merge(user)
                db.session.commit()
                db.session.remove()
        else:
            pass


@socketio.on('join')
def on_join(data):
    """User joins a room"""

    username = data["username"]
    room = data["room"]
    join_room(room)
    # send messages to join room event
    messages = Message.query.filter_by(message_room=data['room']).all()
    msg_list = []

    # decrypt message content
    crypter = Fernet(os.environ.get('KEY'))

    for msg in messages:
        decrypted_msg = crypter.decrypt(msg.message_text.encode())

        _dict = {'message_sender': msg.message_sender, 'message_text': decrypted_msg.decode(),
                 'message_room': msg.message_room, 'message_time': msg.message_time, 'message_type': msg.message_type}
        msg_list.append(_dict)
    socketio.emit('join_room', {'user': current_user.full_name, 'data': msg_list})

    # add user to room record
    room_db = Room.query.filter_by(room_name=data['room']).first()
    room_db.nbr_users += 1
    db.session.commit()
    db.session.remove()

    # Broadcast that new user has joined
    send({"msg": username + " has joined the " + room + " room."}, room=room)


@socketio.on('leave')
def on_leave(data):
    """User leaves a room"""

    username = data['username']
    room = data['room']
    leave_room(room)
    send({"msg": username + " has left the room"}, room=room)


if __name__ == '__main__':
    app.run()
