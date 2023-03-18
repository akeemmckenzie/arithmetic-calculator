# Arithmetic Calculator REST API
Arithmetic Calculator is a web platform providing a simple calculator functionality with a REST API. Users can perform addition, subtraction, multiplication, division, square root operations, and random string generation. Each functionality has a separate cost per request. The user's balance is updated with each request, and requests are denied if the balance isn't sufficient.

This repository includes both the backend (built with Django and Django Rest Framework) and the frontend (built with React and Material-UI).

**Getting Started**
These instructions will help you set up the project on your local machine for development and testing purposes.

**Prerequisites**
Ensure that you have the following software installed on your system:

Python 3.6 or higher
Node.js 12 or higher
npm or yarn

**Backend Setup**

1. Clone the repository:

```
bash
git clone https://github.com/your_username/arithmetic_calculator.git
```

2. Change to the project's root directory:
 
```
bash
cd arithmetic_calculator
```

3. Create a virtual environment and activate it:

```
bash
python -m venv venv
source venv/bin/activate
# On Windows, use `venv\Scripts\activate`
```

4. Install the required packages:
```pip install -r requirements.txt```

5. Apply the migrations:
```python manage.py makemigrations python manage.py migrate```

6. Run the development server:
```python manage.py runserver The backend server will be accessible at http://localhost:8000/.```

**Run Test**

``` python manage.py test calculator.tests ```