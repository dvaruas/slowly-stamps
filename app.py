import os
import random
import string
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, send_from_directory


RESOURCES_PATH = os.path.join(os.path.dirname(__file__), "resources")
DB_PATH = os.path.join(RESOURCES_PATH, "data.db")
USER_IMAGES_PATH = os.path.join(RESOURCES_PATH, "users")
STAMP_IMAGES_PATH = os.path.join(RESOURCES_PATH, "stamps")
NUM_IN_ROW = 6

app = Flask(__name__)


@app.route('/user_image/<filename>')
def user_image(filename):
    return send_from_directory(USER_IMAGES_PATH, filename)


@app.route('/')
@app.route('/users')
def list_users():
    db = sqlite3.connect(DB_PATH)
    conn = db.cursor()
    conn.execute("select count(*) from users")
    num_users = conn.fetchone()[0]
    conn.execute("select count(*) from stamps")
    num_stamps = conn.fetchone()[0]
    conn.execute("select id, name, image_id from users")
    users = {}
    for row in conn:
        users[row[0]] = {"id" : row[0], "name" : row[1], "image" : row[2]}
    for u_id in users.keys():
        conn.execute(f"select count(*) from used_stamps where user_id = {u_id}")
        users[u_id]["count"] = int(conn.fetchone()[0])

    arranged_u_ids = sorted(users.keys(), key=lambda x:users[x]["count"], reverse=True)

    show_users = []
    user_row = ["add_user"]
    for id in arranged_u_ids[:(NUM_IN_ROW - 1)]:
        user_row.append({"id" : users[id]["id"], "name" : users[id]["name"], "image" : users[id]["image"]})
    show_users.append(user_row)

    user_row = []
    i = 0
    for id in arranged_u_ids[NUM_IN_ROW - 1:]:
        user_row.append({"id" : users[id]["id"], "name" : users[id]["name"], "image" : users[id]["image"]})
        i += 1
        if i == NUM_IN_ROW:
            i = 0
            show_users.append(user_row)
            user_row = []
    if user_row:
        show_users.append(user_row)

    conn.close()
    return render_template("users.html", users=show_users, num_in_rows=NUM_IN_ROW, num_users=num_users,
        num_stamps=num_stamps)


@app.route('/user/<userid>')
def user_detail(userid):
    db = sqlite3.connect(DB_PATH)
    conn = db.cursor()
    conn.execute(f"select name, image_id from users where id is {userid}")
    user_info = [{"id" : userid, "name" : row[0], "image_id" : row[1]} for row in conn]
    if len(user_info) == 1:
        conn.execute("select count(*) from users")
        num_users = conn.fetchone()[0]
        conn.execute("select count(*) from stamps")
        num_stamps = conn.fetchone()[0]

        user_info = user_info[0]
        conn.execute(f"select stamp_id from used_stamps where user_id is {userid}")
        used_stamps = [row[0] for row in conn]

        conn.execute("select id, name from stamp_categories")
        categories = dict([(row[0], row[1]) for row in conn])
        stamps_dict = {}
        for category_id, category_name in categories.items():
            conn.execute(f"select id, name, image_id from stamps where category_id is {category_id}")
            i = 0
            stamp_row = []
            stamps = []
            for row in conn:
                if row[0] in used_stamps:
                    continue
                stamp_row.append({"id" : row[0], "name" : row[1], "image" : row[2]})
                i += 1
                if i == NUM_IN_ROW:
                    i = 0
                    stamps.append(stamp_row)
                    stamp_row = []
            if stamp_row:
                stamps.append(stamp_row)
            if stamps:
                stamps_dict[category_name] = stamps

        return render_template("user_detail.html", stamps=stamps_dict, num_in_rows=NUM_IN_ROW,
            num_users=num_users, num_stamps=num_stamps, user_info=user_info)

    return redirect(url_for('list_users'))


