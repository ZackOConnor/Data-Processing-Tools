import os
import re
import pandas as pd 
import pyodbc as db
import datetime
import time

#Quick over view, the code will through excel files and pull out needed columns of information. 
#The code can deal with changing column names and placment, empty rows, and messy headsers. 
#It uses a dict to how possiable column names, a dict to hold the place of each col with in each file
#Custom data cleaning process are layed out in comments

class Carrier():

    def __init__(self, carrier_file_path):
        self.carrier_file_path = carrier_file_path
        self.carrier = self.carrier_file_path.split("\\")[(len(self.carrier_file_path.split("\\"))-1)]
        self.column_name_dict = {
            "" : [],
            "" : [],
            "" : [],
            "" : [],
            "" : [],
            "" : []
        } #Dict to hold the columns(Keys) and possiable names(Values which are Lists)  

    def import_files(self, excel_sheet):
        import_list = os.listdir(self.carrier_file_path)
        for file in import_list:
            if file.split(".")[len(file.split("."))-1] != "xlsx":
                continue
        
            try:
                import_data = pd.read_excel(self.carrier_file_path + "\\" + file, sheet_name = excel_sheet)
            except:
                try:
                    import_data = pd.read_excel(self.carrier_file_path + "\\" + file, sheet_name = "Sheet1")
                except:
                    try:
                       import_data = pd.read_excel(self.carrier_file_path + "\\" + file) 
                    except:
                        print("Incorrect Sheet Name: ", file)
                        #These try excepts try and deal with changing sheet names
                        
            import_dict = {
                "" : "",
                "" : "", 
                "" : ""
                #"pro#" : "", Example of a string col
                #"cost" : 0, Example of a number col
            }
            # create the dict to hold the cols you will need for the current file being worked on
            
            import_data_list = list(import_data)
            for col in import_data_list: 
                for item, value in self.column_name_dict.items():
                    if col in value:
                        import_dict[item] = col
            #the logic above is what handles the changing col names and positions
            
            row_counter = 1
            for index,row in import_data.iterrows():
                sql_import_list = [row[import_dict[""]],row[import_dict[""]]]#build your sql import list

                #if type(sql_import_list[2]) is not str:
                    #try:
                        #sql_import_list[2] = sql_import_list[2].strftime('%m/%d/%Y')
                    #except:
                        #pass
                    #To deal with date times/time stamps you want as string formated as mm/dd/yy

                #if type(sql_import_list[4]) is str:
                    #sql_import_list[4] = re.sub("[^0-9^.]", "", sql_import_list[4])
                    #To strip all non numbers out of a col

                conn = db.connect('')#imput ODB connection
                curs = conn.cursor()
                try:
                    curs.execute("insert into Freight ( ) values ()", sql_import_list)# Fill in your SQL statment
                except:
                    pass#Added to handle bad imput lines and repated pks
                curs.commit()
                curs.close()
                row_counter = row_counter + 1
                if row_counter > 2000:
                    break #sometimes excel files will run until the row max row limit is reached, this stop the files after
                    #a certine number of rows(2000) change as needed
