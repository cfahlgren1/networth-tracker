## School Registration System - Backend API

*This is for a class project and is not fully production ready*

#### Setup 
---

Install libraries

```
pip3 install -r requirements.txt
```

##### In the RSB root folder

Apply migration changes to DB

```python
python3 manage.py migrate
```


Start the Server

```python
python manage.py runserver
```

Visit `http://localhost:8000`

### API
---
Visit  `localhost:8000/api/`

#### Valid API Endpoints

```json
{
    "courses": "http://localhost:8000/api/courses/",
    "addRequests": "http://localhost:8000/api/addRequests/",
    "dropRequests": "http://localhost:8000/api/dropRequests/",
    "professors": "http://localhost:8000/api/professors/",
    "students": "http://localhost:8000/api/students/",
    "enrollmentSummaries": "http://localhost:8000/api/enrollmentSummaries/",
    "gradeReports": "http://localhost:8000/api/gradeReports/",
    "advisors": "http://localhost:8000/api/advisors/"
}
```

Example Endpoint Response: `http://localhost:8000/api/courses/`

```json
[
    {
        "name": "Science",
        "professor": "Caleb Fahlgren",
        "crn": 1235755,
        "description": "",
        "price": 350.49
    },
    {
        "name": "Math",
        "professor": "Caleb Fahlgren",
        "crn": 23666,
        "description": "",
        "price": 225.0
    }
]
```