# webnest

WebNest is a lightweight Python framework designed for building web applications quickly. It offers easy project setup, server management, database integration, and custom HTML tags (similar to Jinja2) for dynamic content rendering. WebNest also features simple routing to streamline your development process.

## Installation

You can install the package using pip:


```bash
pip install webnest
```

## Project
### For create new project:
```bash
webnest createproject 'project-name'
```
### Every action in project runs from `handle.py` in your project directory


### Available Commands

In the project directory, you can run server using this command:
```bash
python handle.py runserver
``` 
Open [http://127.0.0.1:8000](http://127.0.0.1:8000) to view it in your browser.

If you want to connect to database and migrate table and columns :
- Go to `models.py` in your project directory then add your model ,
    It will be somthing like this:
    ```ruby
    class User (Model):
        name = Model.Fields.TextField(verbose_name='username')
        password = Model.Fields.TextField(verbose_name='password')
        age = Model.Fields.IntField(verbose_name='password')   
    ```
- Then run this commnad to render your changes in `treks` folder in your project directory:
    ```bash
    python handle.py rendertreks
    ``` 

- After render your changes in `treks` folder u have to use this command to trek your changes to database:
    ```bash
    python handle.py trek
    ``` 
> [!NOTE]  
> webnest framework support `sqlite3` only in this version , It will support another type of DB in Upcoming releases , Allah willings

