from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dom_web_site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Dom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    info = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Dom %r>' %self.name

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/posts')
def posts():
    dom = Dom.query.order_by(Dom.date.desc()).all()
    return render_template('posts.html', dom=dom)

@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def posts_update(id):
    dom = Dom.query.get(id)
    if request.method == 'POST':
        dom.name = request.form['name']
        dom.info = request.form['info']
        dom.description = request.form['description']

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return 'An error has occurred. Check the correctness of the entered data.'
    else:
        dom = Dom.query.get(id)
        return render_template("posts_update.html", dom=dom)

@app.route('/posts/<int:id>')
def posts_detail(id):
    dom = Dom.query.get(id)
    return render_template('posts_detail.html', dom=dom)

@app.route('/posts/<int:id>/del')
def posts_delete(id):
    dom = Dom.query.get.get_or_404(id)

    try:
        db.session.delete(dom)
        db.session.commit()
        return redirect('/posts')

    except:
        return 'An error occurred while deleting.'

@app.route('/create-dom', methods=['POST', 'GET'])
def create_dom():
    if request.method == 'POST':
        name = request.form['name']
        info = request.form['info']
        description = request.form['description']

        dom = Dom(name=name, info=info, description=description)

        try:
            db.session.add(dom)
            db.session.commit()
            return redirect('/posts')
        except:
            return 'An error has occurred. Check the correctness of the entered data.'
    else:
        return render_template("create_dom.html")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)