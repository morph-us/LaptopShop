from django.shortcuts import render, redirect, HttpResponse
import pymongo
import pandas as pd

#connect to database
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]#select database
mycol = mydb["Items"]#select collection
count=mycol.count_documents({})
   


# Create your views here.
def index(request):
    df = pd.DataFrame(list(mycol.find({},{"_id":0})))
    highest_quant_item_model=df.loc[df['Quantity'].idxmax()]['Model']
    highest_quant_item_brand=df.loc[df['Quantity'].idxmax()]['Brand']
    no_out_of_stock=len(df[df["Quantity"]==0]) 
    no_of_total_items=count
    no_of_brands=len(list(df["Brand"].unique()))
    data=[highest_quant_item_model,highest_quant_item_brand,no_out_of_stock,no_of_total_items,no_of_brands]
    return render(request, 'app/index.html',{'data':data})

def outofstock(request):
    df = pd.DataFrame(list(mycol.find({},{"_id":0})))
    df=df[df["Quantity"]==0]
    df.to_csv('app/templates/app/search.csv', index=False) 
    no_out_of_stock=len(df) 
    data=no_out_of_stock
    return render(request, 'app/searchresult.html',{'query':data,'type':"out of stock items"})

def Model(value):
    model=value
    myquery = { "Model": model }
    mydoc = list(mycol.find(myquery,{"_id":0}))
    df = pd.DataFrame(list(mydoc))
    df.to_csv('app/templates/app/search.csv', index=False)
    return df

def Brand(value):
    brand=value
    myquery = { "Brand":brand }
    mydoc = list(mycol.find(myquery,{"_id":0}))
    df = pd.DataFrame(list(mydoc))
    df.to_csv('app/templates/app/search.csv', index=False)
    return df

def Quantity(value):
    quantity=int(value)
    myquery = { "Quantity": { "$lte": quantity } }
    mydoc = list(mycol.find(myquery,{"_id":0}))
    df = pd.DataFrame(list(mydoc))
    df.to_csv('app/templates/app/search.csv', index=False)
    return df


#switch satatement        
switch={1:Model,
        2:Brand,
        3:Quantity,
        }


def search(request):
    option=int(request.GET['search_by'])
    value=request.GET['value']
    df=switch[option](value)
    querytype=(switch[option])
    if len(df)==0:
        return render(request, 'app/searchresult.html',{'query':"No match found",'type':querytype.__name__ })
    else:    
        return render(request, 'app/searchresult.html',{'query':value,'type':querytype.__name__ })

def insertdata(request):
    global count
    count=count+1
    model=request.GET['model']
    brand=request.GET['brand']
    price=int(request.GET['price'])     
    quantity=int(request.GET['quantity'])
    specs=request.GET['specs']
    item = { "Model": model, "Quantity": quantity,"Brand":brand,"Price":price,"Specifications":specs}
    mycol.insert_one(item)
    df = pd.DataFrame(list(mycol.find({},{"_id":0})))
    df.to_csv('app/templates/app/file.csv', index=False)
    
    return render(request, 'app/view.html',{'model':model})

def view(request):
    df = pd.DataFrame(list(mycol.find({},{"_id":0})))
    df.to_csv('app/templates/app/file.csv', index=False)
    return render(request, 'app/view.html')

def delete(request):
    
    k=mycol.find({},{"_id":0})
    k=list(k)	
    model=k[0]['Model']
    return render(request, 'app/index.html',{'model':model})

def update(request):
    model=request.GET['model']
    price=int(request.GET['price'])     
    quantity=int(request.GET['quantity'])
    myquery = { "Model": model }
    newvalues = { "$set": { "Price": price ,"Quantity": quantity} }
    mycol.update_one(myquery, newvalues)
    df = pd.DataFrame(list(mycol.find({},{"_id":0})))
    df.to_csv('app/templates/app/file.csv', index=False)
    
    return render(request, 'app/view.html')


def removemodel(request):
    model=request.GET['model']
    myquery = { "Model": model }
    mycol.delete_one(myquery)
    df = pd.DataFrame(list(mycol.find({},{"_id":0})))
    df.to_csv('app/templates/app/file.csv', index=False)
    
    return render(request, 'app/view.html')


def insertform(request):
    return render(request, 'app/insertform.html')

def updateform(request):
    return render(request, 'app/updateform.html')

def searchmodelform(request):
    return render(request, 'app/searchmodelform.html')

def searchbrandform(request):
    return render(request, 'app/searchbrandform.html')

def removemodelform(request):
    return render(request, 'app/removemodelform.html')

def searchquantityform(request):
    return render(request, 'app/searchquantityform.html')

def csvfile(request):
    
    return render(request, 'app/file.csv')

def searchcsvfile(request):
    
    return render(request, 'app/search.csv')


