#Owen Cody | 2018 | Bodged_Schedule_Builder_Alert_System

#Import necessary modules
import requests, os, time, smtplib

#Set a variable to see if space is found
the_ree=False

#Sets the API call frequency speed
request_frequency = 3

#The original url that I found from the network
original_url='https://schedulebuilder.umn.edu/api.php?type=sections&institution=UMNTC&campus=UMNTC&term=1193&class_nbrs=60372%2C60385%2C60386%2C60387%2C60388%2C60389%2C60390%2C60391%2C60392%2C60393%2C60394%2C60395%2C61128'

#The reverse engineered query
query_url='https://schedulebuilder.umn.edu/api.php?type=sections&institution=UMNTC&campus=UMNTC&term=1193&class_nbrs='

#The recipients that should be emailed if a space is found
recipients=[]

#The class ID's that should be checked for availability
class_nbrs=['60385','60386','60387','60388','60389','60390','60391','60392','60393','60394','60395','61128']


#My general use class for quick coding
class general_uses:
    def get_local_file_path(self,fPath):
        full_path = os.getcwd()+u"/"+fPath
        return full_path
    
    def text_file_read(self,inputFn):
        try:
            with open(inputFn) as inputFileHandle:
                return inputFileHandle.read()
        except IOError:
            return u'A problem has been encountered as your file doesnt exist!'
    
    def text_file_write(self,textFn,input_text):
        try:
            with open(textFn, "w") as text_file:
                text_file.write(input_text)
        except IOError:
            return u'A problem has been encountered as your file doesnt exist!'


#A function to organize to properly organize our API call
def initialize_args(query,class_n):
    args=str(class_n[0])
    for i in range(1,len(class_n)):
        args=str(args+"%2C"+str(class_n[i]))
    final_url=query_url+args
    return final_url

#A function to allow our program to annoy us with emails if it finds an open class slot in our list
def send_mail(recipients,message):
    gu=general_uses()
    psword=gu.text_file_read(gu.get_local_file_path("sb2_pwd.txt"))
    usrname=gc.text_file_read(gc.get_local_file_path("gmail_usr.txt"))
    recipients.append(list(gc.text_file_read(gc.get_local_file_path("recipients.txt"))))
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(usrname, psword)
    for i in range(len(recipients)):        
        server.sendmail(
            str(usrname), 
            str(recipients[i]), 
            message)
        time.sleep(0.5)
    server.quit()



#Get the number of times we have queried the server
tc=general_uses()
fntc=tc.get_local_file_path("num_times_checked.txt")
ntc=int(tc.text_file_read(fntc))

#Run until a space is found
while(the_ree == False):

    #Attempt to call requests and catch if there is a connection error.
    try:
        #Use requests to call the schedule builder REST API with our classes as arguments. Also, format in json.
        sb_raw = requests.get(initialize_args(query_url,class_nbrs)).json()
        #Increase the times checked count
        ntc+=1
        tc.text_file_write(fntc,str(ntc))

        #Cursor through the response from the server
        for i in range(len(sb_raw)):

            #Find the number of open seats
            open_seats=int(sb_raw[i][u'capacity']-sb_raw[i][u'enrolled_total'])

            #If an open seat is found alert the runner of the program
            if(open_seats > 0):
                for n in range(100):
                    print("REEEEEEEE")
                the_ree = True
                send_mail(recipients,str(sb_raw[i][u'title'])+" | NOW HAS AVAILABLE SEATS! MOVE QUICKLY!")

            #Format and print a nice little display for the console
            print(str(i)+" | "+sb_raw[i][u'title']+"\n---------------------------------------------")
            print("Instructor Name | " + str(sb_raw[i][u'meetings'][0][u'instructors'][0][u'label_name']))
            print("Total Seats | " + str(sb_raw[i][u'capacity']))
            print("Taken Seats | " + str(sb_raw[i][u'enrolled_total']))
            print("Open Seats | " + str(open_seats))
            print("Times Checked | " + str(ntc))

            #Sleep to not overload the Schedule Builder servers
            time.sleep(request_frequency)
            _=os.system('cls')
            #Seperate the query responses
            print('\n')
    except requests.ConnectionError:
        print("Please reconnect to the internet:")
        time.sleep(request_frequency)
