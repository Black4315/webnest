import os
import sys
import re
import inspect
import black
import importlib
from webnest.db.databaseHandler import Model
from webnest.db.databaseHandler import dataBase
from webnest.state_colors import *
from pathlib import Path
import models as models
############pack modules
from settings import APP_NAME


def remove_duplicates(input_list):
    """Remove duplicates from list"""
    return list(dict.fromkeys(input_list))

def line_info_valid(iden):
    """Validate info of model in trek file and fetch it"""
    return re.search(r'\s*info\s*=\s*\[\s*(?:.|\s)*?\s*\]\s*', iden).group().strip()

def ask(ask,funcY,funcN):
            """Change detectors ask message"""
            inp = input(ask)
            while inp not in ['y','n']:
                inp = input('Please answer (y/n): ')
            else:
                if inp == 'y':funcY()
                elif inp == 'n':funcN()

################################################################# All classes
class Trek:
    initial = False

    depth =[tuple]

    info =[]

    processes=[]


class AddField:
    def __init__(self,model_name:str,field_name:str,field:...):
        self.model_name = model_name,
        self.field_name = field_name,
        self.field = field,

    def do(self,model_name):
        verbose_name = self.field[0].verbose_name
        field_type = self.field[0].field_type
        self.field[0].add_column(model_name,verbose_name,field_type)

class RenameField:
    def __init__(self,model_name:str,old_name:str,new_name:str):
        self.model_name = model_name,
        self.old_name = old_name,
        self.new_name = new_name,

    def do(self,model_name):
        # print(model_name)
        pass
        
class AlterField:
     def __init__(self,model_name:str,name:str,field_info:...):
        self.model_name = model_name,
        self.name = name,
        self.field_info = field_info

class DeleteField:
    def __init__(self,model_name:str,name:str,field:...):
        self.model_name = model_name,
        self.name = name,
        self.field = field,
        
    def do(self,model_name):
        verbose_name = self.field[0].verbose_name
        self.field[0].delete_column(model_name,verbose_name) 

class CreateModel:
    def __init__(self,model_name : str , fields = None) :
        self.model_name = model_name
        self.fields = fields
    
    def do(self,model_name):
        Model.__create_table__(model_name)
        model = getattr(models,model_name)

        for field in model._model_attrs[1].values():
            verbose_name = field.verbose_name
            field_type = field.field_type
            field.add_column(model_name,verbose_name,field_type)


class RenameModel:
 
    def __init__(self,old_name:str,new_name:str):
       self.old_name = old_name,
       self.new_name = new_name,

    def do(self,model_name):
        dataBase().execute(f'ALTER TABLE {self.old_name[0]} RENAME TO {model_name}')
     
class DeleteModel:
    def __init__(self,model_name:str):
       self.model_name = model_name,
    
    def do(self,model_name):
        dataBase().execute_noParams('drop table',model_name)

################################################################# All classes

