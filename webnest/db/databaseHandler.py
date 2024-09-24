import sqlite3
import re
import inspect
###########pack modules
from settings import *

validate_columns=r'^[A-Za-z_][A-Za-z0-9_]*\s+(INTEGER|TEXT|REAL|BLOB|NUMERIC)$'
class dataBase:
    def __init__(self):
        self.connection =sqlite3.connect(DATABASE_NAME)
        self.curser = self.connection.cursor()
        self.error = ''

    def validate_identifier(self ,*identifier):
        """ Validate table names, column names, and index names to prevent SQL injection. """
        validate = r'^[A-z_][A-z0-9_]*$'
        for iden in identifier:
            if not re.match(validate,iden):
                raise ValueError(f"Invalid identifier: {iden} "
                                  "you are avalable to use letters "
                                  "and numbers but not in the "
                                  "beginning of the word and you are "
                                  "avalable to use this character "
                                  " `_`")
    
    def execute(self,query, params =None):
        """ Execute a dynamic SQL command """
        try:
            if params: 
                self.curser.execute(query,params)
            else:      
                self.curser.execute(query)
            self.connection.commit()
        except Exception as e:
            # print("Error: " , e) #logging
            self.error = f"Error:{e}"
            self.connection.rollback()

    def execute_noParams(self,command_type = str,*args):
        """ Execute a dynamic SQL command after validation. """
        command = command_type.lower()
        if command == 'create table':
            try:
                table_name = args[0]
                self.validate_identifier(table_name)
                self.execute(f'CREATE TABLE if not exists {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT)')
            except Exception as e :
                # print("Error:",e) 
                self.error = f"Error:{e}" 
                self.connection.rollback()  

        elif command == 'alter table':
            try:
                if len(args) == 1 and isinstance(args[0],list):
                    table_name,alteration = args[0][0],args[0][1:]
                self.validate_identifier(table_name)
                alt = ','.join(alteration)
                self.execute(f'AlTER TABLE {table_name} {alt}')
            except Exception as e :
                # print(e)
                self.error=f"Error:{e}"
                self.connection.rollback()

        elif command == 'create index':pass
        elif command == 'drop table':
            try:
                table_name = args[0]
                self.validate_identifier(table_name)
                self.execute(f'DROP TABLE IF EXISTS {table_name}')
            except Exception as e :
                # print("Error:",e)
                self.error = f"Error:{e}"
                self.connection.rollback()

        elif command == 'drop index':pass
        elif command == 'create view':pass

    def fetchall(self):
        """Fetch all in Data base"""
        return self.curser.fetchall()
    
    def close(self):
        """Close connection Data base"""
        return self.curser.close()
    


class Model:
    dataBase = dataBase
    __model_name__ =None
    _models_registry = []
    _model_attrs = []
      
    def __init_subclass__(cls):
        cls.__model_name__ = cls.__name__.lower()
        model_name = cls.__model_name__

        # cls.__create_table__()
        def m_R(): return model_name,{
                key:value for key, value in cls.__dict__.items() 
                if not inspect.isfunction(value) and not key.startswith('__') 
                and not isinstance(value, str)
            }
        cls._models_registry.append([m_R()])
        cls._model_attrs = m_R()
  
    @classmethod
    def __create_table__(cls,name = None):
        """Create table in database"""
        return cls.dataBase().execute_noParams('create table',name or cls.__model_name__)
    
    @classmethod
    def __insert__(cls, **kwargs):
        columns = ', '.join(kwargs.keys())
        placeholders = ', '.join('?' * len(kwargs))
        # cls.dataBase().validate_identifier(cls.table_name,columns)
        query = f"INSERT INTO {cls.table_name} ({columns}) VALUES ({placeholders})"
        cls.dataBase().execute(query, tuple(kwargs.values()))

    @classmethod
    def object(cls,col_name):
        """Select one column from table and fetch all"""
        cls.dataBase().validate_identifier(cls.table_name,col_name)
        query = f'select {col_name} from {cls.table_name}'
        cls.dataBase().execute(query)
        return cls.dataBase().fetchall()

    @classmethod 
    def all(cls):
        """Select all columns from table and fetch all"""
        cls.dataBase().validate_identifier(cls.table_name)
        query = f'select * from {cls.table_name}'
        cls.dataBase().execute(query)
        return cls.dataBase().fetchall()

    #get one column

    class Fields:
        class BaseField:
            def __init__(self,verbose_name: str ): 
                self.verbose_name = verbose_name

            def add_column(self,table_name,verbose_name, field_type):
                 """Add column in table"""
                 Model.dataBase().validate_identifier(table_name,verbose_name)
                 Model.dataBase().execute_noParams(
                    'alter table',
                    [ f'{table_name}', f'ADD COLUMN {verbose_name} {field_type}']
                )
            def delete_column(self,table_name,verbose_name):
                 """Delete column in table"""
                 Model.dataBase().validate_identifier(table_name,verbose_name)
                 Model.dataBase().execute_noParams(
                    'alter table',
                    [ f'{table_name}', f'DROP COLUMN {verbose_name} ']
                )
                #  print(f'column is deleted {verbose_name}')
                 
            def rename_column(self, old_name,verbose_name,table_name =None):
                 """Rename column in table"""
                #  Model.dataBase().validate_identifier(table_name,verbose_name)
                #  Model.dataBase().execute_noParams(
                #     'alter table',
                #     [ f'{table_name}', f'ADD COLUMN {verbose_name} ']
                # ) 
                #  print(f'update {verbose_name}')

            def __repr__(self) -> str:
                k_v= [f'{k} = {v!r}'if v else'\b' for k, v in vars(self).items() if k!='field_type' ]
                return f'Model.Fields.{self.__class__.__name__}({','.join(k_v)})'     
           
            def __eq__(self, other):
                if isinstance(other, Model.Fields.BaseField):
                    return self.verbose_name == other.verbose_name
                return False
            
        class TextField(BaseField):
            """TextField to add in database as column"""
            def __init__(self,verbose_name: str):
                super().__init__(verbose_name)
                self.field_type = 'TEXT'

        class IntField(BaseField):
            """IntField to add in database as column"""
            def __init__(self,verbose_name: str):
                super().__init__(verbose_name)
                self.field_type = 'INTEGER'

        class DecimalField(BaseField):
            """DecimalField to add in database as column"""
            def __init__(self,verbose_name: str):
                super().__init__(verbose_name)
                self.field_type = 'REAL'
        
        class DateTimeField(BaseField):
            """DateTimeField to add in database as column"""
            def __init__(self,verbose_name: str):
                super().__init__(verbose_name)
                self.field_type = 'NUMERIC'
        
        class BinaryField(BaseField):
            """BinaryField to add in database as column"""
            def __init__(self,verbose_name: str):
                super().__init__(verbose_name)
                self.field_type = 'BLOB'
    
    
