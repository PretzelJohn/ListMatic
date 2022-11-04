ListMatic
=========
ListMatic is a web application that allows users to collaborate on lists. Families can use ListMatic to create chore lists, Christmas lists, grocery lists, and to-do lists. List owners can invite others to view or edit the lists they create.

Team Members
------------
- John Hussey
- Bray Bueres Torres
- Kishan M
- Ryan Kim

Technology
----------
ListMatic is built using the Python Flask web framework, with SQLAlchemy for ORM database communication, Flask Login for user authentication, and Flask WTF for form security and validation.
The web application is hosted on AWS, using the following services:
- EC2 to host the application server and run it via gunicorn and nginx
- RDS to host the MySQL database
- S3 to store static files such as public images

Getting Started
---------------
1.  Clone the GitHub repo into a convenient location<br>
    `git clone https://github.com/PretzelJohn/ListMatic.git ListMatic`
    
2.  Install Python 3<br>
    https://www.python.org/downloads/
    
3.  Install Python virtualenv<br>
    `pip install virtualenv`

4.  Open the cloned folder in your terminal<br>
    `cd ListMatic`

5.  Activate the virtual environment
    - `venv\scripts\activate` (Windows)
    - `. venv/bin/activate` (MacOS)
    - `source venv/bin/activate` (Linux)

6.  Install the requirements<br>
    `pip install -r requirements.txt`

7.  Start the Flask app<br>
    `flask run`
