from flask import Flask, render_template, request
from util import *
from model import LinearModel
from pattern import Pattern

app = Flask(__name__)

data = pd.DataFrame()
model = None

i = 0
def get_data():
    global data
    if(data == None):
        read_data()

    return data


def read_data():
    global data, model
    dsname = 'Allstate-cost-cleaned.csv'
    data = load_data(dsname)
    data = preprocess_data(data)
    y = data['cost']
    X = data.drop('cost', axis=1)
    model = LinearModel(X, y, data.drop('cost', axis=1).columns)


@app.route("/")
def hello_world():
    global data, model, i
    if(data.empty):
        read_data()
        print(f"Reading data for {i}th time")
        i+=1
        model = model.train()

    rsq = model.rsquared
    mse_t = model.mse_total
    mse_m = model.mse_model
    mse_resid = model.mse_resid
    return render_template("index.html", rsquared=rsq, mse_t=mse_t, mse_resid=mse_resid, mse_m=mse_m)

@app.route("/predict", methods=["POST", "GET"])
def predict():
    global data, model, i
    if(data.empty):
        read_data()
        print(f"Reading data for {i}th time")
        i+=1
        model = model.train()
    
    # print("Request recieved")
    post_data = request.json
    # print("Data columns: ", model.get_columns())
    # print("Data columns len: ", len(model.get_columns()))
    # print("Data pattern: ", post_data)
    
    region              = post_data['region']
    car_value           = post_data['car_value']
    group_size          = post_data['group_size']
    car_age             = post_data['car_age'] 
    risk_factor         = post_data['risk_factor']
    age_oldest          = post_data['age_oldest']
    age_youngest        = post_data['age_youngest']
    C_previous          = post_data['C_previous']
    duration_previous   = post_data['duration_previous']
    homeowner           = post_data['homeowner']
    married_couple      = post_data['married_couple']
    coverages           = post_data['coverages']

    pattern = Pattern(region, group_size, homeowner, car_age, car_value,
            risk_factor, age_oldest, age_youngest, married_couple,
            C_previous, duration_previous, coverages)
    
    pattern_array = pattern.get_pattern_array()
    # print("Pattern array: ", pattern_array)
    # print("Pattern array len: ", len(pattern_array))
    predicted = model.predict(pattern_array)
    # print("Predicted cost: ", predicted)
    return str(round(predicted[0], 3))

if __name__ == "__main__":
    app.run(debug=True, port=8990)
