from flask import  Flask,jsonify, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests
import os
from openai import OpenAI

from sqlalchemy import desc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///biscuit.db'
db = SQLAlchemy(app)

client = OpenAI(
    api_key="PASTE_YOUR_KEY_HERE"
)



class Biskit(db.Model):
     sno = db.Column(db.Integer,primary_key=True)
     title =  db.Column(db.String(200))
     desc =  db.Column(db.String(500))
     image = db.Column(db.String(300))
     date_created = db.Column(db.DateTime, default=datetime.utcnow)

     def __repr__(self) -> str:
          return f"{self.sno} - {self.title}"





@app.route('/' ,methods=['GET','POST'])
def my_world():
    if request.method == 'POST':
          title = request.form['title']
          desc = request.form['desc']

          
          safe_title = title.replace(" ", "_")

          prompt = f"Professional food photography of {title}, {desc}"

          image_path = generate_recipe_image(prompt, safe_title)

          biscuit = Biskit(
               title=title,
               desc=desc,
               image=image_path
          )
          
          db.session.add(biscuit)
          db.session.commit()
    allbiskit = Biskit.query.all()
    return render_template('index.html',allbiskit=allbiskit)

def sea_world():
     if request.method == 'POST':
          sea = request.form['sea']
          search = Biskit.query.filter_by(sno=sea).first()
     cokie_update = Biskit.query.filter_by(sno=sea).first()
     return render_template('update.html',cokie_update=cokie_update)
          
          

@app.route('/about')
def about_us():
     return render_template('about.html')
     

@app.route('/update/<int:sno>',methods=['GET','POST'])
def update(sno):
     if request.method == 'POST':
          title = request.form['title']
          desc = request.form['desc']
          cokie_update = Biskit.query.filter_by(sno=sno).first()
          cokie_update.title = title
          cokie_update.desc = desc
          db.session.add(cokie_update)
          db.session.commit()
          return redirect("/")

     cokie_update = Biskit.query.filter_by(sno=sno).first()
     return render_template('update.html',cokie_update=cokie_update)

@app.route('/delete/<int:sno>')
def delete(sno):
     cokie = Biskit.query.filter_by(sno=sno).first()
     db.session.delete(cokie)
     db.session.commit()
     return redirect("/")

@app.route('/display',methods=['GET','POST'])
def display():
    if request.method == 'POST':
          sea = request.form['sea']
          cokie_display = Biskit.query.filter_by(sno=sea).first()
          
    return render_template("display.html",cokie_display=cokie_display)

def generate_recipe_image(prompt, filename):

     import urllib.parse

     encoded_prompt = urllib.parse.quote(prompt)

     image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"

     response = requests.get(image_url)

     os.makedirs("static/generated", exist_ok=True)

     image_path = f"static/generated/{filename}.jpg"

     with open(image_path, "wb") as f:
          f.write(response.content)

     return image_path

if __name__ == "__main__":

     with app.app_context():
          db.create_all()

     app.run(debug=True,port=8000)