import shutil
from django.shortcuts import render
from sklearn.model_selection import train_test_split



from .models import userRegisteredTable
from django.core.exceptions import ValidationError
from django.contrib import messages


def userRegisterCheck(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        username = request.POST.get("loginId")
        mobile = request.POST.get("mobile")
        password = request.POST.get("password")
        

        # Create an instance of the model
        user = userRegisteredTable(
            name=name,
            email=email,
            loginid=username,
            mobile=mobile,
            password=password,
            
        )

        try:
            # Validate using model field validators
            user.full_clean()
            
            # Save to DB
            user.save()
            messages.success(request,'registration Successfully done,please wait for admin APPROVAL')
            return render(request, "userRegisterForm.html")


        except ValidationError as ve:
            # Get a list of error messages to display
            error_messages = []
            for field, errors in ve.message_dict.items():
                for error in errors:
                    error_messages.append(f"{field.capitalize()}: {error}")
            return render(request, "userRegisterForm.html", {"messages": error_messages})

        except Exception as e:
            # Handle other exceptions (like unique constraint fails)
            return render(request, "userRegisterForm.html", {"messages": [str(e)]})

    return render(request, "userRegisterForm.html")


def userLoginCheck(request):
    if request.method=='POST':
        username=request.POST['userUsername']
        password=request.POST['userPassword']

        try:
            user=userRegisteredTable.objects.get(loginid=username,password=password)

            if user.status=='Active':
                request.session['id']=user.id
                request.session['name']=user.name
                request.session['email']=user.email
                
                return render(request,'users/userHome.html')
            else:
                messages.error(request,'Status not activated please wait for admin approval')
                return render(request,'userLoginForm.html')
        except:
            messages.error(request,'Invalid details please enter details carefully or Please Register')
            return render(request,'userLoginForm.html')
    return render(request,'userLoginForm.html')


def userHome(request):
    if not request.session.get('id'):
        return render(request,'userLoginForm.html')
    return render(request,'users/userHome.html')

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import matplotlib.pyplot as plt

def training(request):
    if not request.session.get('id'):
        return render(request,'userLoginForm.html')
    

    # Load the Dataset
    # Replace 'cloud_data.csv' with your dataset filename
    # try:
    #     data = pd.read_csv('media/cloud_resource_allocation_dataset.csv')
    # except FileNotFoundError:
    #     print("Error: 'cloud_resource_allocation_dataset.csv' not found. Please upload the file.")
    #     exit()

    # # Rename columns if needed
    # data.columns = [
    #     'CPU_Usage', 'Memory_Usage_MB', 'Network_Usage_MBps', 'Disk_IO_MBps',
    #     'Energy_Consumption_Watts', 'Service_Latency_ms', 'Predicted_Workload_Pct',
    #     'Workload_Type', 'Task_Priority', 'Optimized_Resource_Allocation'
    # ]

    # # Feature Selection and Target Variable
    # X = data[['CPU_Usage', 'Memory_Usage_MB', 'Network_Usage_MBps', 'Disk_IO_MBps']]
    # y = data['Service_Latency_ms']

    # # Normalize Features
    # scaler = StandardScaler()
    # X_scaled = scaler.fit_transform(X)

    # # Split Dataset (70% Train / 30% Test)
    # X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)

    # # Train SVM Model
    # svmModel = SVR(kernel='rbf')
    # svmModel.fit(X_train, y_train)
    # y_pred_svm = svmModel.predict(X_test)

    # # SVM Metrics
    # mse_svm = mean_squared_error(y_test, y_pred_svm)
    # rsq_svm = r2_score(y_test, y_pred_svm)

    # # Train Decision Tree Model
    # treeModel = DecisionTreeRegressor(random_state=42)
    # treeModel.fit(X_train, y_train)
    # y_pred_tree = treeModel.predict(X_test)

    # # Decision Tree Metrics
    # mse_tree = mean_squared_error(y_test, y_pred_tree)
    # rsq_tree = r2_score(y_test, y_pred_tree)

    # # Display Model Metrics
    # print('\n--- Model Performance ---')
    # print(f'SVM:\tMSE = {mse_svm:.4f}\tR² = {rsq_svm:.4f}')
    # print(f'DT:\tMSE = {mse_tree:.4f}\tR² = {rsq_tree:.4f}')

    # # Save the Best Model
    # if mse_svm < mse_tree:
    #     bestModel = svmModel
    #     bestModelName = 'BestModel_SVM.pkl'
    #     bestType = 'SVM'
    # else:
    #     bestModel = treeModel
    #     bestModelName = 'BestModel_DecisionTree.pkl'
    #     bestType = 'Decision Tree'

    # # Save both the best model and the scaler together in a dictionary
    # joblib.dump({'model': bestModel, 'scaler': scaler}, bestModelName)

    # # Save Performance Metrics
    # metrics = pd.DataFrame({
    #     'SVM_MSE': [mse_svm],
    #     'SVM_R2': [rsq_svm],
    #     'DT_MSE': [mse_tree],
    #     'DT_R2': [rsq_tree]
    # })
    # metrics.to_csv('media/model_metrics.csv', index=False)

    # print(f'\nBest model saved as: {bestModelName}')
    # print('Metrics saved to: model_metrics.csv')
    # # Save both the best model and the scaler together in a dictionary

    # # Optional: Plot Predictions vs Actual
    # plt.figure(figsize=(10, 6))
    # plt.plot(y_test.values, 'b-', label='Actual')
    # plt.plot(y_pred_svm, 'r--', label='SVM Prediction')
    # plt.plot(y_pred_tree, 'g-.', label='DT Prediction')
    # plt.xlabel('Sample Index')
    # plt.ylabel('Service Latency (ms)')
    # plt.title('Predicted vs Actual Service Latency')
    # plt.legend()
    # plt.grid(True)
    # plt.show()
    # print("\nResults saved to 'model_performance.csv'")
    results1=pd.read_csv(r'media/model_metrics.csv')
    dff=results1.to_html()
    # Pass DataFrame to template (convert to dict for easier rendering)
    return render(request, 'users/training.html', {
         
        'results_df':dff  # Convert DataFrame to list of dictionaries
    })
import joblib
import numpy as np
import pandas as pd
from django.shortcuts import render

# Load model and scaler once globally (recommended for performance)
try:
    saved_model = joblib.load('media/BestModel_SVM.pkl')
    model = saved_model['model']
    scaler = saved_model['scaler']
    print("Model and scaler loaded successfully.")
except FileNotFoundError:
    model = None
    scaler = None
    print("Error: 'BestModel_SVM.pkl' not found.")

# =============================
def prediction(request):
    result = None
    error = None
    results_df = []

    if request.method == 'POST':
        try:
            if not model or not scaler:
                raise ValueError("Model or scaler not loaded.")

            # Get values from form input
            cpu = float(request.POST.get('cpu'))
            memory = float(request.POST.get('memory'))
            network = float(request.POST.get('network'))
            disk = float(request.POST.get('disk'))

            # Prepare new input
            new_data = np.array([[cpu, memory, network, disk]])

            # Normalize input using the scaler
            new_data_scaled = scaler.transform(new_data)

            # Predict using the model
            prediction_val = model.predict(new_data_scaled)

            # Convert to dataframe for display
            results_df = pd.DataFrame([{
                "CPU_Usage_percent": cpu,
                "Memory_Usage_MB": memory,
                "Network_Usage_MBps": network,
                "Disk_I_O_MBps": disk,
                "Predicted_Latency_ms": round(prediction_val[0], 2)
            }])

            result = round(prediction_val[0], 2)

        except Exception as e:
            error = str(e)

    return render(request, 'users/prediction.html', {
        'result': result,
        'error': error,
        'results_df': results_df.to_dict(orient="records") if not results_df.empty else []
    })
