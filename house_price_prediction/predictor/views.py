from django.shortcuts import render
import joblib
import pandas as pd


def predict_price(request):
    localities = list(pd.read_csv('data/house_data.csv')['Locality'].unique())  # Load localities

    if request.method == 'POST':
        try:
            # Get input data
            input_data = {
                'Area': float(request.POST.get('area')),
                'BHK': int(request.POST.get('bhk')),
                'Bathroom': int(request.POST.get('bathroom')),
                'Furnishing': request.POST.get('furnishing'),
                'Locality': request.POST.get('locality'),
                'Parking': int(request.POST.get('parking')),
                'Status': request.POST.get('status'),
                'Transaction': request.POST.get('transaction'),
                'Type': request.POST.get('type')
            }

            # Load model and preprocessor
            model = joblib.load('real_estate_model.pkl')
            preprocessor = joblib.load('data_preprocessor.pkl')

            # Create DataFrame for prediction
            input_df = pd.DataFrame([input_data])

            # Preprocess input
            processed_input = preprocessor.transform(input_df)

            # Make prediction
            prediction = model.predict(processed_input)[0]
            formatted_price = "₹{:,}".format(int(prediction))

            return render(request, 'predictor/result.html', {
                'prediction': formatted_price,
                'input_data': input_data
            })

        except Exception as e:
            return render(request, 'predictor/error.html', {
                'error': str(e),
                'localities': localities
            })

    # GET request - show form with localities
    return render(request, 'predictor/form.html', {
        'localities': localities
    })