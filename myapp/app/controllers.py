import os
import random
import string
from flask import (Blueprint, request, render_template, redirect, url_for,
    send_from_directory, current_app)

from app.models import Users, Stamps, StampCategories
from app import db


NUM_IN_ROW = 6

app_mod = Blueprint('slowly-module', __name__)


@app_mod.route('/')
@app_mod.route('/users')
def list_users():
    num_users = Users.query.count()
    num_stamps = Stamps.query.count()

    users = {}
    for row in Users.query.all():
        users[row.id] = {"name" : row.name, "image" : row.image_id,
            "count" : len(row.used_stamps)}

    arranged_u_ids = sorted(users.keys(), key=lambda x:users[x]["count"], reverse=True)

    show_users = []
    user_row = ["add_user"]
    for id in arranged_u_ids[:(NUM_IN_ROW - 1)]:
        user_row.append({"id" : id, "name" : users[id]["name"], "image" : users[id]["image"]})
    show_users.append(user_row)

    user_row = []
    i = 0
    for id in arranged_u_ids[NUM_IN_ROW - 1:]:
        user_row.append({"id" : id, "name" : users[id]["name"], "image" : users[id]["image"]})
        i += 1
        if i == NUM_IN_ROW:
            i = 0
            show_users.append(user_row)
            user_row = []
    if user_row:
        show_users.append(user_row)

    return render_template("users.html", users=show_users, num_in_rows=NUM_IN_ROW,
        num_users=num_users, num_stamps=num_stamps)


@app_mod.route('/user_image/<filename>')
def user_image(filename):
    return send_from_directory(current_app.config["USER_IMAGES_DIR"], filename)


@app_mod.route('/user/<int:userid>')
def user_detail(userid):
    user_details = Users.query.get(userid)
    if user_details:
        num_users = Users.query.count()
        num_stamps = Stamps.query.count()

        stamps_dict = {}
        used_stamps = [sObj.id for sObj in user_details.used_stamps]
        for category in StampCategories.query.all():
            i = 0
            stamp_row = []
            stamps = []
            for stamp in category.stamps:
                if stamp.id in used_stamps:
                    continue
                stamp_row.append({"id" : stamp.id, "name" : stamp.name, "image" : stamp.image_id})
                i += 1
                if i == NUM_IN_ROW:
                    i = 0
                    stamps.append(stamp_row)
                    stamp_row = []
            if stamp_row:
                stamps.append(stamp_row)
            if stamps:
                stamps_dict[category.name] = stamps

        return render_template("user_detail.html", stamps=stamps_dict, num_in_rows=NUM_IN_ROW,
            num_users=num_users, num_stamps=num_stamps,
            user_info={"id" : user_details.id, "name" : user_details.name, "image_id" : user_details.image_id})

    return redirect(url_for('slowly-module.list_users'))


@app_mod.route('/add_user', methods=['GET', 'POST'])
def add_new_user():
    if request.method == 'POST':
        penPalName = request.form['penPalName'].strip()
        penPalImage = request.files.get('penPalImage', None)
        new_file_name = None
        if penPalImage and penPalImage.filename != '':
            while True:
                new_file_name = ''.join((random.choice(string.ascii_letters + string.digits) for i in range(10)))
                if new_file_name not in os.listdir(current_app.config["USER_IMAGES_DIR"]):
                    break
            penPalImage.save(os.path.join(current_app.config["USER_IMAGES_DIR"], new_file_name))

        if new_file_name:
            user_obj = Users(name=penPalName, image_id=new_file_name)
        else:
            user_obj = Users(name=penPalName)

        db.session.add(user_obj)
        db.session.commit()

        return redirect(url_for('slowly-module.list_users'))
    else:
        num_users = Users.query.count()
        num_stamps = Stamps.query.count()
        return render_template("add_user.html", num_users=num_users, num_stamps=num_stamps)


