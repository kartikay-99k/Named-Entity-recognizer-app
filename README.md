# FLask app for Named-Entity-recognition

## **About**
### Simple app for extracting entities like (Name , Designation , PAN , UAN no. , Salary , PF , Date of joining etc)  from payslips. 
   



## **How it Looks**
![The First Page of app](https://raw.githubusercontent.com/kartikay-99k/Named-Entity-recognizer-app/main/Screenshot%202022-09-07%20154333.png)    

### Prediction page
![The Predict Page of app](https://raw.githubusercontent.com/kartikay-99k/Named-Entity-recognizer-app/main/predict.png)    



    
## **Steps for building app**   

Step 1. Collected payslips data for model training.   

Step 2. Used Pytesseract-OCR for extracting text from payslips followed by text pre-processing.   

Step 3. Annotated data with online [NER annotator tool](https://tecoholic.github.io/ner-annotator/).  

Step 4. Trained a Custom NER model using spacy.  

Step 5. Built a web app using Flask package which returns extracted entities from uploaded document.   

   
    


## **How To Use**
### Run it locally 

Step 1. Clone the repository 

Step 2. Pip Install all dependencies in   *requirements.txt*  in your conda environment   (You may run `pip install -r requirements.txt` in your shell )  

Step 3. Run  `python  Flask_app.py` in cmd prompt

