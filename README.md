# Getting Started

First clone the repository from Github and switch to the new directory:

    $ git clone https://github.com/anarkopin/extract_data_pdf.git
    $ cd {{ project_name }}
    
Activate the virtualenv for your project.
    $ python -m venv env
    $ .\env\Scripts\Activate


Install project dependencies:

    $ pip install -r requirements.txt
    
    
Then simply apply the migrations:

    $ python manage.py migrate
    

You can now run the development server:

    $ python manage.py runserver
