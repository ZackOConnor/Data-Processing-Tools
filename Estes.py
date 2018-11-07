import os
import re
import pandas as pd 
import pyodbc as db
import datetime
import time

conn = db.connect('DSN=DataHouse;UID=PERIO\\zoconnor;PWD=Zack1325!')
curs = conn.cursor()
curs.execute("use Syspro")
curs.execute("delete from Freight")
curs.commit()
curs.close()

class Carrier():

    def __init__(self, carrier_file_path):
        self.carrier_file_path = carrier_file_path
        self.carrier = self.carrier_file_path.split("\\")[(len(self.carrier_file_path.split("\\"))-1)]
        self.column_name_dict = {
            "cus_name" : ["Name", "Consignee Name","Consignee","Customer Name","Customer","CONSIGNEE NAME","CONSIGNEE","CUSTOMER NAME","CUSTOMER", " Cons Name", "Cons Name", "CUSTOMER ", "Customer "],
            "dis_center_state" : ["state","STATE","ST", "st", "State","Consignee State", "Cons State", " Cons State", " Cons St", "St"],
            "ship_date" : ["Document Date" ,"Ship date", "Shipment Date", "SHIPDATE","Ship Date", "SHIP DATE", "PICKUPDATE", "Pick Up Date", "PICKUP", "Pick Up", "Pickup Date", "Actual Pickup Date", "SHIPDATE", "SHIP DATE ", "Pick Up ", " Pick Up", " Pickup Date", " Ship Date", "Pick up date "],
            "pro#" : ["Assignment", "Bill Number", "Invoice Number", "PRONO","Pro Number", " Pro Number", "Pro #", "Pro#", "PRO#", "PRO #", "PRO Number", "OD Pro#", "Prono", "PRO", "PRO ", " Pro Nbr"],
            "cost" : ["Balance Due" ,"Amount DC", "Amount Due"," Invoice Amt", "Gross Amount","Cost","Total", "Charges", "Cost ", "COST ", "COST", "Costs", "Total Cost", "Total Charge (Net)"],
            "accessorials" : ["accessorials", "Accessorials", "Accessorial", "Acc.", "Accessorial Charge", " TTL Acc Chgs", "Acc Chgs", "TTL Acc Chgs"]
        }

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
            import_dict = {
                "cus_name" : "",
                "dis_center_state" : "", 
                "ship_date" : "",
                "carrier" : self.carrier,
                "pro#" : "",
                "cost" : 0,
                "accessorials" : 0
            }
            import_data_list = list(import_data)
            for col in import_data_list: 
                for item, value in self.column_name_dict.items():
                    if col in value:
                        import_dict[item] = col
            row_counter = 1
            for index,row in import_data.iterrows():
                if self.carrier == "NCS":
                    if import_dict["accessorials"] != 0:
                        sql_import_list = ["Walgreens","NA",row[import_dict["ship_date"]],import_dict["carrier"],row[import_dict["pro#"]],row[import_dict["cost"]],row[import_dict["accessorials"]]]
                    else:
                        sql_import_list = ["Walgreens","NA",row[import_dict["ship_date"]],import_dict["carrier"],row[import_dict["pro#"]],row[import_dict["cost"]],0]

                else:
                    if import_dict["accessorials"] != 0:
                        sql_import_list = [row[import_dict["cus_name"]],row[import_dict["dis_center_state"]],row[import_dict["ship_date"]],import_dict["carrier"],row[import_dict["pro#"]],row[import_dict["cost"]],row[import_dict["accessorials"]]]
                    else:
                        sql_import_list = [row[import_dict["cus_name"]],row[import_dict["dis_center_state"]],row[import_dict["ship_date"]],import_dict["carrier"],row[import_dict["pro#"]],row[import_dict["cost"]],0]

                if type(sql_import_list[2]) is not str:
                    try:
                        sql_import_list[2] = sql_import_list[2].strftime('%m/%d/%Y')
                    except:
                        pass

                if type(sql_import_list[4]) is str:
                    sql_import_list[4] = re.sub("[^0-9^.]", "", sql_import_list[4])

                conn = db.connect('DSN=DataHouse;UID=PERIO\\zoconnor;PWD=Zack1325!')
                curs = conn.cursor()
                curs.execute("use Syspro")

                try:
                    curs.execute("insert into Freight ( cus_name, dis_center_state, ship_date, carrier, pro#, cost, accessorials) values (?,?,?,?,?,?,?)", sql_import_list)
                except:
                    pass

                curs.commit()
                curs.close()
                row_counter = row_counter + 1
                if row_counter > 2000:
                    break 

XPO_Logisctics = Carrier("C:\\Users\\zoconnor\\Desktop\\Freight Payment\\XPO Logistics")
XPO_Logisctics.import_files("Orders")
NCS = Carrier("C:\\Users\\zoconnor\\Desktop\\Freight Payment\\NCS")
NCS.import_files("Orders")
YRC_Frieght = Carrier("C:\\Users\\zoconnor\\Desktop\\Freight Payment\\YRC Freight")
YRC_Frieght.import_files("Orders")
UPS_Freight = Carrier("C:\\Users\\zoconnor\\Desktop\\Freight Payment\\UPS Freight")
UPS_Freight.import_files("Orders")
OldD = Carrier("C:\\Users\\zoconnor\\Desktop\\Freight Payment\\OldD")
OldD.import_files("Orders")
NEMF = Carrier("C:\\Users\\zoconnor\\Desktop\\Freight Payment\\NEMF")
NEMF.import_files("Orders")
Estes = Carrier("C:\\Users\\zoconnor\\Desktop\\Freight Payment\\Estes")
Estes.import_files("Orders")
FedEx = Carrier("C:\\Users\\zoconnor\\Desktop\\Freight Payment\\FedEx Freight")
FedEx.import_files("Orders")

conn = db.connect('DSN=DataHouse;UID=PERIO\\zoconnor;PWD=Zack1325!')
curs = conn.cursor()
curs.execute("use Syspro")
curs.execute("delete from Freight where [pro#] < 1")
curs.commit()
curs.close()