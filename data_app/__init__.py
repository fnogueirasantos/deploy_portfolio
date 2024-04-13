# Imports
from flask import render_template, url_for, redirect, flash, request, Response
import pandas as pd
from flask_login import login_user, LoginManager, login_required, logout_user
from .models import app, db, User, RegisterForm, LoginForm
from .analytics.dash_01.dashboard import create_dashboard_01
from .analytics.dash_02.dashboard import create_dashboard_02
from .analytics.dash_03.dashboard import create_dashboard_03
from .data_science.regression.regression_model import ModelRegresison, FeaturesRegression
from .data_science.classification.classification_model import ModelClasifier, FeaturesClassification
from .data_science.budget_marketing.regression_model import ModelBudgetMkt, FeaturesBudgetMkt
from .data_science.predict_lead.predict_model import Model_Lead_Predict, Features_Lead_Predict
from .api.api import APIBackend

#### LOGIN CONFIGS 
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Initialize
with app.app_context():
    db.create_all()
    dash_app1 = create_dashboard_01(app)
    dash_app2 = create_dashboard_02(app)
    dash_app3 = create_dashboard_03(app)

#### ROUTES

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Login failed. Check your username and password.', 'danger')
    return render_template('login.html', form=form)


@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html')

@ app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Thanks for registering! Now you can login!')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/dashboard1/')
@login_required
def dashboard1():
    return dash_app1.index()

@app.route('/dashboard2/')
@login_required
def dashboard2():
    return dash_app2.index()

@app.route('/dashboard3/')
@login_required
def dashboard3():
    return dash_app3.index()

@app.route("/otherprojects")
@login_required
def otherprojects():
    return render_template("other_projects.html")

@app.route("/other_project_01")
@login_required
def other_project_01():
    return render_template("Jup_other_project_01.html")

@app.route("/other_project_02")
@login_required
def other_project_02():
    return render_template("data_clean.html")

@app.route("/other_project_03")
@login_required
def other_project_03():
    return render_template("clustering.html")

@app.route('/regression', methods=['GET', 'POST'])
@login_required
def regression():
    form = FeaturesRegression()
    model_regression_instance = ModelRegresison()

    if form.validate_on_submit():
        age = form.age.data
        bmi = float(form.bmi.data)
        print(bmi)
        smoker = 1 if form.smoker.data == 'Yes' else 0  # Mapping 'Yes' to 1 and 'No' to 0
        predicted_value = model_regression_instance.new_predict(age, bmi, smoker)
        value_predict_anually = f"U$ {predicted_value[0]:.2f}"
        value_predict_monthly = f"U$ {predicted_value[0]/12:.2f}"
        return render_template("predict_regression.html", form=form, value_predict_anually=value_predict_anually,value_predict_monthly=value_predict_monthly)
    
    return render_template('regression.html', form=form)

@app.route("/doc_regression_app_01")
@login_required
def doc_regression_app_01():
    return render_template("doc_regression.html")


@app.route('/classification', methods=['GET', 'POST'])
@login_required
def classification():
    form = FeaturesClassification()
    model_classification_instance = ModelClasifier()    
    
    if form.validate_on_submit(): 
        features = {
            'gender': form.gender.data,
            'SeniorCitizen': form.senior_citizen.data,
            'Partner': form.partner.data,
            'Dependents': form.dependents.data,
            'tenure': form.tenure.data,
            'PhoneService': form.phone_service.data,
            'MultipleLines': form.multiple_lines.data,
            'InternetService': form.internet_service.data,
            'OnlineSecurity': form.online_security.data,
            'OnlineBackup': form.online_backup.data,
            'DeviceProtection': form.device_protection.data,
            'TechSupport': form.tech_support.data,
            'StreamingTV': form.streaming_tv.data,
            'StreamingMovies': form.streaming_movies.data,
            'Contract': form.contract.data,
            'PaperlessBilling': form.paperless_billing.data,
            'PaymentMethod': form.payment_method.data,
            'TotalCharges': form.total_charges.data
        }
        predictions = model_classification_instance.new_predict(features)
        probability_Churn_Yes = str(round(predictions['Probability_Churn_Yes'].values[0], 2)) + ' %'
        return render_template("predict_classification.html", form=form, probability_Churn_Yes=probability_Churn_Yes)
    return render_template('classification.html', form=form)

