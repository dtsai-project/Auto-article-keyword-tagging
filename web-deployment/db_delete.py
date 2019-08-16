from application import Post, db

post = Post.query.all()
for i in post:
    db.session.delete(i)
    db.session.commit()
print("sukses")
