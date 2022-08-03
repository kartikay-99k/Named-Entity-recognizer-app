# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer


# import working libraries
import streamlit as st 
import pandas as pd 
import spacy

# Utils
import os
# =============================================================================
# import base64
# import tempfile
# from pathlib import Path
# =============================================================================

# text extraction utils
from pdf2image import convert_from_path
from pytesseract import image_to_string


def convert_pdf_to_img(pdf_file):
    return convert_from_path(pdf_file)


def convert_image_to_text(file):
    text = image_to_string(file)
    return text



def get_text_from_any_pdf(pdf_file):
    images = convert_pdf_to_img(pdf_file)
    final_text = ""
    for pg, img in enumerate(images):
        
        final_text += convert_image_to_text(img)
        #print("Page n°{}".format(pg))
        #print(convert_image_to_text(img))
    
    return final_text


#################################################

# Define a flask app
Flask_app = Flask(__name__)

MODEL_PATH = 'C:/Users/kartikay.gupta/Flask_dir/model/'
nlp_model = spacy.load(MODEL_PATH)


def model_predict(file_path, model):
    entity = []
    txt = []
    df = pd.DataFrame()
    img_ext = [".jpg" , ".jpeg" , ".png"]
    for ext in img_ext:
        if file_path.endswith(ext):
            text = convert_image_to_text(file_path)
            doc = model(text)
            for ent in doc.ents:
                entity.append(ent.label_)
                txt.append(ent.text)
            df["Entity_type"]=pd.Series(entity)
            df["Entity_extracted"]=pd.Series(txt)
            break
        
    
            
        
    if file_path.endswith(".pdf" ):
        text = get_text_from_any_pdf(file_path)
        doc = model(text)
        for ent in doc.ents:
            entity.append(ent.label_)
            txt.append(ent.text)
        df["Entity_type"]=pd.Series(entity)
        df["Entity_extracted"]=pd.Series(txt)
    
    return df    
        

Flask_app.config["UPLOAD_FOLDER"] = "C:/Users/kartikay.gupta/Flask_dir/uploads/"
    
@Flask_app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')
    

@Flask_app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)

        f.save(Flask_app.config['UPLOAD_FOLDER'] + filename)

        file_path = Flask_app.config['UPLOAD_FOLDER'] + filename 

        # Make prediction
        df_result = model_predict(file_path, nlp_model)
        return render_template("result.html",tables=[df_result.to_html()])
        

        #return result
    return None


#################################################


if __name__ == '__main__':
    Flask_app.run(debug=True)



