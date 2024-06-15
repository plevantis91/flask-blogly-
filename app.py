from flask import Flask, render_template, redirect, request, url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'hushhushhush'

app.debug = True 

debug = DebugToolbarExtension(app)

connect_db(app)

with app.app_context():
    db.create_all()  # Create tables if they don't exist
    print('Tables created')


@app.route('/')
def home():
    # Displays a page with the list of users
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users.html', users=users)


@app.route('/form', methods = ["GET","POST"])
def create_user():
    # Display page with the form to create a new user
    if request.method == 'POST':
        new_user = User(
            first_name=request.form.get('first_name'),
            last_name=request.form.get('last_name'),
            image_url=request.form.get('image_url' or None)
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        return redirect('/')
    
    return render_template('form.html')
        

@app.route('/users/<int:user_id>', methods=['GET','POST'])
def user_detail(user_id):
    #  Displays page with info of a specified users
     if request.method == 'GET':
         user = User.query.get_or_404(user_id)
         return render_template('detail.html', user=user)
     elif request.method == 'POST':
        user = User.query.get_or_404(user_id)
        user.first_name = request.form.get('first_name')
        user.last_name = request.form.get('last_name')
        user.image_url = request.form.get('image_url')

     db.session.add(user)
     db.session.commit()
 
     return redirect("/users")

@app.route('/users/<int:user_id>/edit', methods = ['GET', 'POST'])
def edit_user(user_id):
    if request.method == 'GET':
        user = User.query.get_or_404(user_id)
        return render_template('edit.html', user=user)
    elif request.method == 'POST':
        user = User.query.get_or_404(user_id)
        user.first_name = request.form.get('first_name')
        user.last_name = request.form.get('last_name')
        user.image_url = request.form.get('image_url')

    db.session.add(user)
    db.session.commit()

    return redirect('/')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    # Deletes specified user
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/')


if __name__ == '__main__':
   
    app.run(debug=True)