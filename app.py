from tkinter import messagebox
from tkinter.filedialog import askopenfilenames, askdirectory
from modules import pdfTableExtract
import gc
import pandas as pd
# Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing


'''
Set path to data directory here
'''
# DIR_PATH = askdirectory() # show an "Open" dialog box and return the path to the directory where pdf files are stored
# FILES = os.listdir(DIR_PATH)
# FILES = askopenfiles()

if __name__ == "__main__":
    FILES = askopenfilenames()
    tables = pdfTableExtract(FILES)
    data = tables.extract_main()
    print(f"\n{'*'*10} {data.shape[0]} rows extracted {'*'*10}\n")
    print(f"\n{'*'*10} 10 samples {'*'*10}\n")
    print(data[data.columns[:8]].sample(10), '\n')
    save = input('Save extracted data (y/n)? ')
    if 'y' in save.lower():
        save_path = askdirectory(title="Choose folder to save")
        data.to_csv(f'{save_path}/pdf_table_extracts.csv')
        messagebox.showinfo(title="", message="Table data saved")
    else:
        pass
    print('Complete and exiting program')
    del FILES, tables, data
    gc.collect()

    
