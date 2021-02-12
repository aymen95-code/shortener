import random, string
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = '6f4f33f6fb14823923f55fc73c8a3eaa'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Urls(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(60), unique=True, nullable=False)
    shortened = db.Column(db.String(5), unique=True, nullable=False)

    def repr(self):
        return f'<{self.url} => {self.shortened}>'

def generate_token(url:str, y:int) -> str:
    duplicate:bool = False
    while True:
        random_token:str = ''.join(random.choice(string.ascii_letters) for x in range(y))
        for existing_url in Urls.query.all():
            if random_token == existing_url:
                duplicate = True
                break # break for loop
        if duplicate:
            continue # continue while loop
        else:
            return random_token
        

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        shortened_url = generate_token(request.form["url"], 5)
        print(shortened_url)
        url = Urls(url=request.form["url"], shortened=shortened_url)
        db.session.add(url)
        db.session.commit()
        return redirect(url_for('all'))
    return render_template('index.html')

@app.route('/all')
def all():
    list_of_urls = Urls.query.all()
    return render_template('all.html', urls=list_of_urls)

@app.route('/<string:shortened_url>')
def pathUrl(shortened_url):
    url = Urls.query.filter_by(shortened=shortened_url).first().url
    if 'https://' in url:
        return redirect(url)
    else:
        url = 'https://' + url
        return redirect(url)
    

if __name__ == "__main__":
    app.run(debug=True)
