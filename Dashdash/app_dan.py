from flask import Flask, render_template, request
import plotly
import plotly.graph_objs as go
import pandas as pd
import json
from sqlalchemy import create_engine
from werkzeug.wrappers import Request, Response

import joblib

model = joblib.load('Churn_pred')

app = Flask(__name__)

df = pd.read_csv('df_churn.csv')

def category_plot(
    cat_plot = 'histplot',
    cat_x = 'occupation', cat_y = 'age',
    estimator = 'count', hue = 'churn'):
    
    if cat_plot == 'histplot':
        data = []
        for val in df[hue].unique():
            hist = go.Histogram(
                x=df[df[hue]==val][cat_x],
                y=df[df[hue]==val][cat_y],
                histfunc=estimator,
                name=str(val)
            )
            data.append(hist)
        title='Histogram'
    elif cat_plot == 'boxplot':
        data = []

        for val in df[hue].unique():
            box = go.Box(
                x=df[df[hue] == val][cat_x], #series
                y=df[df[hue] == val][cat_y],
                name=str(val)
        )
            data.append(box)
        title='Box'
        
    if cat_plot == 'histplot':
        layout = go.Layout(
            title=title,
            xaxis=dict(title=cat_x),
            yaxis=dict(title=estimator),
            boxmode = 'group'
        )
    else:
        layout = go.Layout(
            title=title,
            xaxis=dict(title=cat_x),
            yaxis=dict(title=cat_y),
            boxmode = 'group'
        )
    result = {'data': data, 'layout': layout}
    graphJSON = json.dumps(result, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

@app.route('/')
def index():
    plot = category_plot()
    list_plot = [('histplot', 'Histogram'), ('boxplot', 'Box')]
    list_x = [('dependents', 'dependents'), ('occupation', 'occupation')]
    list_y = [('current_balance', 'current_balance'), ('age', 'age'),("current_month_credit","current_month_credit"),("previous_month_credit","previous_month_credit")]
    list_est = [('count', 'Count'), ('avg', 'Average'), ('max', 'Max'), ('min', 'Min')]
    list_hue = [('gender','gender'),("customer_nw_category","customer_nw_category"),("churn","churn")]

    return render_template(
        'category.html',
        plot=plot,
        focus_plot='histplot',
        focus_x='dependetns',
        focus_estimator='count',
        focus_hue='churn',
        drop_plot= list_plot,
        drop_x= list_x,
        drop_y= list_y,
        drop_estimator= list_est,
        drop_hue= list_hue)

@app.route('/cat_fn/<nav>') ## CEKCEKCEK
def cat_fn(nav):

    # saat klik menu navigasi
    if nav == 'True':
        cat_plot = 'histplot'
        cat_x = 'occupation'
        cat_y = 'age'
        estimator = 'count'
        hue = 'churn'
        
    else:
        cat_plot = request.args.get('cat_plot')
        cat_x = request.args.get('cat_x')
        cat_y = request.args.get('cat_y')
        estimator = request.args.get('estimator')
        hue = request.args.get('hue')

    if estimator == None:
        estimator = 'count'
    
    if cat_y == None:
        cat_y = 'age'
        
    list_plot = [('histplot', 'Histogram'), ('boxplot', 'Box')]
    list_x = [('dependents', 'dependents'), ('occupation', 'occupation')]
    list_y = [('current_balance', 'current_balance'), ('age', 'age'),("current_month_credit","current_month_credit"),("previous_month_credit","previous_month_credit")]
    list_est = [('count', 'Count'), ('avg', 'Average'), ('max', 'Max'), ('min', 'Min')]
    list_hue = [('gender','gender'),("customer_nw_category","customer_nw_category"),("churn","churn")]

    plot = category_plot(cat_plot, cat_x, cat_y, estimator, hue)
    return render_template(
        # file yang akan menjadi response dari API
        'category.html',
        # plot yang akan ditampilkan
        plot=plot,
        # menu yang akan tampil di dropdown 'Jenis Plot'
        focus_plot=cat_plot,
        # menu yang akan muncul di dropdown 'sumbu X'
        focus_x=cat_x,
        focus_y=cat_y,

        # menu yang akan muncul di dropdown 'Estimator'
        focus_estimator=estimator,
        # menu yang akan tampil di dropdown 'Hue'
        focus_hue=hue,
        # list yang akan digunakan looping untuk membuat dropdown 'Jenis Plot'
        drop_plot= list_plot,
        # list yang akan digunakan looping untuk membuat dropdown 'Sumbu X'
        drop_x= list_x,
        # list yang akan digunakan looping untuk membuat dropdown 'Sumbu Y'
        drop_y= list_y,
        # list yang akan digunakan looping untuk membuat dropdown 'Estimator'
        drop_estimator= list_est,
        # list yang akan digunakan looping untuk membuat dropdown 'Hue'
        drop_hue= list_hue
    )

##################
## SCATTER PLOT ##
##################

# scatter plot function
def scatter_plot(cat_x, cat_y, hue):


    data = []

    for val in df[hue].unique():
        scatt = go.Scatter(
            x = df[df[hue] == val][cat_x],
            y = df[df[hue] == val][cat_y],
            mode = 'markers',
            name = str(val)
        )
        data.append(scatt)

    layout = go.Layout(
        title= 'Scatter',
        title_x= 0.5,
        xaxis=dict(title=cat_x),
        yaxis=dict(title=cat_y)
    )

    result = {"data": data, "layout": layout}

    graphJSON = json.dumps(result,cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

@app.route('/scatt_fn')
def scatt_fn():
    cat_x = request.args.get('cat_x')
    cat_y = request.args.get('cat_y')
    hue = request.args.get('hue')

    # WAJIB! default value ketika scatter pertama kali dipanggil
    if cat_x == None and cat_y == None and hue == None:
        cat_x = 'occupation'
        cat_y = 'age'
        hue = 'churn'

    # Dropdown menu
    list_x = [('dependents', 'dependents'), ('occupation', 'occupation')]
    list_y = [('current_balance', 'current_balance'), ('age', 'age'),("current_month_credit","current_month_credit"),("previous_month_credit","previous_month_credit")]
    list_hue = [('gender','gender'),("customer_nw_category","customer_nw_category"),("churn","churn")]

    plot = scatter_plot(cat_x, cat_y, hue)

    return render_template(
        'scatter.html',
        plot=plot,
        focus_x=cat_x,
        focus_y=cat_y,
        focus_hue=hue,
        drop_x= list_x,
        drop_y= list_y,
        drop_hue= list_hue
    )

##############
## PIE PLOT ##
##############

def pie_plot(hue = 'churn'):
    


    vcounts = df[hue].value_counts()

    labels = []
    values = []

    for item in vcounts.iteritems():
        labels.append(item[0])
        values.append(item[1])
    
    data = [
        go.Pie(
            labels=labels,
            values=values
        )
    ]

    layout = go.Layout(title='Pie', title_x= 0.48)

    result = {'data': data, 'layout': layout}

    graphJSON = json.dumps(result,cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

@app.route('/pie_fn')
def pie_fn():
    hue = request.args.get('hue')

    if hue == None:
        hue = 'churn'

    list_hue = [('gender','gender'),("customer_nw_category","customer_nw_category"),("churn","churn")]

    plot = pie_plot(hue)
    return render_template('pie.html', plot=plot, focus_hue=hue, drop_hue= list_hue)
        
@app.route('/predict')        
def predict():
    ml=pd.read_csv('df_churn.csv')
    tab=ml.head(1000)
    return render_template('predict.html',data=tab.values) 
            
        
@app.route('/result', methods=['POST', 'GET'])
def result():
    
    if request.method == 'POST':
    ## Untuk Predict
    
        got=request.form
        
        age=int(got['age'])
        
        gender_Female=""
        if got["gender"] == "Female" :
            gender_Female =1
        else :
            gender_Female =0
        
        gender_Male=""
        if got["gender"] == "Male" :
            gender_Male =1
        else :
            gender_Male =0
        
        dependents = int(got["dependents"])
        
        occupation =""
        if got["occupation"] == "student" :
            occupation =0
        elif got["occupation"] == "salaried" :
            occupation =1
        elif got["occupation"] == "self_employed" :
            occupation =2
        elif got["occupation"] == "company" : 
            occupation =3
        elif got["occupation"] == "retired" :
            occupation =4
        
        customer_nw_category=""
        if int(got["customer_nw_category"])==3 :
            customer_nw_category=0
        elif int(got["customer_nw_category"])==2 :
            customer_nw_category=1
        elif int(got ["customer_nw_category"])==1 :
            customer_nw_category =2
        
        current_balance=float(got["current_balance"])
        
        current_month_credit=float(got["current_month_credit"])
        
        previous_month_credit=float(got["previous_month_credit"])
        
        
        
        
        
        
        
        
        
            

            
        pred = model.predict_proba([[age,dependents, occupation,
                               customer_nw_category,current_balance,current_month_credit,
                               previous_month_credit,gender_Female,gender_Male]])[0][1]

#         ## Untuk Isi Data
        
        gender_dt=""
        if got["gender"] == "Female":
            gender_dt = "Female"
        elif got["gender"] == "Male":
            gender_dt = "Male"
        
        occupation_dt =""
        if got["occupation"] == "student" :
            occupation_dt= "student"
        elif got["occupation"] == "salaried" :
            occupation_dt = "salaried"
        elif got["occupation"] == "self_employed" :
            occupation_dt = "self_employed"
        elif got["occupation"] == "company" : 
            occupation_dt = "company"
        elif got["occupation"] == "retired" :
            occupation_dt = "retired"
        
        customer_nw_category_dt=""
        if int(got["customer_nw_category"])==3:
            customer_nw_category_dt="3"
        elif int(got["customer_nw_category"])==2:
            customer_nw_category_dt="2"
        elif int(got ["customer_nw_category"])==1:
            customer_nw_category_dt ="1"
            
#         result = [name_count,desc_count,main_category_dt_Art,main_category_dt_Comics,main_category_dt_Crafts,main_category_dt_Dance,
#         main_category_dt_Design,main_category_dt_Fashion,main_category_dt_Film_Video,main_category_dt_Food,main_category_dt_Games,
#         main_category_dt_Journalism,main_category_dt_Music,main_category_dt_Photography,main_category_dt_Publishing,
#         main_category_dt_Technology,main_category_dt_Theater,country_dt_US,country_dt_GB,country_dt_CA,
#         country_dt_AU,country_dt_NL,country_dt_NZ,country_dt_SE,country_dt_DK,country_dt_NO,country_dt_IE,country_dt_DE,Month_dt,Launched_Deadline,
#         backers_count]
        

        return render_template('result.html',
            age=int(got['age']),gender=gender_dt,dependents = int(got["dependents"]),
            occupation=occupation_dt, customer_nw_category=customer_nw_category_dt,
            current_balance=float(got['current_balance']),
            current_month_credit=float(got['current_month_credit']),
            previous_month_credit=float(got['previous_month_credit']),
            churn_pred=pred)

if __name__ == "__main__":
    app.run(debug=False)