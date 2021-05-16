from flask import Flask, request, jsonify, render_template, url_for
import os
from main import process 

app= Flask(__name__)
app.config["UPLOAD_PATH"]="data/"

showFolder = os.path.join('static')
print(showFolder)
app.config['SHOW_FOLDER'] = showFolder

@app.route('/',methods=["GET","POST"])
def upload_file():
    if request.method =="POST":
        directory =r"D:\PascalVOC-to-Images"
        os.chdir(directory)
        for f in request.files.getlist('file_name'):
            # f= request.files['file_name']
            f.save(os.path.join(app.config['UPLOAD_PATH'],f.filename))
            file_name, file_extension = os.path.splitext(f.filename)
            print(file_extension)
            if file_extension == ".xml":
                filePath=process(file_name)
                print(filePath)
                path = os.getcwd()
                # print(os.path.dirname(path)+'\data'+path)
                pic1 = os.path.join(app.config['SHOW_FOLDER'], 'savedImage.jpg')
                print(pic1)
        return render_template("index.html", user_image=pic1)  
    return render_template("index.html",msg="please choose the file")


if __name__ =='__main__':
    app.run(debug=True)