class Handel_treks:
        
    def __init__(self) :
        from webnest.path import add_path
        import models as models
        self.members = inspect.getmembers(models,inspect.isclass)
        self.trks_file = add_path('treks')
        if not os.path.isdir('treks'):
            Path('treks/__init__.py').parent.mkdir(parents=True, exist_ok=True)
            Path('treks/__init__.py').touch()

        self.all_trk_file =[ trk for trk in os.listdir(self.trks_file) if trk !='__init__.py' and'isdeleted' not in trk and trk.endswith('.py')]
        self.change_detector = []
        self.init = False
        self.allInit = []
        self.depth =()
        self.info = []
        self.processes = 'processes=[]'
        self.all_processes=[]
        self.action=None
        self.delete = []
        self.model_renamed = False
        self.compare_modelWithtrks=remove_duplicates([(m[1].__model_name__) for s in self.all_trk_file  for m in self.members if m[1].__model_name__  if m[1].__model_name__ in s ])
        self.trkF_simplified = remove_duplicates([f[:f.find('_')] for f in self.all_trk_file ])
        self.seen = set()

    # FUNCTIONS
    def content(self):
           return black.format_str("from webnest.db.databaseHandler import Model\nfrom webnest.db import treks\n\n"+"class Trek(treks.Trek):\n "+f"   initial = {self.init}\n"+ f"    depth =[{self.depth}]\n"+f"    info =[{self.info}]\n"+f"    {self.processes}\n", mode=black.FileMode())
    
    def make_dir_gl(self,content = None,model_name = None):
        """Make file for model treks """
        file_name = None
        with open(f'{self.trks_file}/{model_name}_{self.action}.py','w') as file:
            file.write(content or self.content())  

    def file_paths(self,file_name):
        """treks/file path"""
        return f'{self.trks_file}/{file_name}'
    
    def last_filename_trekFile(self,model_name):
        return f'{model_name}_recentUpd.py' if os.path.isfile(self.file_paths(f'{model_name}_recentUpd.py')) else f'{model_name}_initial.py'
    
    def trekking_message(self,trk_file_path,name=APP_NAME):
        return f"{GREEN}Treks for '{name}':{WHITE} {trk_file_path}\n    "
    # FUNCTIONS 
    
    class delete_trks_file:
            """Delete treks file that deleted in model file"""
            def __init__(self,base) -> None:
                self.base = base

            def delete_detector(self):
                # if self.base.model_renamed==False and self.base.model_renamed!={}:
                if not self.base.model_renamed:
                    for trk in self.base.trkF_simplified:
                        if trk not in self.base.compare_modelWithtrks:
                            self.base.delete.append(trk)
                            if trk not in self.base.seen:
                                print(f'{self.base.trekking_message(self.base.file_paths(f'{trk}_isdeleted.py'))}- Delete model {RED}{trk}{WHITE}')
                                self.base.seen.add(trk)
            
            def deleting(self):
                if self.base.delete!= False:
                    for to_delete in self.base.delete:
                        file_path = self.base.file_paths(self.base.last_filename_trekFile(to_delete))
                        if os.path.isfile(file_path):
                            trks_to_delete = [t for t in self.base.all_trk_file if to_delete in t]
                            with open(file_path,'r')as file:
                                line = line_info_valid(file.read())
                                if line: info = eval(line[line.rfind('['):])[0]
                            self.base.info = f'{info}'
                            self.base.action= 'isdeleted'
                            self.base.processes=f"processes = [treks.DeleteModel(model_name={repr(to_delete)})]"
                            self.base.all_processes.append({'model_name':to_delete,'process':self.base.processes})
                            
                            self.base.make_dir_gl(model_name = to_delete)
                            for trk in trks_to_delete:
                                try:
                                    os.remove(self.base.file_paths(trk))
                                except:
                                    continue
              
    class make_trks_files:
        """Handel most of treks histroy and save it in file"""
        def __init__(self,base) -> None:
            self.base = base 
            self.make_trks_file()

        def make_trks_file(self):
            for member in self.base.members:
                the_class = member[1]
                if the_class.__model_name__:
                    model_name = the_class.__model_name__
                    models_reg = the_class._models_registry
                    attrs = the_class._model_attrs
                    fields = attrs[1]
                    self.base.info = attrs

                # FUNCTIONS
                    
                    def create_model(trk_file_path=None):
                            """Content and Message confirms creating model"""               
                            create_mess = f"{self.base.trekking_message(trk_file_path)}- Create model {CYAN}{model_name.capitalize()}{WHITE}"      
                            create_model = f'processes=[treks.CreateModel(\nmodel_name ="{attrs[0]}",\nfields ={[(k,v) for k,v in fields.items() if k != '_model_attrs'] }\n)]'
                            return {'create_mess':create_mess,'create_model':create_model}
                    
                    def rename_model(old_name,new_name)->str:
                        return f'processes=[treks.RenameModel(old_name={repr(old_name)},new_name={repr(new_name)})]'
                    
                    def create_field(name,field:dict=None):
                        """message of creating field"""   
                        create_field = f'processes=[treks.AddField(model_name="{attrs[0]}",field = {field})]'            
                        field_mess = f"{"\n".join([f'- {CYAN}Add {WHITE}field {name}'])}"
                        return {'field_mess':field_mess,'create_field':create_field}
                                
                    def make_dir(content = None,model_name = model_name):
                        return self.base.make_dir_gl(content=content,model_name=model_name)
                # FUNCTIONS

                    def main(): 
                        def change_detector(isfield: bool = None):
                            """Detect changes of models `info` in models.py and trek the updates to trekkings folder."""
                        #model_changes
                            def model_changes():
                                """Check any chenges in model rename or .. nothing XD, it rename only. """
                                # rename model detector
                                trks = [[f for f in self.base.all_trk_file if name in f] for name in self.base.trkF_simplified]
                                for t in trks:
                                    file_name = t[-1]
                                    if os.path.isfile(self.base.file_paths(file_name)):
                                        with open(self.base.file_paths(file_name),'r')  as file  :
                                            line = line_info_valid(file.read())
                                            if line:
                                                info = eval(line[line.rfind('['):])[0]
                                                if not os.path.isfile(self.base.file_paths(f'{attrs[0]}_initial.py')) and info[0]!=attrs[0] and info[1]==attrs[1]: 
                                                    def renameY():
                                                        print(f'- {YELLOW}Rename{WHITE} model from {info[0]} to {attrs[0]}')    
                                                        self.base.model_renamed = {'old':f'{info[0]}','new':f'{attrs[0]}'}
                                                    def renameN():self.base.model_renamed = {}
                                                    try:
                                                        ask(f'Did you change model {info[0]} to {attrs[0]} (y/n): ',renameY,renameN)
                                                    except KeyboardInterrupt as e:
                                                        raise KeyboardInterrupt(
                                                            'Something happened i dont know, But i think '
                                                            'you pressed CTRL-C or CTRL-BREAK right ?'
                                                        ) from e #logging    
                                                
                                # rename model detector
                                
                        #model_changes
                            def field_changes():   
                                """Check any changes in fieldes add,rename,alter,delete""" 
                                file_name = self.base.last_filename_trekFile(model_name) 
                                initORrec = 'init' if file_name== f'{model_name}_initial.py'else'recent'
                                local_change_detector = False
                                file = self.base.file_paths(file_name)
                                
                                if os.path.isfile(file):
                                    with open(file,'r') as file :
                                        line = line_info_valid(file.read())
                                        
                                        if line:
                                            info = eval(line[line.rfind('['):])[0]
                                            
                                            if not self.base.init and not self.base.model_renamed:
                                                if info!=attrs: # change detected
                                            
                                            ######### change detected        
                                            
                                                    if info[0]==attrs[0]: # check that change is in field not model name
                                                        local_change_detector = True
                                                        self.base.change_detector.append(True)
                                                        all_fields_attr = attrs[1]
                                                        all_fields_info = info[1]
                                                        procesess='processes=['
                                                        print(f"{self.base.trekking_message(f'treks/{info[0]}_recentUpd.py')}"+'\b'*4,end='')
                                                        add_field_process =  "f'treks.AddField(model_name= {repr(attrs[0])},field_name = {repr(kA)} , field = {vA}),'"
                                                        
                                                        for kA,vA in all_fields_attr.items():
                                                            renamed = False
                                                            for kI,vI in all_fields_info.items():
                                                                if kA!=kI and vA==vI :
                                                                    """Rename field probability."""
                                                                    renamed =True
                                                                    procesess += f'treks.RenameField(model_name="{attrs[0]}",old_name = {repr(kI)},new_name = {repr(kA)}),'
                                                                    print(' '*4+f'- {YELLOW}Rename{WHITE} field {kI} to {kA}')
                                                                 
                                                                elif kA==kI and vA!=vI:
                                                                    """Alter field probability."""
                                                                    procesess += f'treks.AlterField(model_name="{attrs[0]}",name = {repr(kI)},field_info = {repr(vA)}),'
                                                                    print(' '*4+f'- {YELLOW}Alter{WHITE} field {kI}')
                                                            
                                                            if kA not in all_fields_info.keys() and not renamed: #and vA not in all_fields_info.values():
                                                                    """Add field probability."""
                                                                    procesess += eval(add_field_process)
                                                                    print(' '*4+f"- {CYAN}Add {WHITE}field {kA}")
    
                                                        #delete
                                                        for kI,vI in all_fields_info.items():    
                                                            if kI not in all_fields_attr.keys() and vI not in all_fields_attr.values():
                                                                """Delete field probability"""
                                                                procesess += f'treks.DeleteField(model_name="{attrs[0]}",name = {repr(kI)},field={vI})'
                                                                print(' '*4+f'- {RED}Delete{WHITE} field {kI}')        

                                                        self.base.processes = procesess+']'
                                                        self.base.all_processes.append({'model_name':model_name,'process':self.base.processes})

                                            ######### change detected          
                                                else: # no change detected
                                                    local_change_detector = False
                                                    self.base.change_detector.append(False)
                                                return [initORrec,local_change_detector]
                                                
                            if not isfield: return model_changes()
                            return field_changes()

                    # treks vars    
                        change_detector() # detect if model is renamed or deleted befor make trekkings
                        if  not self.base.model_renamed and not [trk for trk in self.base.all_trk_file if f'{model_name}_' in trk ]:
                            self.base.init = True 
                            self.base.allInit.append(True)
                        else: self.base.init =False
                        if self.base.init: self.base.action = 'initial'
                        else : self.base.action = 'recentUpd'
                        model_class = {'create_model': create_model()['create_model'],
                            'rename_model':rename_model
                        }
                    # treks vars
                    #handle treks dir
                        def init():
                            """Add initial trek"""
                            if self.base.action == 'initial' :
                                self.base.processes = model_class['create_model']
                                self.base.all_processes.append({'model_name':model_name,'process':self.base.processes})

                                make_dir()
                                print(create_model(self.base.file_paths(f'{model_name}_initial.py'))['create_mess']) # create message

                        def recent_old():
                            """Add and Update recent_old trek"""
                            def upd_rec_old():
                                if os.path.isfile(self.base.file_paths(f'{model_name}_recentUpd.py')):
                                    read = open(self.base.file_paths(f'{model_name}_recentUpd.py'),'r').read()
                                    self.base.action = 'oldUpd'
                                    make_dir(content=read)   
                                    self.base.action = 'recentUpd'
                                    make_dir()

                            field_detector = change_detector(isfield=True)
                            if field_detector and field_detector[1]: 
                                    if field_detector[0]=='init' and self.base.action == 'recentUpd':
                                        make_dir()
                                        self.base.action = 'oldUpd'
                                        make_dir()
                                        
                                    elif field_detector[0]=='recent':
                                        upd_rec_old()
                                        

                            if self.base.model_renamed:
                                oldName:str = self.base.model_renamed['old']
                                newName:str = self.base.model_renamed['new']
                                trk_actions = [f[f.find('_'):] for f in self.base.all_trk_file if oldName in f]
                                self.base.processes = model_class['rename_model'](oldName,newName)
                                self.base.all_processes.append({'model_name':model_name,'process':self.base.processes})

                                if not os.path.isfile(self.base.file_paths(oldName+'_recentUpd.py')): 
                                    make_dir()
                                    self.base.action = 'oldUpd'
                                    make_dir()
                                
                                for tA in trk_actions:
                                    os.rename(self.base.file_paths(oldName+tA),self.base.file_paths(newName+tA))
                                
                                # if os.path.isfile(self.base.file_paths(oldName+'_renamed.py')):
                                #     os.remove(self.base.file_paths(oldName+'_renamed.py'))
                                # self.base.action = 'renamed'
                                # make_dir()
                                upd_rec_old()
                
                        init()
                        recent_old() 
                    #handle trekking dir
                    main()
    

    def make_delete_trks(self):
    
        make_trk= self.make_trks_files(self)
        delete= self.delete_trks_file(self)
        delete.delete_detector()
        delete.deleting()
        database = dataBase()

        if True not in self.change_detector and True not in self.allInit and not self.model_renamed and not self.delete:
            print(f'{CYAN}Render treks:\n{BLACK}  No change detected.{WHITE}')
        else:
            
            database.execute('CREATE TABLE if not exists treks (id INTEGER PRIMARY KEY AUTOINCREMENT , model_name TEXT , process TEXT)')
            if self.all_processes:
                for process in self.all_processes:
                    model_name = process['model_name'].capitalize()
                    processes = process['process'][process['process'].find('['):].replace('treks.','')
                    database.execute('INSERT INTO treks (model_name,process) VALUES (?,?)',(model_name,processes))
                   
    
    def trek(self):
        """trek the changes detected in models to data base (sqlite3)"""
        database = dataBase()
        database.execute('SELECT model_name,process from treks')
        treks = database.fetchall()

        if treks:
            for trek in treks:
                model_name = trek[0]

                if model_name:
                    process = eval(trek[1])
                    noDelete = False
                    noDeleteField= False

                    for cls in process:
                        cls_name =cls.__class__.__name__ 
                        args = [model_name]

                        if cls_name != 'DeleteModel':

                            if cls_name== 'DeleteField':
                                if cls.name[0] not in getattr(models,model_name)._model_attrs[1].keys():
                                    args = [model_name]
                                else: 
                                    noDeleteField = True

                            if not noDeleteField:
                                cls.do(*args)

                        else:
                            if os.path.isfile(self.file_paths(f'{model_name.lower()}_isdeleted.py')) and not os.path.isfile(self.file_paths(f'{model_name.lower()}_initial.py')) :
                                cls.do(model_name,)

                            else: 
                                noDelete = True

                    database.execute('DELETE FROM treks')

            if not noDelete:
                print(f'\n{CYAN}Applying for treks:\n{GREEN}  Trek has been successfuly done.{WHITE}')

        else:
            print(f'{CYAN}Applying for treks:\n{BLACK}  No treks to apply.')
            print(F'{YELLOW}you have to run command `python handle.py rendertreks` before{WHITE}')    


