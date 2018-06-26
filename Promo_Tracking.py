import os
import datetime
import csv
import re

class Master_List():
    #Creates a list of pervious used emails
    def ineligible_list(self,brand,promo):
        #creates and formats a Ineligiable List file for the given brand promo combo
        self.brand = brand
        self.promo = promo
        self.file_path = '//goatee/public/Brand Management/' + self.brand + '/Promotions/' + self.promo + '/Shopify Order Export/'
        ineligible_file_path = self.file_path + 'Ineligible List'
        if os.listdir(ineligible_file_path) == []:
            with open (ineligible_file_path + '/Ineligible List.csv','w+',newline='') as csvfile:
                title = ['Email','Brand','Promo']
                csvwriter = csv.writer(csvfile, delimiter=',')
                csvwriter.writerow(title)       

    def add_email(self,email):
        #Opens the Ineligiable List and adds the lastest used Emails 
        brand = self.file_path.split('/')[5]
        promo = self.file_path.split('/')[7]
        with open(self.file_path + '/Ineligible List/Ineligible List.csv','a+',newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',')
            row = [email,brand,promo]
            csvwriter.writerow(row)

class Data_Exstract():
    #all of the data exstract methods needed
    def exstract_names(self,name):
        #splits the line and pulls out the first name, last name, and email1]
        names = name[0].split(' ')
        cleaned_names = [names[0],names[1],name[1],name[3]]
        return(cleaned_names)

    def exstract_time(self,filename):
        #splits the filename and pulls out the start and end time stamps
        filename = re.split("-|_",filename)
        Current_Time = datetime.date(int(filename[4]),int(filename[5]),int(filename[6].split('.')[0]))
        return(Current_Time)

path_Barbasol_data = "//goatee/public/Brand Management/Barbasol/Promotions/Tee Off/Shopify Order Export/Original Shopify Export for Harte Hanks"
path_Pure_Silk_data = "//goatee/public/Brand Management/Pure Silk/Promotions/TLC Marketing Promo/Shopify Order Export/Original Shopify Exports for TLC"

path_Barbasol_Clean = "//goatee/public/Brand Management/Barbasol/Promotions/Tee Off/Shopify Order Export/Scrubbed File for Harte Hanks"
path_Pure_Silk_Clean = "//goatee/public/Brand Management/Pure Silk/Promotions/TLC Marketing Promo/Shopify Order Export/Scrubbed File for TLC"

Lastest_File_Barbasol = ""
Lastest_File_Pure_Silk = ""

#Barbasol
barbasol_used_emails = Master_List()
barbasol_used_emails.ineligible_list('Barbasol','Tee Off')
Lastest_Time = datetime.date(2011,1,1)#Early Dummy Date
for filename in os.listdir(path_Barbasol_data):
    Current_Time = Data_Exstract().exstract_time(filename)
    if Lastest_Time < Current_Time:
        Lastest_Time = Current_Time
        Lastest_File = filename
     
file = open(path_Barbasol_data + '/' + Lastest_File)
Valid_Products = ['Barbasol Ultra 6 Plus Value Pack','Barbasol Shave Club Starter Kit','Barbasol Ultra 6 Plus']

Checked_Names_file = open('//goatee/public/Brand Management/Barbasol/Promotions/Tee Off/Shopify Order Export/Ineligible List/Ineligible List.csv','r')
Checked_Names = []
for line in Checked_Names_file:
    line = line.split(',')
    Checked_Names.append(line[0])
Checked_Names_file.close()

with open(path_Barbasol_Clean + '/' + 'Barbasol_' +Lastest_File, 'a+',newline='') as csvfile:
    title = ['first name','last name','address 1','address 2','city','state','zip','email address','phone number']
    csvwriter = csv.writer(csvfile, delimiter=',')
    for line in csvfile:
        if len(line) == 0:
            csvwriter.writerow(title)
            break
    for line in file:
        line = line.split(',')
        if line [2] in Valid_Products:
            names = Data_Exstract().exstract_names(line)
            if names[2] not in Checked_Names:
                Checked_Names.append(names[2])
                Formated_Line = [names[0],names[1],'','','','','',names[2],'']   
                csvwriter.writerow(Formated_Line)
                barbasol_used_emails.add_email(names[2])  

#Pure Silk
pure_silk_used_emails = Master_List()
pure_silk_used_emails.ineligible_list('Pure Silk','TLC Marketing Promo')
Lastest_Time = datetime.date(2011,1,1)#Early Dummy Date
for filename in os.listdir(path_Pure_Silk_data):
    Current_Time = Data_Exstract().exstract_time(filename)
    if Lastest_Time < Current_Time:
        Lastest_Time = Current_Time
        Lastest_File = filename

Checked_Names_file = open('//goatee/public/Brand Management/Pure Silk/Promotions/TLC Marketing Promo/Shopify Order Export/Ineligible List/Ineligible List.csv','r')
Checked_Names = []
for line in Checked_Names_file:
    line = line.split(',')
    Checked_Names.append(line[0])
Checked_Names_file.close()

file.close()        
file = open(path_Pure_Silk_data + '/' + Lastest_File)
Valid_Products = ['Pure Silk Contour 6 Value Pack','Pure SilkÂ Shave Club Starter Kit','Pure Silk Shave Club Starter Kit','Pure Silk Contour 6 Razor']

with open(path_Pure_Silk_Clean + '/' + "Pure_Silk_" + Lastest_File, 'a+',newline='') as csvfile:
    title = ['First Name','Last Name','Email Address','State']
    csvwriter = csv.writer(csvfile, delimiter=',')
    for line in csvfile:
        if len(line) == 0:
            csvwriter.writerow(title)
            break
    for line in file:
        line = line.split(',')
        if line [2] in Valid_Products:
            names = Data_Exstract().exstract_names(line)
            if names[2] not in Checked_Names:
                Checked_Names.append(names[2])
                Formated_Line = [names[0],names[1],names[2],names[3]]
                csvwriter.writerow(Formated_Line)
                pure_silk_used_emails.add_email(names[2])
file.close()