@app_mod.route('/edit/<int:userid>', methods=['GET', 'POST'])
def edit_existing_user(userid):
    user_obj = Users.query.get(userid)
    if not user_obj:
        return redirect(url_for('slowly-module.list_users'))

    if request.method == 'POST':
        prev_name, prev_image_id = user_obj.name, user_obj.image_id

        penPalName = request.form['penPalName'].strip()
        if penPalName != prev_name:
            user_obj.name = penPalName

        penPalImage = request.files.get('penPalImage', None)
        new_file_name = None
        if penPalImage and penPalImage.filename != '':
            while True:
                new_file_name = ''.join((random.choice(string.ascii_letters + string.digits) for i in range(10)))
                if new_file_name not in os.listdir(current_app.config["USER_IMAGES_DIR"]):
                    break
            penPalImage.save(os.path.join(current_app.config["USER_IMAGES_DIR"], new_file_name))
            if prev_image_id:
                os.remove(os.path.join(current_app.config["USER_IMAGES_DIR"], prev_image_id))
            user_obj.image_id = new_file_name

        db.session.commit()
        return redirect(url_for('slowly-module.list_users'))
    else:
        num_users = Users.query.count()
        num_stamps = Stamps.query.count()
        conn.execute(f"select name, image_id from users where id is {userid}")
        return render_template("edit_user.html", num_users=num_users, num_stamps=num_stamps,
            user_id=userid, user_name=user_obj.name, user_image_id=user_obj.image_id)


@app_mod.route('/delete/<int:userid>')
def delete_user(userid):
    uObj = Users.query.get(userid)
    if uObj:
        db.session.delete(uObj)
        db.session.commit()
    return redirect(url_for('slowly-module.list_users'))


@app_mod.route('/stamp_image/<filename>')
def stamp_image(filename):
    return send_from_directory(current_app.config["STAMP_IMAGES_DIR"], filename)


@app_mod.route('/stamps')
def list_stamps():
    num_users = Users.query.count()
    num_stamps = Stamps.query.count()

    stamps_dict = {}
    for category in StampCategories.query.all():
        i = 0
        stamp_row = []
        stamps = []
        for stamp in category.stamps:
            stamp_row.append({"id" : stamp.id, "name" : stamp.name, "image" : stamp.image_id})
            i += 1
            if i == NUM_IN_ROW:
                i = 0
                stamps.append(stamp_row)
                stamp_row = []
        if stamp_row:
            stamps.append(stamp_row)
        stamps_dict[category.name] = stamps

    return render_template("stamps.html", stamps=stamps_dict, num_in_rows=NUM_IN_ROW,
        num_users=num_users, num_stamps=num_stamps)


@app_mod.route('/add_stamp', methods=['GET', 'POST'])
def add_new_stamp():
    if request.method == 'POST':
        chosen_category = request.form.getlist('category-radio')
        category_Obj = None
        if chosen_category:
            chosen_category = chosen_category[0]
            if chosen_category == "newCategory":
                if request.form['newCategoryName']:
                    newCategoryName = request.form['newCategoryName'].strip()
                    category_Obj = StampCategories(name=newCategoryName)
                    db.session.add(category_Obj)
            else:
                category_Obj = StampCategories.query.get(chosen_category)

            if category_Obj:
                stampName = request.form['inputStampName'].strip()
                stampImage = request.files.get('stampImage', None)
                new_file_name = None
                if stampImage and stampImage.filename != '':
                    while True:
                        new_file_name = ''.join((random.choice(string.ascii_letters + string.digits) for i in range(10)))
                        if new_file_name not in os.listdir(current_app.config["STAMP_IMAGES_DIR"]):
                            break
                    stampImage.save(os.path.join(current_app.config["STAMP_IMAGES_DIR"], new_file_name))

                if new_file_name:
                    new_stamp = Stamps(name=stampName, category=category_Obj, image_id=new_file_name)
                else:
                    new_stamp = Stamps(name=stampName, category=category_Obj)
                db.session.add(new_stamp)

            db.session.commit()

        return redirect(url_for('slowly-module.list_stamps'))

    num_users = Users.query.count()
    num_stamps = Stamps.query.count()
    all_categories = [{"cid" : category.id, "cname" : category.name} for category in StampCategories.query.all()]

    return render_template("add_stamp.html", num_users=num_users,
        num_stamps=num_stamps, all_categories=all_categories)


@app_mod.route('/use/<use_info>')
def save_used_stamps(use_info):
    info_parts = use_info.split("-")
    if len(info_parts) == 2:
        user_id, stamp_id = info_parts
        user_obj = Users.query.get(user_id)
        stamp_obj = Stamps.query.get(stamp_id)
        if user_obj and stamp_obj:
            user_obj.used_stamps.append(stamp_obj)
            db.session.add(user_obj)
            db.session.commit()
    return redirect(url_for('slowly-module.list_users'))
