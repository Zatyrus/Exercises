## Dependencies
import os
import tkinter as tk
from tkinter import filedialog
from pprint import pprint, pformat

import PyPDF2 as pdf
"""
PyPDF2 is a free and open-source pure-python PDF library capable of splitting, 
merging, cropping, and transforming the pages of PDF files. It can also add custom data, 
viewing options, and passwords to PDF files. 
PyPDF2 can retrieve text and metadata from PDFs as well.
"""

## Windows Explorer Interface
class pyDialogue():
    
    @staticmethod
    def askDIR():
        root = tk.Tk()
        root.withdraw()
        root.call('wm', 'attributes', '.', '-topmost', True)
        DIR_path = filedialog.askdirectory()
        return DIR_path

    @staticmethod
    def askFILE():
        root = tk.Tk()
        root.withdraw()
        root.call('wm', 'attributes', '.', '-topmost', True)
        FILE_path = filedialog.askopenfilename()
        return FILE_path

    @staticmethod
    def askFILES():
        root = tk.Tk()
        root.withdraw()
        root.call('wm', 'attributes', '.', '-topmost', True)
        FILE_path = filedialog.askopenfilenames()
        return FILE_path
    

    def askSAVEASFILE():
        root = tk.Tk()
        root.withdraw()
        root.call('wm', 'attributes', '.', '-topmost', True)
        FILE_path = filedialog.asksaveasfilename(defaultextension="*",
                                                title="Save as...",
                                                confirmoverwrite=True,
                                                filetypes=[("PDF files", "*.pdf"),
                                                            ("Text files", "*.txt"),
                                                            ("All files", "*")])
        return FILE_path
    
class pdfInterface():
    
    path:str
    reader:pdf
    id:int
    
    def __init__(self, path:str, id:int):
        self.path = path
        self.id = id
    
        self.__post_init__()
    
    def __post_init__(self):
        self.reader = pdf.PdfReader(self.path)
        
    ## Getters
    def getNumPages(self):
        return len(self.reader.pages)
    
    def getPDFMetadata(self):
        info = self.reader.metadata
        return info
    
    def getPDFText(self):
        text = ''
        for i in range(self.getNumPages()):
            page = self.reader.pages[i]
            text += page.extract_text()
        return text
    
    def getPDFPage(self, page_number:int):
        return self.reader.pages[page_number]
    
    def getAllPDFPages(self):
        return self.reader.pages
    
    ## Viewers
    def viewPDF(self):
        os.startfile(self.path)
        
    def viewPDFPage(self, page:int):
        page = self.getPDFPage(page)
        page.extract_text()
        
    ## Writers
    ...
    
