# Throwaway script used to transfer data once upon a time
import os
import shutil
import sqlite3


if __name__ == "__main__":
    source_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "old_resources"))
    target_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "resources"))

    db_source = sqlite3.connect(os.path.join(source_dir, "data.db"))
    db_target = sqlite3.connect(os.path.join(target_dir, "data.db"))

    cur_source = db_source.cursor()
    cur_target = db_target.cursor()

    cur_source.execute("select id, name, image_id from users")
    for row in cur_source:
        id, name, image_id = row
        name = name.replace("'", "''")
        cur_target.execute(f"insert into users (id, name, image_id) values ({id}, '{name}', '{image_id}')")
        if image_id:
            if os.path.exists(os.path.join(source_dir, "users", image_id)):
                shutil.copy(os.path.join(source_dir, "users", image_id), os.path.join(target_dir, "users", image_id))

    cur_source.execute("select id, name from stamp_categories")
    for row in cur_source:
        id, name = row
        name = name.replace("'", "''")
        cur_target.execute(f"insert into stamp_categories (id, name) values({id}, '{name}')")

    cur_source.execute("select id, name, category_id, image_id from stamps")
    for row in cur_source:
        id, name, category_id, image_id = row
        name = name.replace("'", "''")
        cur_target.execute(f"insert into stamps (id, name, category_id, image_id) values ({id}, '{name}', {category_id}, '{image_id}')")
        if image_id:
            if os.path.exists(os.path.join(source_dir, "stamps", image_id)):
                shutil.copy(os.path.join(source_dir, "stamps", image_id), os.path.join(target_dir, "stamps", image_id))

    cur_source.execute("select user_id, stamp_id from used_stamps")
    for row in cur_source:
        user_id, stamp_id = row
        cur_target.execute(f"insert into used_stamps (user_id, stamp_id) values ({user_id}, {stamp_id})")

    db_target.commit()

    db_source.close()
    db_target.close()
