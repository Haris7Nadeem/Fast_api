from fastapi import FastAPI,Path,HTTPException,Query
import json
app = FastAPI()

def load_data():
    with open('patients.json','r')as f:
      data= json.load(f)
      return data
   

@app.get('/')
def home():
    return {'msg':'Hi this is home  '}



@app.get('/view')
def view():
    data=load_data()
    return data


@app.get('/patient/{patient_id}')
def view_patient(patient_id:str=Path(...,description='ID of the patient in DB',example='P001')):
    data=load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404,detail='patient not found')


@app.get('/sort')
def sort_patient(sort_by: str =Query(...,description='sort on the basis height ,weight,BMI'),order:str=Query('asc',description='sort in asc and desc order')):
    valid_filds=['height','weight','bmi']

    if sort_by not in valid_filds:
        raise HTTPException(status_code=400,detail= f'inavalid filids chose from {valid_filds}')
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,detail='invalid selct from asc and desc order')
    data=load_data()
    sort_order=True if order =='desc'else False

    sorted_data= sorted(data.values(),key=lambda x:x.get(sort_by,0),reverse=sort_order)
    return sorted_data