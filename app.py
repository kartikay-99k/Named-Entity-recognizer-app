# import working libraries
import streamlit as st 
import pandas as pd 
import spacy

# Utils
import base64
import tempfile
from pathlib import Path

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



def csv_downloader(data):
    csvfile = data.to_csv(index=False)
    b64 = base64.b64encode(csvfile.encode()).decode()
    new_filename = "result.csv"
    st.markdown("#### Download File ###")
    href = f'<a href="data:file/csv;base64,{b64}" download="{new_filename}">Click Here!!</a>'
    st.markdown(href,unsafe_allow_html=True)
    
# list for storing results
entity = []
txt = []    
    
    
def main():
    
    """Main Function Body """
    activities = ["Image","PDF"]
    choice = st.sidebar.selectbox("Select Activities",activities)
    if choice == 'Image':
        image_file = st.file_uploader("Upload Image", type=["png","jpg","jpeg"])
        if image_file is not None:
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                df = pd.DataFrame()
                fp = Path(tmp_file.name)
                fp.write_bytes(image_file.getvalue())
                text = convert_image_to_text(tmp_file.name)
                nlp = spacy.load("./model/")
                doc = nlp(text)
                for ent in doc.ents:
                    entity.append(ent.label_)
                    txt.append(ent.text)
                df["Entity_type"]=pd.Series(entity)
                df["Entity_extracted"]=pd.Series(txt)
                csv_downloader(df)        


       
    if choice == 'PDF':
        pdf_file = st.file_uploader("Upload Pdf", type="pdf")
        if pdf_file is not None:
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                df = pd.DataFrame()
                fp = Path(tmp_file.name)
                fp.write_bytes(pdf_file.getvalue())
                text = get_text_from_any_pdf(tmp_file.name)
                nlp = spacy.load("./model/")
                doc = nlp(text)
                for ent in doc.ents:
                    entity.append(ent.label_)
                    txt.append(ent.text)
                df["Entity_type"]=pd.Series(entity)
                df["Entity_extracted"]=pd.Series(txt)
                csv_downloader(df)     
    
                            

                
                
if __name__ == '__main__':
	main()