class pdfTools():
    
    __path_list:list[str]
    __files:dict[str, pdfInterface]
    __arrangement:dict[int, str]
    __verbose:bool
    
    def __init__(self, path_list:list[str] = None, verbose:bool=False):
        self.__path_list = path_list
        self.__verbose = verbose
        
        self.__post_init__()
    
    ## catch all for post init
    def __post_init__(self):
        self.__files = {path:pdfInterface(path, id) for id, path in enumerate(self.__path_list)}
        self.__arrangement = {id:path for id, path in enumerate(self.__path_list)}
        return
    
    ## classmethods
    @classmethod
    def fromDIR(cls, DIR_path:str = None, verbose:bool=False)->tuple[list[str], bool]:
        
        try:
            assert DIR_path
            assert os.path.isdir(DIR_path)
        except:
            print('Choose a directory with PDF files.')
            DIR_path = pyDialogue.askDIR()        
        
        path_list = [os.path.join(DIR_path, file) for file in os.listdir(DIR_path)]
        return cls(path_list, verbose)
    
    @classmethod
    def fromFILES(cls, FILE_path:str = None, verbose:bool=False)->tuple[list[str], bool]:
        
        try:
            assert FILE_path
            assert os.path.isfile(FILE_path)
        except:
            print('Choose a file or files.')
            FILE_path = pyDialogue.askFILES()
        
        return cls(FILE_path, verbose)
    
    
    @property
    def arrangement(self):
        return self.__arrangement
    @arrangement.setter
    def arrangement(self, new_arrangement):
        self.__arrangement = new_arrangement
        #self.__sortAranngement()
        
    @property
    def files(self):
        return self.__files
    @files.setter
    def files(self, new_files):
        self.__files = new_files
        
    @property 
    def path_list(self):
        return self.__path_list
    @path_list.setter
    def path_list(self, new_path_list):
        self.__path_list = new_path_list
    
    @property
    def verbose(self):
        return self.__verbose
    @verbose.setter
    def verbose(self, new_verbose):
        self.__verbose = new_verbose
        print(f'Verbose: {self.__verbose}')
    
    @property
    def numFiles(self):
        return len(self.__path_list)
    
        
    ## interface
    def showPDFMetadata(self):
        for path in self.path_list:
            print(self.__files[path].getPDFMetadata())
            
    def showPDFArrangement(self):
        for id in self.arrangement:
            print(f'{id}: {self.__getPathLeaf(self.__arrangement[id])}')
    
    ## change arrangement
    def __requestNewArrangement(self):
        new_arrangement = {}
        for id in self.arrangement:
            print(f'Current: {id}: {self.__getPathLeaf(self.__arrangement[id])}')
            new_id = self.__request_new_id(new_arrangement)
            new_arrangement[new_id] = self.__arrangement[id]
        self.__sortAranngement()
        return new_arrangement
    
    def __request_new_id(self, new_arrangement:dict[int, str]):
        terminate = False
        while not terminate:
            
            new_id = int(input('New ID: '))
            
            try:
                assert new_id in self.arrangement
                assert new_id not in new_arrangement
                terminate = True
            except:
                print('Invalid ID')
        return new_id
    
    # def __sortAranngement(self):
    #     temp = sorted(self.__arrangement.items(), key=lambda x: x[0])
    
    def __getPathLeaf(self, path:str):
        return path.split('/')[-1]
    
    def __showArrangement(self):
        temp = {}
        for id in self.arrangement:
            temp[id] = self.__getPathLeaf(self.__arrangement[id])
        return pprint(temp)
    
    def __confirmNewArrangement(self, new_arrangement:dict[int, str]):
        print('New Arrangement:')
        self.__showArrangement()
        confirm = input('Confirm? (y/n): ')
        return confirm
    
    def rearrange(self, new_arrangement:list[int]):
        print('Current Arrangement:')
        self.showPDFArrangement()
        
        ## check if new arrangement is valid
        try:
            assert len(new_arrangement) == len(self.__arrangement)
            assert all([id in new_arrangement for id in self.__arrangement])
            
        except AssertionError as e:
            print('Invalid arrangement')
            print('Error:', e)
            print('Exiting...')
            return False
    
        ## Rearrange
        tmp_arrangement = {id:self.__arrangement[id] for id in new_arrangement}
        
        ## Check back with user
        print('New Arrangement:')
        pprint(tmp_arrangement)
        confirm = input('Confirm? (y/n): ')
        
        if confirm == 'y':
            if self.verbose:
                print('Arrangement set')
            self.arrangement = tmp_arrangement
            return True
        elif confirm == 'n':
            if self.verbose:
                print('Arrangement not set')
            return False
        else:
            print('Invalid input')
            return False
        
    
    def setArrangement(self):
        new_arrangement = self.__requestNewArrangement()
        
        ## check if new arrangement is valid
        try:
            assert len(new_arrangement) == len(self.__arrangement)
            assert all([id in new_arrangement.keys() for id in self.__arrangement.keys()])
            assert all([path in new_arrangement.values() for path in self.__path_list])
            
        except AssertionError as e:
            print('Invalid arrangement')
            print('Error:', e)
            print('Exiting...')
            return False
            
        ## Check back with user
        confirm = self.__confirmNewArrangement(new_arrangement)
        
        if confirm == 'y':        
            self.arrangement = new_arrangement
            
            if self.verbose:
                print('Arrangement set')
                
            return True
        
        else:
            if self.verbose:
                print('Arrangement not set')
                
            return False
    
    def swap_first_last(self):
        temp = self.arrangement[0]
        self.arrangement[0] = self.arrangement[len(self.arrangement)-1]
        self.arrangement[len(self.arrangement)-1] = temp
                
        if self.verbose:
            print('First and last swapped')
            self.__showArrangement()
        
        return True
        
    ## PDF Operations
    def quickMerge(self, output:str = None):
        
        try:
            assert output
            assert output.endswith('.pdf')
            
        except:
            output = pyDialogue.askSAVEASFILE()
        
        merger = pdf.PdfMerger()
        for path in self.arrangement.values():
            merger.append(path)
            
        merger.write(output)
        merger.close()
        
        return True

        
    	