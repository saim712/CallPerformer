from flask import Flask,render_template,redirect,request
import cv2
from cv2 import imshow, waitKey
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class Todo(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200),nullable=False)
    password=db.Column(db.String(500),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.name}"


# @app.route("/")
# def create_database():
#     with app.app_context():
#         db.create_all()
#     return "Database schema created successfully!"






@app.route('/',methods=['POST','GET'])
def hello_world():
    if request.method=='POST':
        print('post')
        title=request.form['title']
        desc=request.form['desc']

        todo=Todo(title=title,desc="desc")
        db.session.add(todo)
        db.session.commit()
    alltodo=Todo.query.all()
    # print(alltodo)
    return render_template('login.html',alltodo=alltodo)
    # return render_template('gpt.html')
    # return 'Hello, World i am coming by the will of creator of multiverses'







@app.route('/gpt',methods=['POST','GET'])
# @app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print('post')
        title = 'my name'
        desc = 'my password'

        # Create a new Todo instance with the provided title and desc
        todo = Todo(name=title, password=desc)

        # Add the new Todo instance to the database
        db.session.add(todo)

        # Commit the changes to the database
        db.session.commit()

    # Retrieve all todos from the database
    alltodo = Todo.query.all()

    # Render the template with the retrieved todos
    return render_template('gpt.html', alltodo=alltodo)


@app.route('/login',methods=['POST','GET'])
def page():
    return render_template('login.html')

@app.route('/analyze_emotion', methods=['POST'])
def analyze_emotion():
    if 'image' not in request.files:
        return 'No file part'

    image = request.files['image']
    

    if image.filename == '':
        return 'No selected file'

   

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')

    # Read the input image

    app_root = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the image inside the static folder
    image_path = os.path.join(app_root, 'static', 'image', 'istockphoto-1352096257-1024x1024.jpg')
    img = cv2.imread(image_path)
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(imgGray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Iterate over detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Get the region of interest (ROI) for eyes and smile within the detected face
        roi_gray = imgGray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]

        # Detect eyes within the face region
        eyes = eye_cascade.detectMultiScale(roi_gray)

        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 0, 255), 2)

        # Detect smiles within the face region
        smiles = smile_cascade.detectMultiScale(roi_gray, scaleFactor=1.8, minNeighbors=20)

        # Iterate over detected smiles
        for (sx, sy, sw, sh) in smiles:
            cv2.rectangle(roi_color, (sx, sy), (sx+sw, sy+sh), (255, 0, 0), 2)

    # Display the result
    imshow("output", img)
    waitKey(0)
    cv2.destroyAllWindows()

    
    # return f'Emotion Analysis Result: {emotion_result}'

    return render_template('gpt.html')

if __name__ == '__main__':
    app.run(debug=True)


