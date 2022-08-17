## Table of contents
1. About the application
2. Prerequisites
3. Installation
4. Starting the project
### 1. About the application
***
The application is a django web application that let the user publish or
ask for a review for a specific book. This application is an MVP. Because 
the application is an MVP, I voluntarily kept the style simple and minimal.
When a user creates an account, he/she has the possibility to follow other 
users. When a user follows another user, he/she is able to see reviews and
tickets of this followed user. When a user wish to ask for a review, he/she 
creates a ticket. When a ticket has been created by a user, this ticket can 
receive a review. If a ticket has already received a review, this ticket is 
no longer available. Users haves also the possibility to post a review not 
in response to a ticket. When a user posts a review or a ticket, he/she 
is able to update his/her own tickets/reviews as many times as they want.
***
### 2. Prerequisites
***
For this project, Django 4.0.5, GitHub and Python 3.10 are required.
***
### 3. Installation
***
To work with Django, you need first to install it in the terminal of your 
IDE. Before to install Django, make sure your virtual environment is 
activated. If your virtual environment is not activated run the following 
command "env/bin/activate" in the directory you intend to start the 
project. 

Once your virtual environment is activated, install django by running the
following command in your terminal (in the directory you intend to start the project): 
pip install django. When Django is installed, there is some dependencies 
which are automatically linked to Django. In order to keep track of 
these dependencies run the following command: pip freeze > requirements.txt. 
Thus, all packages required for the project are stored in this file.
***
### 4. Starting the project
***
Once you have successfully installed Django, you can clone the project by
using git clone or git pull with the following address: 
https://github.com/Kmenguete/OpenClassroom_project9.git
When you pulled the project in your local machine, go to the directory 
litreview(in the terminal) and run the following command:
python manage.py runserver
Then you will be able to see the user interface of the django web 
application.