@app.route('/add_user', methods=['GET', 'POST'])
def add_new_user():
    db = sqlite3.connect(DB_PATH)
    conn = db.cursor()
    if request.method == 'POST':
        penPalName = request.form['penPalName'].strip()
        penPalName = penPalName.replace("'", "''")

        penPalImage = request.files.get('penPalImage', None)
        new_file_name = None
        if penPalImage and penPalImage.filename != '':
            while True:
                new_file_name = ''.join((random.choice(string.ascii_letters + string.digits) for i in range(10)))
                if new_file_name not in os.listdir(USER_IMAGES_PATH):
                    break
            penPalImage.save(os.path.join(USER_IMAGES_PATH, new_file_name))

        if new_file_name:
            conn.execute(f"insert into users (name, image_id) values ('{penPalName}', '{new_file_name}')")
        else:
            conn.execute(f"insert into users (name) values ('{penPalName}')")

        db.commit()
        conn.close()
        return redirect(url_for('list_users'))
    else:
        conn.execute("select count(*) from users")
        num_users = conn.fetchone()[0]
        conn.execute("select count(*) from stamps")
        num_stamps = conn.fetchone()[0]
        conn.close()
        return render_template("add_user.html", num_users=num_users, num_stamps=num_stamps)

@app.route('/edit/<userid>', methods=['GET', 'POST'])
def edit_existing_user(userid):
    db = sqlite3.connect(DB_PATH)
    conn = db.cursor()
    if request.method == 'POST':
        conn.execute(f"select name, image_id from users where id is {userid}")
        prev_name, prev_image_id = conn.fetchone()

        penPalName = request.form['penPalName'].strip()
        if penPalName != prev_name:
            penPalName = penPalName.replace("'", "''")
            conn.execute(f"update users set name = '{penPalName}' where id is {userid}")

        penPalImage = request.files.get('penPalImage', None)
        new_file_name = None
        if penPalImage and penPalImage.filename != '':
            while True:
                new_file_name = ''.join((random.choice(string.ascii_letters + string.digits) for i in range(10)))
                if new_file_name not in os.listdir(USER_IMAGES_PATH):
                    break
            penPalImage.save(os.path.join(USER_IMAGES_PATH, new_file_name))
            os.remove(os.path.join(USER_IMAGES_PATH, prev_image_id))
            conn.execute(f"update users set image_id = '{new_file_name}' where id is {userid}")

        db.commit()
        conn.close()
        return redirect(url_for('list_users'))
    else:
        conn.execute("select count(*) from users")
        num_users = conn.fetchone()[0]
        conn.execute("select count(*) from stamps")
        num_stamps = conn.fetchone()[0]
        conn.execute(f"select name, image_id from users where id is {userid}")
        user_name, user_image_id = conn.fetchone()
        conn.close()
        return render_template("edit_user.html", num_users=num_users, num_stamps=num_stamps,
            user_id=userid, user_name=user_name, user_image_id=user_image_id)


@app.route('/delete/<userid>')
def delete_user(userid):
    db = sqlite3.connect(DB_PATH)
    conn = db.cursor()
    conn.execute(f"delete from users where id={userid}")
    conn.execute(f"delete from used_stamps where user_id={userid}")
    db.commit()
    conn.close()
    return redirect(url_for('list_users'))


@app.route('/stamp_image/<filename>')
def stamp_image(filename):
    return send_from_directory(STAMP_IMAGES_PATH, filename)


@app.route('/stamps')
def list_stamps():
    db = sqlite3.connect(DB_PATH)
    conn = db.cursor()
    conn.execute("select count(*) from users")
    num_users = conn.fetchone()[0]
    conn.execute("select count(*) from stamps")
    num_stamps = conn.fetchone()[0]
    conn.execute("select id, name from stamp_categories")
    categories = dict([(row[0], row[1]) for row in conn])
    stamps_dict = {}
    for category_id, category_name in categories.items():
        conn.execute(f"select id, name, image_id from stamps where category_id is {category_id}")
        i = 0
        stamp_row = []
        stamps = []
        for row in conn:
            stamp_row.append({"id" : row[0], "name" : row[1], "image" : row[2]})
            i += 1
            if i == NUM_IN_ROW:
                i = 0
                stamps.append(stamp_row)
                stamp_row = []
        if stamp_row:
            stamps.append(stamp_row)
        stamps_dict[category_name] = stamps
    conn.close()
    return render_template("stamps.html", stamps=stamps_dict, num_in_rows=NUM_IN_ROW,
        num_users=num_users, num_stamps=num_stamps)


