#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 16:01:47 2019

@author: erkamozturk
"""

__author__ = 'erkamozturk'

from Tkinter import *
import ttk
import xlrd
import os
import codecs
import anydbm
import pickle
from recommendations import *
import tkMessageBox


class Curriculum(Frame):

    def __init__(self, root):
        Frame.__init__(self, root)
        self.root = root
        self.tools()
        self.planning()
        self.user="ahmetozturk"

    def get_menu(self):
        self.menu =xlrd.open_workbook('Menu.xlsx')  # open the excel file
        self.sheet = self.menu.sheet_by_index(0)  # index 0 = first page
        self.list_menu = [] # container
        for row in range(1, self.sheet.nrows):  # for each row
            self.list_menu.append(self.sheet.cell(row, 0).value) # all gets full in container
        return self.list_menu  # get a list

    def tools(self):
        self.get_menu() # run it, we have list of foods in menu
        self.f1 = Frame(self.root, bg="black", width=500, height=75)  # I work with 6 frames. All separates each on frame
        self.l_ccre = Label(self.f1, fg="yellow", text="Cafe Crown Recommendation Engine - SEHIR Special Edition",
                                 font="Times 20", bg="black", width=55, height=1)
        self.f2 = Frame(self.root, width=500, height=75) # frame2
        self.l_welcome = Label(self.f2, fg="black", font="Times 13", text="Welcome!")
        self.l_please = Label(self.f2, fg="black", font="Times 13", text="Please rate entries that you have had at CC,"
                                                                         " and we will recommend you what you may like to"
                                                                         " have!")
        self.period=Label(self.f2, text="'"*320) # this is separter
        self.f3 = Frame(self.root, width=500, height=75) # frame3
        self.l_choose = Label(self.f3, fg="red", font="Times 10 bold", text="Chooese a meal:")
        self.l_enter = Label(self.f3, fg="red", font="Times 10 bold", text="Enter your rating")
        self.box_value = StringVar()  # settings of box
        self.box = ttk.Combobox(self.f3, textvariable=self.box_value, width=30)
        self.box['values'] = self.get_menu() # values are my list which I get when I start
        self.box.current(0)
        self.b_add = Button(self.f3, bg="white", fg="blue", text=5*" "+"Add"+5*" ", font="Times 10 bold", command=self.displaying)
        self.s_top = Scrollbar(self.f3) #frame3
        self.mylist = Listbox(self.f3, yscrollcommand=self.s_top.set, height=5, width=32) # this is listbox. my scrollbar work with listbpx
        self.s_top.config(command=self.mylist.yview)
        self.b_remove = Button(self.f3, bg="white", fg="red", text="Remove \n Selected", font="Times 10 bold", command=self.removing)
        self.slider = Scale(self.f3, from_=1, to=10, orient=HORIZONTAL) # this slider 1 to 10
        self.f4 = Frame(self.root, width=500, height=75) #frame4
        self.period2 = Label(self.f4, text="'"*320) # separeter
        self.l_middle = Label(self.f4, fg="black", text="Get Recommendations", font="Times 15 bold")
        self.f5 = Frame(self.root, width=500, height=75) # frame5
        self.period3 = Label(self.f5, text="'"*320) # separeter
        self.l_settings = Label(self.f5, text="Settings:", fg="red", font="Times 15 bold")
        self.text = Entry(self.f5, fg="black", textvariable=StringVar, width=2)
        self.f6 = Frame(self.root, width=500, height=75) # frame6
        self.period4 = Label(self.f6, text="'"*320) # separeter
        self.s_bot = Scrollbar(self.f6) # scrollbar for bottom
        self.leftone = Listbox(self.f6, yscrollcommand=self.s_bot.set, height=5, width=50) # listbox for result
        self.s_bot.config(command=self.leftone.yview)
        self.l_purple = Label(self.f6, text="User similars to:",font="Times 12 bold", fg="white", bg="purple")
        self.listbox_users = Listbox(self.f6, height=5, width=35) # listbox for 2. at the botom
        self.l_brown = Label(self.f6, text="User ratings(select a user on the left)",font="Times 12 bold", fg="white", bg="brown")
        self.s_bot1 = Scrollbar(self.f6)
        self.listbox_userratings = Listbox(self.f6, yscrollcommand=self.s_bot1.set, height=5, width=55) # listbox for 3. at the bottom
        self.s_bot1.config(command=self.listbox_userratings.yview)

        if os.path.exists("own_ratings.db"):
            self.ratings_foods = anydbm.open("own_ratings.db", "c")  # Is there any db(ownratings)? If there, write it
            for key in self.ratings_foods:
                self.mylist.insert(END, key + "-->" + str(pickle.loads(self.ratings_foods[key])))
        else:
            self.ratings_foods = anydbm.open("own_ratings.db", "c") # If not, create new one

    def displaying(self):
        self.mylist.delete(0, END) # delete everything, everytime when I clicked
        self.ratings_foods[self.box.get().encode('utf-8')] = pickle.dumps(self.slider.get()) # key=food name value=rating
        for key in self.ratings_foods:
            self.mylist.insert(END, key + "-->" + str(pickle.loads(self.ratings_foods[key]))) # write it on listbox

    def removing(self):
        self.selected = self.mylist.get(ACTIVE) # get from listbox which one is selected
        self.a = self.selected.index("-") # it gets x---->5. I need to x so I need to find first - from left
        self.name_removing = self.selected[:self.a]  # get the name (...) before -
        del self.ratings_foods[self.name_removing.encode('utf-8')]  # delete this key in db
        self.mylist.delete(0, END)  # clear list box
        for key in self.ratings_foods:  # write again
            self.mylist.insert(END, key + "-->" + str(pickle.loads(self.ratings_foods[key])))

    def getRec(self):
        if self.text.get() =="":
            tkMessageBox.showerror("Error", "Number of recommendations should be number, not empty.\nPlease give any number.")
        self.cc_ratings = {}  # empty dic I will fill in gettings datas given db and mine db
        self.cc_ratings["ahmetozturk"] = {}
        for i in self.ratings_foods:  # this my structure, my db
            self.cc_ratings["ahmetozturk"][i] = pickle.loads(self.ratings_foods[i]) # I put this infos in one dict
        self.given_ratings = anydbm.open("cc_ratings.db", "c") # open the given db
        for i in self.given_ratings: # same work for this I put infos in one dict
            self.cc_ratings[i] = pickle.loads(self.given_ratings[i])
        self.listbox_users.bind('<<ListboxSelect>>', self.go_right)  # when I click some row in listbox call go_right
        self.simililarties = [sim_distance, sim_pearson, sim_distance]  # I gave the valus of radiobox 0, 1, 2 it will give if 0=[list][0]
        if self.first_part.get() == 3:  # this is value of radiobutton user based
            self.listbox_userratings.delete(0, END)
            self.l_purple = Label(self.f6, text="User similars to:",font="Times 12 bold", fg="white", bg="purple").grid(row=1, column=10, sticky=EW)
            self.result_box_rec = getRecommendations(self.cc_ratings, self.user, similarity = self.simililarties[self.second_part.get()]) # get the recommaditions
            self.user_similars_to = topMatches(self.cc_ratings, self.user, n=5, similarity=self.simililarties[self.second_part.get()]) # get the top mathces
            self.leftone.delete(0, END) # clear listbox
            for key,value in self.result_box_rec:  #  write it
                self.leftone.insert(END, str(key)[:4] + " --- >" + value)
                if self.leftone.size() == int(self.text.get()):  # size(number of rows) equal to getting int from text
                    break
            self.listbox_users.delete(0, END)  # clear it
            for key,value in self.user_similars_to:  # write it
                self.listbox_users.insert(END, str(key)[:4] + "-" + value)
        elif self.first_part.get() == 4:
            self.listbox_userratings.delete(0, END)
            self.item_similirs = Label(self.f6, text="Item similars to:",font="Times 12 bold", fg="white", bg="purple").grid(row=1, column=10, sticky=EW)  # for update the labes
            self.item_similarty_score = Label(self.f6, text="Similary Items(select a item on the left)",font="Times 12 bold", fg="white", bg="brown").grid(row=1, column=15, sticky=EW)
            self.transformed_dict = calculateSimilarItems(self.cc_ratings, n=5)  # for item based, calculate similarties
            self.transformed_dict_2 = getRecommendedItems(self.cc_ratings,self.transformed_dict,self.user)  # give recommended items
            self.leftone.delete(0, END)  # clear listbox
            for key,value in self.transformed_dict_2:  #  write the outputs of getRecommendedItems
                self.leftone.insert(END, str(key) + "-" + value)  # write it in format
                if self.leftone.size() == int(self.text.get()) :  #  get the length of list box == get text in integer format
                    break  # if equalty checks, break the process
            self.listbox_users.delete(0, END)  # clear it
            for key in self.cc_ratings["ahmetozturk"]:  # write it
                self.listbox_users.insert(END, str(key) + "-" + str(self.cc_ratings["ahmetozturk"][key]))

    def go_right(self,e):
        if self.first_part.get() == 3:
            self.active_row = self.listbox_users.curselection()[0]  # get which one is active it will give tuples
            self.str_active = self.listbox_users.get(self.active_row,self.active_row)[0]  # get the string from tuple
            val,name = self.str_active.split("-")  # separete it, and get name
            self.listbox_userratings.delete(0, END)  # clear everthing
            self.listbox_userratings.insert(0,name + " also rated the following")  # first row
            self.listbox_userratings.insert(1,"")  # second row
            i=2 # start second
            for key in self.cc_ratings[name]:  # write it
                self.listbox_userratings.insert(i,str(key) +"-->"+ str(self.cc_ratings[name][key]))
                i = i + 1
        if self.first_part.get() == 4:
            a = self.listbox_users.curselection()[0]  # get which one is active it will give tuples
            a = self.listbox_users.get(a,a)[0]  # get the string from tuple
            name,val = a.split("-")  # separete it, and get name
            a = name.encode("utf-8")
            self.listbox_userratings.delete(0, END)  # clear everthing
            self.listbox_userratings.insert(0,"Similar items>Similarty score(for %s)" % (a))  # first row
            self.listbox_userratings.insert(1,"")  # second row
            i = 2  # start with 3th
            for key, tv in self.transformed_dict[a]:
                self.listbox_userratings.insert(i,str(tv) +"-->"+ str(key))
                i = i + 1

    def planning(self):  # this part for geometry
        for c in [self.f1,self.f2,self.f3,self.f4,self.f5,self.f6]:
            c.grid()
        self.l_ccre.grid(row=0, column=0, padx=100)
        self.l_welcome.grid(row=0,column=0)
        self.l_please.grid(row=1, column=0, padx=10)
        self.period.grid()

        self.l_choose.grid(row=0, column=0, padx=40, pady=2)
        self.l_enter.grid(row=0, column=1, padx=40, pady=2)
        self.box.grid(row=1, column=0, padx=20)
        self.slider.grid(row=1, column=1)
        self.b_add.grid(row=1, column=2, padx=20)
        self.b_remove.grid(row=1, column=5, padx=15)
        self.mylist.grid(row=1, column=3, pady=5, sticky=NS)
        self.s_top.grid(row=1, column=4, sticky=NS)
        self.period2.grid(row=0, column=0, columnspan=3)
        self.l_middle.grid(row=1, column=1)
        self.period3.grid(row=0,column=0, columnspan=10)
        self.l_settings.grid(row=1, column=0)
        self.l_number_of = Label(self.f5, text="Number of recommendations:", fg="black").grid(row=2, column=0)
        self.text.grid(row=2, column=1)
        self.l_choose_purple1 = Label(self.f5, text="Choose recommendation method:", fg="purple", font="Times 12 italic").grid(row=2, column=5)
        self.l_choose_purple2 = Label(self.f5, text="Choose similarty metric:", fg="purple", font="Times 12 italic").grid(row=5, column=5)
        self.first_part = IntVar()
        self.second_part = IntVar()
        self.user_based = Radiobutton(self.f5, text="User based", font="Times 10 bold", variable=self.first_part, value=3).grid(row=3, column=5)
        self.item_based = Radiobutton(self.f5, text="Item based", font="Times 10 bold", variable=self.first_part, value=4).grid(row=4, column=5)
        self.get_rec = Button(self.f5, text="Get Recommendations", fg="blue", font="Times 13 bold", command=self.getRec).grid(row=7, column=7)
        self.euclidean = Radiobutton(self.f5, text="Euclidean Score", font="Times 10 bold", variable=self.second_part, value=0).grid(row=6, column=5)
        self.pearson = Radiobutton(self.f5, text="Pearson Score", font="Times 10 bold", variable=self.second_part, value=1).grid(row=7, column=5)
        self.jackkard = Radiobutton(self.f5, text="Jackkard Score", font="Times 10 bold", variable=self.second_part, value=2).grid(row=8, column=5)
        self.period4.grid(row=0, column=0, columnspan=100)
        self.l_resultbox = Label(self.f6, text="Result Box(Recemmendation)", fg="black",font="Times 12 ").grid(row=1, column=0)
        self.leftone.grid(row=2, column=0, pady=5, sticky=NS)
        self.s_bot.grid(row=2, column=1, sticky=NS)
        self.l_purple.grid(row=1, column=10, sticky=EW)
        self.listbox_users.grid(row=2, column=10)
        self.l_brown.grid(row=1, column=15, sticky=EW)
        self.listbox_userratings.grid(row=2, column=15, pady=5, sticky=NS)
        self.s_bot1.grid(row=2, column=16, sticky=NS)


def main():
    root = Tk()
    root.wm_title("Enter the Recommender")
    root.geometry("950x680+175+00")
    app_erkam = Curriculum(root)
    root.mainloop()
if __name__ == "__main__":
    main()
