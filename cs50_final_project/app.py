from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.utils import secure_filename
from validate_email import validate_email
from waitress import serve
import datetime
import random
import socket
import cs50
import os

db = cs50.SQL("sqlite:///users.db")
ip = socket.gethostbyname(socket.gethostname())

app = Flask(__name__)
app.config['SECRET_KEY'] = '*07ooQd!1sOa875yj4GR3ty4yyd&g16x'
app.config["UPLOAD_FOLDER"] = "C:/Users/msi/Desktop/cs50_final_project/static/uploadings"


def get_current_post(id):
    return db.execute("SELECT * FROM posts WHERE post_id = ?", id)[0]


@app.route("/")
def main():
    # session.clear()
    if session.get("user_id") != None:
        posts = db.execute("SELECT * FROM posts")
        users = db.execute("SELECT * FROM user WHERE id IN (SELECT user_id FROM posts)")

        ids = set(i["user_id"] for i in posts)
        names = [i["username"] for i in users]
        imgs = [i["img_filename"] for i in users]

        for id, name, img in zip(ids, names, imgs):
            for i in posts:
                if id == i["user_id"]:
                    i["name"] = name
                    i["img_filename"] = img


        return render_template("home.html", posts = posts)
    
    return render_template("login.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if email == "" or password == "":
            return render_template("login.html", error_message="Invalid name or password")
        
        if not validate_email(email):
            return render_template("login.html", error_message="Please enter a valid email")


        other_email = db.execute("SELECT COUNT(email) AS user_count, username, id FROM user WHERE email = ? AND password = ?", email, password)

        if other_email[0]["user_count"] == 1:
            session["user_id"] = other_email[0]["id"]
            session["username"] = other_email[0]["username"]
            return redirect("/")
        
        else:
            return render_template("login.html", error_message = "Account not found")
        
    else:
        return render_template("login.html")


@app.route("/sign_up", methods=["POST", "GET"])
def sign_up():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        now = datetime.datetime.now()
        account_date = f"{now.year}-{now.month}-{now.day} {now.hour}:{now.minute}:{now.second}"

        if name == "" or password == "" or email == "":
            return render_template("sign_up.html", error_message="Please fill the blanks")
        
        if len(name) > 8:
            return render_template("sign_up.html", error_message="Max name length is 8")
        
        if len(name) < 2:
            return render_template("sign_up.html", error_message="Minimum name length is 3")
        
        if not validate_email(email):
            return render_template("sign_up.html", error_message="Invalid email")
        
        
        email_count = db.execute("SELECT COUNT(email) AS email_count FROM user WHERE email = ?", email)[0]["email_count"]
        username_count = db.execute("SELECT COUNT(username) AS username_count FROM user WHERE username = ?", name)[0]["username_count"]

        if email_count == 0 and username_count == 0:
            db.execute("INSERT INTO user (username, password, email, account_date) VALUES (?, ?, ?, ?)", name, password, email, account_date)
            id = db.execute("SELECT id FROM user WHERE username = ?", name)
            session["user_id"] = id[0]["id"]
            session["username"] = name
            return redirect("/")
        
        else:
            return render_template("sign_up.html", error_message = "This name is already exists")
    
    else:
        return render_template("sign_up.html")


@app.route("/logout")
def log_out():
    if session.get("user_id") != None:
        db.execute("DELETE FROM comments WHERE user_id = ?", session["user_id"])
        db.execute("DELETE FROM posts WHERE user_id = ?", session["user_id"])
        db.execute("DELETE FROM user WHERE id = ?", session["user_id"])

        session["username"] = None
        session["user_id"] = None
        session["post_id"] = None

    return redirect("/")

# @app.route("/home")
# def home():
#     return redirect("/")


@app.route("/render_post")
def render_post():
    if session.get("user_id") != None:
        return render_template("post.html")
    else:
        return redirect("/")

@app.route("/post", methods=["POST"])
def post():
    text = request.form.get("text")
    file = request.files["file"]
    if file:
        filename = secure_filename(file.filename)
        files = os.listdir(app.config["UPLOAD_FOLDER"])


        if filename in files:
            index = filename.index(".")
            file_format = filename[index::]
            filename_with_no_format = filename[:index:]

            filename = f"{filename_with_no_format}({len(files) + 1}){file_format}"

        file.save(os.path.join(app.root_path, app.config["UPLOAD_FOLDER"], filename))        
        
        db.execute("INSERT INTO posts (user_id, filename, legend) VALUES (?, ?, ?)", session["user_id"], filename, text)
        post_id = db.execute("SELECT post_id FROM posts WHERE user_id = ?", session["user_id"])

        session["post_id"] = post_id[0]["post_id"]

        return redirect("/")
    else:
        return render_template("post.html", error_message="Please enter a file")
        
@app.route("/like/<string:post_id>")
def like_post(post_id):
    curr_likes = get_current_post(post_id)["likes"]
    db.execute("UPDATE posts SET likes = ? WHERE post_id = ?", int(curr_likes) + 1, post_id)
    return redirect("/")

@app.route("/dislike/<string:post_id>")
def dislike_post(post_id):
    curr_dislikes = get_current_post(post_id)["dislikes"]
    db.execute("UPDATE posts SET dislikes = ? WHERE post_id = ?", int(curr_dislikes) + 1, post_id)
    return redirect("/")

@app.route("/render_comment/<string:post_id>")
def render_comment(post_id):
    session["post_id"] = post_id

    post_comments = db.execute("SELECT * FROM comments WHERE post_id = ?", post_id)
    users = db.execute("SELECT * FROM user WHERE id IN (SELECT user_id FROM comments WHERE post_id = ?)", post_id)
    
    ids = set(i["user_id"] for i in post_comments)
    names = [i["username"] for i in users]
    imgs = [i["img_filename"] for i in users]

    for id, name, img in zip(ids, names, imgs):
        for i in post_comments:
            if id == i["user_id"]:
                i["name"] = name
                i["img_filename"] = img


    return render_template("comments.html", comments = post_comments)

        
@app.route("/post_comment", methods=["POST"])
def post_comment():
    text = request.form.get("content")
    db.execute("INSERT INTO comments (content, user_id, post_id) VALUES (?, ?, ?)", text, session["user_id"], session["post_id"])

    comment_number = db.execute("SELECT comment_number FROM posts WHERE post_id = ?", session["post_id"])[0]["comment_number"]
    db.execute("UPDATE posts SET comment_number = ? WHERE post_id = ?", comment_number + 1, session["post_id"])

    return redirect(f"/render_comment/{session['post_id']}")



@app.route("/like_comment/<string:comment_id>")
def like_comment(comment_id):
    curr_likes = db.execute("SELECT likes FROM comments WHERE comment_id = ?", comment_id)[0]["likes"]

    db.execute("UPDATE comments SET likes = ? WHERE comment_id = ?", int(curr_likes) + 1, comment_id)
    return redirect(f"/render_comment/{session['post_id']}")

@app.route("/dislike_comment/<string:comment_id>")
def dislike_comment(comment_id):
    curr_likes = db.execute("SELECT dislikes FROM comments WHERE comment_id = ?", comment_id)[0]["dislikes"]
    db.execute("UPDATE comments SET dislikes = ? WHERE comment_id = ?", int(curr_likes) + 1, comment_id)
    return redirect(f"/render_comment/{session['post_id']}")

@app.route("/share")
def share():
    return redirect("/")


@app.route("/profile")
def profile():
    user = db.execute("SELECT * FROM user WHERE id = ?", session["user_id"])
    data = db.execute("SELECT SUM(likes) AS likes_sum, SUM(dislikes) AS dislikes_sum, COUNT(post_id) AS posts_count, SUM(comment_number) AS comment_sum FROM posts WHERE user_id = ?", session["user_id"])[0]
    return render_template("profile.html", user=user, likes_sum=data["likes_sum"], dislikes_sum=data["dislikes_sum"], posts_count=data["posts_count"], comment_sum=data["comment_sum"])

@app.route("/follow/<string:user_id>")
def follow(user_id):
    followers = db.execute("SELECT followers FROM user WHERE id = ?", user_id)[0]["followers"]
    db.execute("UPDATE user SET followers = ? WHERE id = ?", followers + 1, user_id)

    return redirect("/")

@app.route("/render_change_profile")
def render_change_profile():
    return render_template("change_picture.html", id=session["user_id"])

@app.route("/change_profile", methods=["POST"])
def change_profile():
    file = request.files["file"]
    if file:
        filename = secure_filename(file.filename)
        files = os.listdir(app.config["UPLOAD_FOLDER"])


        if filename in files:
            index = filename.index(".")
            file_format = filename[index::]
            filename_with_no_format = filename[:index:]

            filename = f"{filename_with_no_format}({len(files) + 1}){file_format}"

        file.save(os.path.join(app.root_path, app.config["UPLOAD_FOLDER"], filename))        
        
        db.execute("UPDATE user SET img_filename = ? WHERE id = ?", filename, session["user_id"])

        return redirect("/")
    else:
        return render_template("post.html", error_message="Please enter a file")


@app.route("/show_person_profile/<string:user_id>")
def show_person_profile(user_id):
    user = db.execute("SELECT * FROM user WHERE id = ?", user_id)
    data = db.execute("SELECT SUM(likes) AS likes_sum, SUM(dislikes) AS dislikes_sum, COUNT(post_id) AS posts_count, SUM(comment_number) AS comment_sum FROM posts WHERE user_id = ?", user_id)[0]
    return render_template("profile.html", user=user, likes_sum=data["likes_sum"], dislikes_sum=data["dislikes_sum"], posts_count=data["posts_count"], comment_sum=data["comment_sum"])    



if __name__ == "__main__":
    app.debug = True
    # serve(app, host=ip, port=9999)
    app.run()


# start with the backend and add the store image file name