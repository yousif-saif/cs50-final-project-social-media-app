
Social media app
#### Video Demo:  https://www.youtube.com/watch?v=oz4SxLQMUt4
#### Description:
This is social media app by yousif saif,
In this project i build a social media app were you can login, sign up, post, comment, like, dislike, share a post, logout and a profile section to display the user data,
I used python, python flask framework as the server-side, css, css bootstrap framework, SQLITE3 for the databases, litile javascript to make the share function and html

Here is an explanation for the app:
# templates:

## layout.html:
Is the root for all the project's templates.

## login.html:
Here where you can login to you'r account by entering your password and email.
Here is a preview of the template:

![Screenshot (41)](https://user-images.githubusercontent.com/109082486/231876751-55cbaf16-eaa2-47f2-9c39-58d74295c861.png)

In the email input you type the email for your account.
and the password input you type the password for youe account.


## sign_up.html:
Here where you can sign up (create new account) by entering your name, password and email.
Here is a preview of the template:

![Screenshot (42)](https://user-images.githubusercontent.com/109082486/231877373-f5a8f436-f30c-42b6-a8ad-142178ce5a43.png)

Here you sign_up (create a new account) by typing your name, email, password

## home.html:
Here is the main page were you can see people's posts.

### Like:
You can like the post. Here is a preview for the like button:

![Screenshot (43)](https://user-images.githubusercontent.com/109082486/231878716-7e310d48-ca4a-4144-bd4a-4cffad44f033.png)


### Dislike:
You can dislike the post. Here is a preview for the dislike button:

![Screenshot (43)](https://user-images.githubusercontent.com/109082486/231879907-61695ef9-42da-4987-a138-68e9bf5f7bbb.png)


### Comment:
You can comment on peoples post and you can also like the comments and dislike them.
Here is a preview of the comment button:


![Screenshot (43)](https://user-images.githubusercontent.com/109082486/231880388-8512c95f-4aa1-407a-8470-3a112ade8a5e.png)


### Share:
You can share the website on whatsapp. Here is a preview of the comment button:

![Screenshot (43)](https://user-images.githubusercontent.com/109082486/231881787-db566f9c-598f-4ae5-9e09-57bdd94e6471.png)

## Comments.html:
Here where you can comment for people posts.

## Post.html:
Here where you can post a post by choosing an image and type something you whant.
Here is a preview of the template:

![Screenshot (46)](https://user-images.githubusercontent.com/109082486/231875860-c4bb1745-8ace-49eb-84bd-1d772861e2c7.png)

In the "Write something..." input you type the text that you want to include with the image.

The "choose File" is the button to uplaod an image with the text (if entered).

## profile.html:
Here where you can see all of your profile data and others (by pressing on thier profile image) like the total amount of thier posts, the date they create the account, total likes, total dislikes, total comments, thier name, email, profile picture.

Here is a preview of the template:

![Screenshot (45)](https://user-images.githubusercontent.com/109082486/231883333-4b2ac126-3d45-442c-a44f-ad15e660a784.png)


## change_picture.html:
Here where you can change your profile picture by choosing an image.
Here is a preview of the template:

![Screenshot (47)](https://user-images.githubusercontent.com/109082486/231882971-41526d3f-02b6-4f36-9df5-0e3b9ab6a8c7.png)

By pressing on the "choose file" button you can choose an image for your profile image.

# folders:

## static:
Here is all the website data excepte of the style.css wich is a css file that adds a a style to the template.

## uploadings:
Here is all the posts images and people's profile images

## templates:
Here is all the html files for the website.

# app.py:
Is the server-side for the flask app that runs the website.
