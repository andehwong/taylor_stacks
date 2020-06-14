# Taylor Stacks

**Taylor Stacks** is an open-source web scraping tool to accurately convert data from University of Western Ontario's 
(also known as Western University) course calendar into a read-able JSON format.

The name **Taylor Stacks** is an homage to the infamous library on the University of Western Ontario campus known as
Taylor Library, where many Western students spent their blood, sweat and tears in pursuit of higher education.

The project is currently a **work-in-progress**.

### Prerequisites
Before running the script, you require the following:
* Python 3.8+
* requests library
* BeautifulSoup library

### Running Taylor Stacks
Before running the scraper, you have to install the following libraries:
```
pip install -r requirements.txt
```

Running Taylor Stacks is very straight forward thus far. All you have to do is execute:
```
python main.py
```
or 
```
python3 main.py
```
... depending on how many versions of Python you have running on your local machine.

### TO-DO
* Prerequisite scraping
    * ~~Prerequisites that have course lists where all courses are prerequisites~~
    * *"or"* prerequisites, where the student must have at least one of the aforementioned "or" list
    * *"Either"* groups, where the student must satisfy one of the groups of prerequisites
    * *"At least 1.0/2.0"* groups, where a student must have a certain number of courses from a list
    * Minimum marks for certain courses
    * Permission from department