@app.route("/doc_classification_app_01")
@login_required
def doc_classification_app_01():
    return render_template("doc_classification.html")


@app.route('/budgetmarketing', methods=['GET', 'POST'])
@login_required
def budgetmarketing():
    form = FeaturesBudgetMkt()
    model_marketing_budget = ModelBudgetMkt()    
    
    if form.validate_on_submit(): 
        features = {
            'Period_01': form.Period_01.data,
            'Period_02': form.Period_02.data,
            'Period_03': form.Period_03.data,
            'Period_04': form.Period_04.data,
            'Period_05': form.Period_05.data,
            'Period_06': form.Period_06.data,
            'Period_07': form.Period_07.data,
            'Period_08': form.Period_08.data,
            'Period_09': form.Period_09.data,
            'Period_10': form.Period_10.data,
            'Period_11': form.Period_11.data,
            'Period_12': form.Period_12.data,
        }
        dataframe, predictions = model_marketing_budget.new_predict(features)
        
        return render_template("predict_budget_marketing.html", form=form, predictions=predictions, dataframe = dataframe)
    return render_template('budget_marketing.html', form=form)

@app.route("/doc_budget_marketing")
@login_required
def doc_budget_marketing():
    return render_template("doc_budget_marketing.html")


@app.route('/download_csv', methods=['POST'])
@login_required
def download_csv():
    if request.method == 'POST':
        # Get predictions data from the form
        predictions_json = request.form.get('predictions')


        print(predictions_json)

        # Convert JSON string to DataFrame
        df_predictions = pd.read_json(predictions_json)

        # Convert DataFrame to CSV
        csv_data = df_predictions.to_csv(index=False)

        # Return the CSV file as an attachment with specified filename
        headers = {
            'Content-Disposition': 'attachment; filename=marketing_budget_predictions.csv'
        }

        return Response(
            csv_data,
            mimetype='text/csv',
            headers=headers
        )

    else:
        return "Method Not Allowed"


@app.route('/leadpredict', methods=['GET', 'POST'])
@login_required
def leadpredict():
    form = Features_Lead_Predict()
    model_lead_predict = Model_Lead_Predict()   
    if form.validate_on_submit(): 
        target_converted_users = form.target_converted_users.data
        min_budget = form.min_budget.data
        max_budget = form.max_budget.data
        predictions2, df_simulations = model_lead_predict.new_predict_simulation(target_converted_users, min_budget, max_budget)
        df_check = df_simulations[df_simulations['Converted_users'] == target_converted_users].head(1)
        if not df_check.empty:
            df_simulations = df_simulations[df_simulations['Converted_users'] == target_converted_users].head(1)
        else:
            df_simulations = pd.DataFrame({'Number_of_views': '-',
                                           'Number_of_clicks': '-',
                                           'Converted_users': '-',
                                           'Budget': 'Budget Enough!!'}, index=[0])
        df_simulations.rename(columns={'Number_of_views': 'Number of views',
                                           'Number_of_clicks': 'Number of clicks',
                                           'Converted_users': 'Converted users'},
                                           inplace=True)
        return render_template("predict_lead.html", predictions2=predictions2, form=form, dataframe_lead=df_simulations.head(1))
    return render_template('lead_predict.html', form=form)

@app.route("/doc_lead_predict")
@login_required
def doc_lead_predict():
    return render_template("doc_lead_predict.html")

@app.route('/download_csv2', methods=['POST'])
@login_required
def download_csv2():
    if request.method == 'POST':
        # Get predictions data from the form
        predictions_json = request.form.get('predictions2')
        # Convert JSON string to DataFrame
        df_predictions = pd.read_json(predictions_json)

        # Convert DataFrame to CSV
        csv_data = df_predictions.to_csv(index=False)

        # Return the CSV file as an attachment with specified filename
        headers = {
            'Content-Disposition': 'attachment; filename=lead_predictions.csv'
        }

        return Response(
            csv_data,
            mimetype='text/csv',
            headers=headers
        )

    else:
        return "Method Not Allowed"

api_backend = APIBackend()
@app.route('/api/pizza_sales')
def home_api():
    return render_template('api.html')

@app.route('/api/pizza_sales/<int:query_id>')
def get_pizza_sales(query_id):
    return api_backend.get_data_pizza_sales(query_id)

@app.route('/api/pizza_sales/sales_predict')
def make_predicts():
    return api_backend.sales_predict()