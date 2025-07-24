# Investment Portfolio Allocation System

A Django application that provides personalized investment portfolio recommendations based on user financial profiles and risk tolerance.

## Features

- Asset allocation recommendations across multiple asset classes (equity, debt, gold, real estate, crypto, cash)
- Risk profile determination based on user inputs
- Equity portfolio optimization with stock recommendations
- Responsive web interface with visualization of allocation

## Project Structure

```
hackathon/
├── core/                   # Main Django app
│   ├── migrations/         # Database migrations
│   ├── static/             # Static files (CSS, JS)
│   │   ├── css/
│   │   └── js/
│   ├── templates/          # HTML templates
│   │   └── core/
│   ├── templatetags/       # Custom template tags
│   ├── admin.py            # Admin configuration
│   ├── apps.py             # App configuration
│   ├── models.py           # Data models
│   ├── serializers.py      # API serializers
│   ├── urls.py             # URL routing
│   ├── utils.py            # Utility functions
│   └── views.py            # View controllers
├── hackathon_project/      # Django project settings
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── scripts/                # Investment allocation scripts
│   ├── bond_monte_carlo.py # Bond portfolio optimization
│   ├── crypto_monte_carlo.py # Crypto portfolio optimization
│   ├── currency_monte_carlo.py # Currency portfolio optimization
│   ├── equity_monte_carlo.py # Equity portfolio optimization
│   ├── prediction_allocation.py # Asset allocation prediction
│   ├── top_instruments.py  # Instrument recommendations
│   ├── *.csv               # Market data files
│   └── *.joblib            # ML model files
├── manage.py               # Django management script
├── requirements.txt        # Project dependencies
└── README.md               # This file
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone https://github.com/devrj17/NexAlt.git
   cd NexAlt
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Create a superuser (optional):
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

7. Access the application at http://127.0.0.1:8000/

## Usage

1. Fill out the investment profile form with your financial details and risk preferences
2. Submit the form to receive personalized asset allocation recommendations
3. View recommended instruments for each asset class based on your risk profile

## License

This project is open source and available under the [MIT License](LICENSE).