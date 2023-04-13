
# posts = [{'user_id': 2, 'post_id': 1, 'likes': 9, 'dislikes': 11, 'comment_number': 1, 'shares': 0, 'filename': 'IMG-20230331-WA0004.jpg', 'legend': 'From phone'}, 
#         {'user_id': 1, 'post_id': 2, 'likes': 10, 'dislikes': 3, 'comment_number': 4, 'shares': 0, 'filename': 'python_image.jpg', 'legend': 'From laptop'}, 
#         {'user_id': 1, 'post_id': 3, 'likes': 4, 'dislikes': 0, 'comment_number': 0, 'shares': 0, 'filename': 'mars-planet-view-4k-rn2.jpg', 'legend': 'Finallllyyyyy'}]

# users = [{'id': 1, 'username': 'yousif', 'password': '123', 'email': 'a@a', 'followers': 5, 'account_date': '2023-4-6 17:14:12', 'img_filename': 'mars-planet-view-4k-rn2(5).jpg'},
#         {'id': 2, 'username': 'yousif3', 'password': '123', 'email': 'a@a2', 'followers': 0, 'account_date': '2023-4-6 17:14:43', 'img_filename': 'person.jpg'}]

# ids = set(i["user_id"] for i in posts)
# names = [i["username"] for i in users]
# imgs = [i["img_filename"] for i in users]

# for id, name, img in zip(ids, names, imgs):
#     for i in posts:
#         if id == i["user_id"]:
#             i["name"] = name
#             i["img_filename"] = img


def c(s):
    return s + round(s/3) - round(s/4)

i = 0
e = c(9)
while e != 18:
    i += 1
    e = c(e)

print(i)