@app.route('/add_stamp', methods=['GET', 'POST'])
def add_new_stamp():
    db = sqlite3.connect(DB_PATH)
    conn = db.cursor()
    if request.method == 'POST':
        chosen_category = request.form.getlist('category-radio')
        category_id = None
        if chosen_category:
            chosen_category = chosen_category[0]
            if chosen_category == "newCategory":
                if request.form['newCategoryName']:
                    newCategoryName = request.form['newCategoryName'].strip()
                    newCategoryName = newCategoryName.replace('"', "'")
                    newCategoryName = newCategoryName.replace("'", "''")
                    conn.execute(f"insert into stamp_categories (name) values ('{newCategoryName}')")
                    conn.execute(f"select id from stamp_categories where name is '{newCategoryName}'")
                    category_id = conn.fetchone()[0]
            else:
                category_id = chosen_category

            if category_id:
                stampName = request.form['inputStampName'].strip()
                stampName = stampName.replace('"', "'")
                stampName = stampName.replace("'", "''")

                stampImage = request.files.get('stampImage', None)
                new_file_name = None
                if stampImage and stampImage.filename != '':
                    while True:
                        new_file_name = ''.join((random.choice(string.ascii_letters + string.digits) for i in range(10)))
                        if new_file_name not in os.listdir(STAMP_IMAGES_PATH):
                            break
                    stampImage.save(os.path.join(STAMP_IMAGES_PATH, new_file_name))

                if new_file_name:
                    conn.execute(f"insert into stamps (name, category_id, image_id) values ('{stampName}', {category_id}, '{new_file_name}')")
                else:
                    conn.execute(f"insert into stamps (name, category_id) values ('{stampName}', {category_id})")

            db.commit()
        conn.close()
        return redirect(url_for('list_stamps'))

    conn.execute("select count(*) from users")
    num_users = conn.fetchone()[0]
    conn.execute("select count(*) from stamps")
    num_stamps = conn.fetchone()[0]
    conn.execute("select id, name from stamp_categories")
    all_categories = [{"cid" : row[0], "cname" : row[1]} for row in conn]
    conn.close()
    return render_template("add_stamp.html", num_users=num_users, num_stamps=num_stamps,
        all_categories=all_categories)


@app.route('/use/<use_info>')
def save_used_stamps(use_info):
    db = sqlite3.connect(DB_PATH)
    conn = db.cursor()
    info_parts = use_info.split("-")
    if len(info_parts) == 2:
        user_id, stamp_id = info_parts
        conn.execute(f"insert into used_stamps (user_id, stamp_id) values ({user_id}, {stamp_id})")
        db.commit()
    conn.close()
    return redirect(url_for('list_users'))


if __name__ == '__main__':
    if not os.path.exists(RESOURCES_PATH):
        os.mkdir(RESOURCES_PATH)
    if not os.path.exists(USER_IMAGES_PATH):
        os.mkdir(USER_IMAGES_PATH)
    if not os.path.exists(STAMP_IMAGES_PATH):
        os.mkdir(STAMP_IMAGES_PATH)

    db = sqlite3.connect(DB_PATH)
    conn = db.cursor()
    conn.execute("create table if not exists users ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "name TEXT NOT NULL, image_id TEXT)")
    conn.execute("create table if not exists stamp_categories ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL)")
    conn.execute("create table if not exists stamps ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "name TEXT NOT NULL, "
        "category_id INTEGER references stamp_categories(id) ON DELETE CASCADE, "
        "image_id TEXT)")
    conn.execute("create table if not exists used_stamps ("
        "user_id INTEGER references users(id) ON DELETE CASCADE, "
        "stamp_id INTEGER references stamps(id) ON DELETE CASCADE)")
    conn.close()

    app.run(host='0.0.0.0')
