from website import app, db
with app.app_context():
    db.drop_all()
print('Deleted database! ')