'''
File: coffee_break.py (originally project.py)
---------------------------------------------
This program is for promoting internal communication of organizations.
It randomly creates groups of 4, giving group ID so that the groups can
use it as Zoom ID directly if they would like.
The program shows the group members' name and employee pictures
when the user inputs their employee number.
'''
import pandas as pd
import random
from simpleimage import SimpleImage
import tkinter as tk
import tkinter.font as font
import tkinter.ttk as ttk
from tkinter import StringVar
from PIL import ImageTk
from PIL import Image
import webbrowser
import datetime

STANDARD_TIME = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))) #offset-aware
TODAY = datetime.datetime.now() #offset-naive

def main():
    img = SimpleImage("intro.png")
    img.show()
    edata = pd.read_excel('employees_database.xlsx')
    signup_dict = edata.set_index('employee number')['name'].to_dict()
    picture_dict = edata.set_index('employee number')['picture'].to_dict()
    num_list = edata['employee number'].unique()
    group_names = create_group_names(num_list)
    same_group = create_group(edata)
    final_group = assign_members_group(group_names, same_group)
    while True:
        user_number = user_input_popup()
        if user_number == "":
            break
        user_number = int(user_number)
        print("Group names: ")
        print(group_names)
        print("Assign employees in groups of 4: ")
        print(same_group) #works
        print("All groups: ")
        print(final_group) #works
        your_group = search_group(user_number, final_group)
        show_group(your_group, signup_dict, picture_dict)
        print("You are in Group " + str(your_group[0]) + ":) Have fun with " + signup_dict[your_group[1]] + ", "
              + signup_dict[your_group[2]] + " and " + signup_dict[your_group[3]] + "!")
    img_gd = SimpleImage("GoodDay.jpg")
    img_gd.show()

def show_group(your_group, signup_dict, picture_dict):
    popup = tk.Tk()
    popup.geometry('1000x700')
    myfont = font.Font(family='Calibri', size=40)
    message1 = tk.Label(text="You are in Group " + str(your_group[0]) + " :)\nHave fun with ",
                       width=60, height=3)
    message1['font'] = myfont
    message1.pack()

    load = Image.open(picture_dict[your_group[1]])
    render = ImageTk.PhotoImage(load)
    img = tk.Label(image=render)
    img.image = render
    img.place(x=120, y=200)

    name1 = tk.Label(text=signup_dict[your_group[1]])
    name1['font'] = myfont
    name1.place(x=120, y=355)

    load = Image.open(picture_dict[your_group[2]])
    render = ImageTk.PhotoImage(load)
    img = tk.Label(image=render)
    img.image = render
    img.place(x=420, y=200)

    name2 = tk.Label(text=signup_dict[your_group[2]])
    name2['font'] = myfont
    name2.place(x=420, y=355)

    load = Image.open(picture_dict[your_group[3]])
    render = ImageTk.PhotoImage(load)
    img = tk.Label(image=render)
    img.image = render
    img.place(x=720, y=200)

    name3 = tk.Label(text=signup_dict[your_group[3]])
    name3['font'] = myfont
    name3.place(x=720, y=355)

    new = 1
    url = "https://zoom.us/"
    def openweb():
        webbrowser.open(url, new=new)
    Btn = tk.Button(popup, text="Open Zoom", command=openweb, width=10, height=1, fg="white", bg="#2D8CFF", bd=5)
    Btn['font'] = myfont
    Btn.place(x=360, y=500)


    popup.mainloop()

def user_input_popup():
    #global user_number
    popup = tk.Tk()
    #popup.withdraw()
    # Screen size
    popup.geometry('1000x700')
    myFont = font.Font(family='Calibri', size=13)
    myFont1 = font.Font(family='Calibri', size=24)
    GreetFont = font.Font(family='Calibri', size=25)
    Q1Font = font.Font(family='Calibri', size=23)

    Greeting = tk.Frame()
    greeting = tk.Label(master=Greeting,
                        text="Would you like to have coffee break with your colleagues today at 3pm?",
                        width=60, height=3)
    # apply font to the button label
    greeting['font'] = GreetFont
    greeting.pack()
    Greeting.pack()

    Button = tk.Frame()
    '''button1 = tk.Button(master=Button, text="Why not!", width=10, height=2, bg="#FFC0CB", bd=5)
    button1['font'] = myFont'''
    button2 = tk.Button(master=Button, text="Nah I'm good today", width=18, height=1, bg="#E0FFFF",
                        bd=5, command=popup.destroy)
    button2['font'] = myFont
    #button1.pack(side="left", padx=10)
    button2.pack(side="right", padx=10)
    Button.pack()

    q1 = tk.Label(text="What's your employee number?", width=50, height=3)
    q1['font'] = Q1Font
    q1.pack()

    var = StringVar()
    entry = tk.Entry(textvariable=var, width=27)
    #user_number = entry.get()
    entry['font'] = myFont
    entry.pack()

    def callback():
        user_number = var.get()
        popup.destroy()
        '''if user_number == "":
            return ""'''
        '''print(user_number)
        print(entry.get())'''
        return user_number

    button3 = tk.Button(text="Find my group!", width=15, height=2, bg="#FAFF8A",
                        bd=5, command=callback)
    button3['font'] = myFont1
    button3.pack(pady=20)
    popup.mainloop()  # this comes at the end of the code
    return var.get()

def search_group(user_number, final_group):
    '''
    this is to figure out which group the user is in,
    and returns the group number
    :param user_number:
    :return group number that the user is belong to:
    '''
    pre_your_group = ([key for key, value in final_group.items() if user_number in value])
    pre_your_group.append(final_group[pre_your_group[0]])
    #print(pre_your_group)
    your_group = []
    for i in pre_your_group:
        if isinstance(i, list):
            your_group.extend(i)
        else:
            your_group.append(i)
    your_group.remove(user_number)
    return your_group

def assign_members_group(group_names, same_group):
    #merge 2 lists of group_names and same_group to make a dictionary
    return dict(zip(group_names, same_group))


def create_group(edata):
    '''
    randomly line up employee numbers, and
    create groups of 4, based on the number of employees
    :param edata:
    :return same_group:
    '''
    num_count = 0
    same_group = []
    num_list = edata['employee number'].unique()
    while num_count < len(num_list):
        employee_num = random.choice(num_list)
        if employee_num not in same_group: #check if the employee number is duplicably picked
            same_group.append(employee_num)
            num_count += 1
    return [same_group[i:i + 4] for i in range(0, len(same_group), 4)] #split the list into groups of 4
    #print(same_group)
    '''
    check if the number is duplicated
    print(len(same_group))
    print(Counter(same_group).keys())
    print(Counter(same_group).values())
    '''

def create_group_names(num_list):
    group_names = []
    for num in range(len(num_list) // 4):
        num = random.randint(11111111111, 100000000000)
        group_names.append(num)
    return group_names




if __name__ == '__main__':
    main()