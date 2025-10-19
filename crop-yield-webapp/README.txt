Crop Yield Webapp
-----------------
This package contains a simple Flask web application that loads a pre-trained crop yield model
(a scikit-learn model saved as 'crop_yield_model.pkl') and provides a web UI for predictions.

IMPORTANT:
- Place your actual 'crop_yield_model.pkl' file in the project root (/app) before running.
- If the model file is missing, the app will return an error on prediction.

How to run (local):
  1. create a virtualenv: python -m venv venv
  2. activate it: source venv/bin/activate   (Linux/Mac) or venv\Scripts\activate (Windows)
  3. pip install -r requirements.txt
  4. python app.py
  5. open http://localhost:5000

How to deploy (prod):
  - Use Render, Railway, Heroku, or Docker. The app uses Gunicorn in production.