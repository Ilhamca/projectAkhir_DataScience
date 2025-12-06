# Food Nutrition Analyzer Web Application

## Setup Instructions

### 1. Export the Model
First, run the export script to save the trained model:

```bash
python export_model.py
```

This will create:
- `websait/model.pkl` - The trained Random Forest model
- `websait/scaler.pkl` - The feature scaler
- `websait/nutrition_data.csv` - Nutrition database

### 2. Setup Web Server

#### Option A: Using PHP Built-in Server
```bash
cd websait
php -S localhost:8000
```

Then open your browser to: `http://localhost:8000`

#### Option B: Using XAMPP/WAMP
1. Copy the `websait` folder to your `htdocs` directory
2. Start Apache server
3. Open: `http://localhost/websait`

### 3. Requirements
- Python 3.x with packages:
  - pandas
  - numpy
  - scikit-learn
  - pickle
- PHP 7.4 or higher
- Web browser

## Features

### 1. Nutrition Analysis
- Enter calories, proteins, fat, and carbohydrate values
- Get instant classification (Good/Moderate/Poor nutrition)
- View detailed nutrition facts including:
  - Total macronutrients
  - Macronutrient ratios
  - Calorie density

### 2. Food Database Browser
- Browse existing foods from the dataset
- Click any food item to auto-fill the form
- See nutrition labels for each food

### 3. Classification Categories
- **Good Nutrition** (Label 0): Balanced macronutrient profile
- **Moderate Nutrition** (Label 1): Acceptable but could be better
- **Poor Nutrition** (Label 2): Not optimal, consume with caution

## Files Structure

```
websait/
├── index.html          # Main web interface
├── predict.php         # Prediction endpoint
├── predict_api.py      # Python prediction script
├── get_foods.php       # Food database API
├── model.pkl           # Trained model (generated)
├── scaler.pkl          # Feature scaler (generated)
└── nutrition_data.csv  # Nutrition database (generated)
```

## How It Works

1. User enters nutrition values in the web form
2. PHP receives the data and calls Python script
3. Python loads the trained model and makes prediction
4. Result is returned to PHP and displayed to user
5. User sees classification with detailed nutrition facts

## Notes

- Make sure Python is accessible from command line
- The model uses the same preprocessing as the training notebook
- All nutrition values are scaled using StandardScaler before prediction
- The system can classify any food based on its macronutrient profile
