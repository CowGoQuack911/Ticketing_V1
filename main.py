# Python Program to act as ticketing system, to be rolled out to users at some point.
import tkinter as tk
from sqlite3 import Cursor, Connection
from tkinter import ttk
import tkinter.messagebox
from tkinter import Text
from datetime import datetime
import os
import sqlite3

# Table Kill Code
''''
    connection = sqlite3.connect('FIT_Ticketing.db')
    cursor = connection.cursor()
    cursor.execute('drop table Tickets')

'''


# SQLITE3 table structure
def make_database():
    connection_2 = sqlite3.connect('FIT_Ticketing.db')
    cursor_2 = connection_2.cursor()
    cursor_2.execute("""CREATE TABLE Tickets(
                   Parent Text,
                   iid INTEGER, 
                   id INTEGER, 
                   User TEXT, 
                   Creation_Date TEXT, 
                   Priority TEXT, 
                   Status TEXT, 
                   Description TEXT,
                   User_Note TEXT,
                   Admin_Note TEXT)""")


def pull_job():
    return
    # pull_Data_Entry.delete(0,tk.END)
    # pull_Data_Entry.insert(0,'305923')


def clear_create():
    create_User_Title_Entry.delete(0, tk.END)
    create_Note_Entry.delete('1.0', 'end-1c')
    priority_Options_inside.set('Please Select Priority')
    create_Description_Entry.delete(0, tk.END)
    review_Live_Pull_Status_Entry.delete(0, tk.END)
    review_Live_Pull_Admin_Notes_Entry.delete(0, tk.END)
    priority_Options_inside_Review.set('Please Select Priority')
    review_Live_Pull_ID_Entry.delete(0, tk.END)


def show_frame(frame_this):
    frame_this.tkraise()
    clear_create()


def ticket_submit():
    global count
    if priority_Options_inside.get() == 'Please Select Priority' or \
            create_Note_Entry.get('1.0', 'end-1c') == '' or \
            create_User_Title_Entry.get() == '':
        error_input()
        return
    connection_Update: Connection = sqlite3.connect('FIT_Ticketing.db')
    cursor_Update: Cursor = connection_Update.cursor()
    insert_string1 = ("""INSERT INTO Tickets VALUES(
    'Ticket',
    {Cnt},
    1,
    "{User}",
    '{Date}',
    '{Priority}',
    '1',
    '{Description}',
    '{User_Note}',
    '')""".format(
        Cnt='{:>6}'.format(count),
        User=os.getlogin(),
        Date=datetime.now().strftime('%m/%d/%Y %H:%M:%S'),
        Priority=priority_Options_inside.get(),
        Description=create_Description_Entry.get(),
        User_Note=create_Note_Entry.get('1.0', 'end-1c')))
    cursor_Update.execute(insert_string1)
    connection_Update.commit()
    connection_Update.close()
    live_tree.insert(parent='', index='end', iid=str(count), text='Ticket', values=(
        count, count, os.getlogin(), datetime.now().strftime('%m/%d/%Y %H:%M:%S'), create_Description_Entry.get(),
        priority_Options_inside.get(), '1', create_Note_Entry.get('1.0', 'end-1c')))
    # live_tree.insert(parent='', index='end', iid=str(count), text='Parent', values=(count,
    # os.getlogin(), str(datetime.now().strftime('%m/%d/%Y %H:%M:%S')), create_Priority_Entry.get(), '1',
    # create_Note_Entry.get('1.0', 'end-1c'), '')) do some submit BS
    clear_create()
    count += 1
    create_Ticket_ID_entry['text'] = count


def select_record():
    review_Live_Pull_Status_Entry.delete(0, tk.END)
    review_Live_Pull_Admin_Notes_Entry.delete(0, tk.END)
    priority_Options_inside.set('Please Select Priority')
    review_Live_Pull_ID_Entry.delete(0, tk.END)
    selected = live_tree.focus()
    values = live_tree.item(selected, 'values')
    review_Live_Pull_ID_Entry.insert(0, values[1])
    review_Live_Pull_Status_Entry.insert(0, values[6])
    review_Live_Pull_Admin_Notes_Entry.insert(0, values[8])
    priority_Options_inside_Review.set('Please Select Priority')


def update_record():
    if (
            review_Live_Pull_ID_Entry.get() == '' or priority_Options_inside_Review.get() == 'Please Select Priority'
            or review_Live_Pull_Status_Entry.get() == ''):
        error_input()
        return
    # grab selected row
    selected = live_tree.focus()
    # save newer data
    connection_Add = sqlite3.connect('FIT_Ticketing.db')
    c = connection_Add.cursor()
    c.execute("""UPDATE Tickets SET
    Status = '{Status}',
    Priority = '{Priority}',
    Admin_Note = '{Admin_Notes}'
    
    WHERE rowid = {ID}""".format(
        Status=str(review_Live_Pull_Status_Entry.get()),
        Priority=str(priority_Options_inside_Review.get()),
        Admin_Notes=str(review_Live_Pull_Admin_Notes_Entry.get()),
        ID=review_Live_Pull_ID_Entry.get()))
    connection_Add.commit()
    connection_Add.close()
    # Old way of Updating, without Database
    old_values = live_tree.item(selected, 'values')
    live_tree.item(selected, values=(
        old_values[0],
        review_Live_Pull_ID_Entry.get(),
        old_values[2],
        old_values[3],
        old_values[4],
        priority_Options_inside_Review.get(),
        review_Live_Pull_Status_Entry.get(),
        old_values[7],
        review_Live_Pull_Admin_Notes_Entry.get()))
    # cleanup boxes
    review_Live_Pull_Status_Entry.delete(0, tk.END)
    review_Live_Pull_Admin_Notes_Entry.delete(0, tk.END)
    priority_Options_inside_Review.set('Please Select Priority')
    review_Live_Pull_ID_Entry.delete(0, tk.END)


def update_record_sub():
    print(priority_Options_inside_Review.get())
    global count
    # grab selected row
    if review_Live_Pull_ID_Entry.get() == '' \
            or priority_Options_inside_Review.get() == 'Please Select Priority' \
            or review_Live_Pull_Status_Entry.get() == '' \
            or review_Live_Pull_Admin_Notes_Entry.get() == '':
        error_input()
        return
    selected = live_tree.focus()
    old_values = live_tree.item(selected, 'values')
    live_tree.insert(parent=old_values[0], index='end', iid=str(count), text='notes',
                     values=(count,
                     review_Live_Pull_ID_Entry.get(),
                     old_values[1],
                     old_values[2],
                     priority_Options_inside_Review.get(),
                     review_Live_Pull_Status_Entry.get(),
                     old_values[5],
                     review_Live_Pull_Admin_Notes_Entry.get()))
    connection_Update: Connection = sqlite3.connect('FIT_Ticketing.db')
    cursor_Update: Cursor = connection_Update.cursor()
    cursor_Update.execute(""" INSERT INTO Tickets Values(
    '{Parent}',
    {County},
    {id},
    '{User}',
    '{Date}',
    '{Priority}',
    '{Status}',
    '{Description}',
    '{User_Note}',
    '{Admin_Note}')
    """.format(
        Parent=old_values[0],
        id=review_Live_Pull_ID_Entry.get(),
        User=old_values[2],
        Date=datetime.now().strftime('%m/%d/%Y %H:%M:%S'),
        Priority=old_values[6],
        Status=old_values[7],
        User_Note=old_values[8],
        Admin_Note=review_Live_Pull_Admin_Notes_Entry.get(),
        Description=old_values[5],
        County=count
    ))

    connection_Update.commit()
    connection_Update.close()
    clear_create()
    count += 1
    return



def mark_job_complete():
    # todo: will have to be done in SQL
    # todo: mark ALL jobs with same ID statuses to enumerated complete status
    # sudo code
    """
    update Ticket
    set status: 5
    where id = selected.val[0]
    :return:
    """
    connection_Complete: Connection = sqlite3.connect('FIT_Ticketing.db')
    cursor_Complete: Cursor = connection_Complete.cursor()
    cursor_Complete.execute('''
    update Tickets
    set status = 5
    where id = {ID}
    '''.format(
        ID=review_Live_Pull_ID_Entry.get()
    ))
    connection_Complete.commit()
    connection_Complete.close()
    return


# Display Error message if invalid/empty input/entry
def error_input():
    tk.messagebox.showinfo('Empty Data', 'all fields must be filled to be submitted')


# Closes Program
def close():
    root.destroy()


# Binds tree view and auto populates entry fields
def clicker(e):
    select_record()


if __name__ == '__main__':
    if os.path.isfile('FIT_Ticketing.db'):
        print("hi")
    else:
        make_database()
    # Initial table connect to count row IDs
    connection = sqlite3.connect('FIT_Ticketing.db')
    cursor = connection.cursor()
    make_Tree = cursor.execute('select rowid from Tickets order by rowid desc limit 1').fetchone()
    connection.close()
    count = 1
    if make_Tree is None:
        Count = 1
    else:
        count: int = make_Tree[0] + 1

    # Define primary window/root
    root = tk.Tk()
    root.title('FIT Ticketing')
    root.minsize(width=1000, height=800)
    root.geometry('1650x850')
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    # Create primary Frames
    main_menu = tk.Frame(root, bg='grey')
    create_Ticket = tk.Frame(root, bg='white')
    review_Ticket = tk.Frame(root, bg='white', width=1650, height=850)
    review_logs = tk.Frame(root, bg='white')
    # Frame Configuration
    # Generate all frames in cleaner fashion
    for frame in (main_menu, create_Ticket, review_Ticket, review_logs):
        frame.grid(row=0, column=0, sticky='nesw')
    # Sub Frames
    # Create Ticket_Frames
    Create_Ticket_Sub_Frame1 = tk.Frame(create_Ticket)
    Create_Ticket_Sub_Frame1.pack(padx=5, pady=5, fill='both')
    # Review ticket Frames
    review_tree_frame = tk.Frame(review_Ticket)
    review_tree_frame.pack(padx=5, pady=5, fill='x')
    review_Information_frame = tk.Frame(review_Ticket, bg='orange')
    review_Information_frame.pack(padx=5, pady=5, fill='both')
    review_Menu_frame = tk.Frame(review_Ticket, bg='grey')
    review_Menu_frame.pack(padx=5, pady=5, fill='both')

    # Scroll Bar configuration
    live_tree_scroll = ttk.Scrollbar(review_tree_frame)
    live_tree_scroll.pack(side='right', fill='y')

    # create Trees and style
    style = ttk.Style()
    style.theme_use('default')
    style.configure("Treeview",
                    background='white',
                    foreground='black',
                    rowheight=25,
                    fieldbackground='white'
                    )
    live_tree = ttk.Treeview(review_tree_frame, yscrollcommand=live_tree_scroll.set, height=25)
    style.map('Treeview',background=[('selected', 'blue')])
    live_tree['columns'] = (
        'Row_ID', 'ID', 'User', 'Date_Assigned', 'Description', 'Priority', 'Status', 'User_Notes', 'Admin_Notes')
    live_tree_scroll.config(command=live_tree.yview)

    # format tree to see what data is being pulled in
    live_tree.column('#0', anchor='w', width=60, stretch=False)
    live_tree.column('User', anchor='w', width=65, stretch=False)
    live_tree.column('Row_ID', anchor='w', width=50, stretch=False)
    live_tree.column('ID', anchor='w', width=50, stretch=False)
    live_tree.column('Date_Assigned', anchor='center', width=150, stretch=False)
    live_tree.column('Description', anchor='center', width=175, stretch=False)
    live_tree.column('Priority', anchor='w', width=60, stretch=False)
    live_tree.column('Status', anchor='w', width=60, stretch=False)
    live_tree.column('User_Notes', anchor='w', width=200)
    live_tree.column('Admin_Notes', anchor='w', width=200)
    # Header name for Tree view
    live_tree.heading('#0', text='Parent', anchor='w')
    live_tree.heading('User', text='User', anchor='w')
    live_tree.heading('Row_ID', text='Row_ID', anchor='w')
    live_tree.heading('ID', text='ID', anchor='w')
    live_tree.heading('Date_Assigned', text='Date Assigned', anchor='center')
    live_tree.heading('Description', text='Description', anchor='w')
    live_tree.heading('Priority', text='Priority', anchor='w')
    live_tree.heading('Status', text='Status', anchor='w')
    live_tree.heading('User_Notes', text='User Notes', anchor='w')
    live_tree.heading('Admin_Notes', text='Admin Notes', anchor='w')
    # Insert Database Data into Treeview
    connection = sqlite3.connect('FIT_Ticketing.db')
    cursor = connection.cursor()
    make_Tree = cursor.execute('select *,rowid from Tickets where status <> "5"').fetchall()
    live_tree.tag_configure('evenrow', background="lightblue", foreground="white")
    live_tree.tag_configure('oddrow', background= 'lightgrey', foreground="white")
    live_tree.tag_configure('subrow', background='grey', foreground="white")
    ctr = 0
    clr = ''
    for row in make_Tree:
        if ctr % 2 == 0:
            clr = 'evenrow'
        else:
            clr = 'oddrow'
        if row[0] == 'Ticket':
            live_tree.insert(parent='', index='end', iid=row[1], text=row[0],
                             values=(row[10], row[1], row[3], row[4], row[5], row[6], row[7], row[8], row[9]), tags=(clr, ))
            ctr += 1
        else:
            live_tree.insert(parent=row[0], index='end', iid=row[1], text='Note',
                             values=(row[10], row[0], row[3], row[4], row[5], row[6], row[7], row[8], row[9]), tags= 'subrow', )
    connection.commit()
    connection.close()
    # Dummy data that was added
    # live_tree.insert(parent='', index='end', iid='0', text='',
    #                  values=('1', 'spagheti', '09/25/95', '2', '1', 'lasagna', 'broken'))
    # live_tree.insert(parent='', index='end', iid='1', text='Parent', values=(
    #     '1', 'spagheti', datetime.now().strftime('%m/%d/%Y %H:%M:%S'), '2', '1', 'lasagna', 'broken'))
    # live_tree.insert(parent='', index='end', iid='2', text='Parent',
    #                  values=('2', 'spagheti', '09/25/95', '2', '1', 'lasagna', 'broken'))
    # live_tree.insert(parent='2', index='end', iid='3', text='Parent',
    #                  values=('3', 'spagheti', '09/25/95', '2', '1', 'lasagna', 'broken'))
    # live_tree.insert(parent='', index='end', iid='4', text='Parent',
    #                  values=('4', 'spagheti', '09/25/95', '2', '1', 'lasagna', 'broken'))
    # live_tree.insert(parent='', index='end', iid='5', text='Parent',
    #                  values=('5', 'spagheti', '09/25/95', '2', '1', 'lasagna', 'broken'))
    # live_tree.insert(parent='', index='end', iid='6', text='Parent',
    #                  values=('6', 'spagheti', '09/25/95', '2', '1', 'lasagna', 'broken'))
    # live_tree.insert(parent='', index='end', iid='7', text='Parent',
    #                  values=('7', 'spagheti', '09/25/95', '2', '1', 'lasagna', 'broken'))
    # live_tree.insert(parent='', index='end', iid='8', text='Parent',
    #                  values=('8', 'spagheti', '09/25/95', '2', '1', 'lasagna', 'broken'))
    # live_tree.insert(parent='', index='end', iid='9', text='Parent',
    #                  values=('9', 'spagheti', '09/25/95', '2', '1', 'lasagna', 'broken'))
    # live_tree.insert(parent='', index='end', iid='10', text='Parent',
    #                  values=('10', 'spagheti', '09/25/95', '2', '1', 'lasagna', 'broken'))
    live_tree.pack(fill='both', padx=5, pady=5)

    # View_Logs = tk.Frame()
    # Options menus for Priority and Status
    priority_Options = ['1 -General Assistance',
                        '2 - Moderate',
                        '3 - Should probably try',
                        '4 - oh lord the house is on fire']
    Status_Options = ['1 - Ticket Received',
                      '2 - Ticket Under Review',
                      '3 - Ticket Requires Further Investigation',
                      '4 - Difficulties, seeking escalation',
                      '5 - Job completed/Closed']
    # Home Screen Widgets
    home_To_Create_Button = tk.Button(main_menu, text='Create Ticket',
                                      width=25,
                                      height=2,
                                      bg='black',
                                      fg='white',
                                      command=lambda: show_frame(create_Ticket))
    home_To_Review_Button = tk.Button(main_menu, text='Review Tickets',
                                      width=25,
                                      height=2,
                                      bg='black',
                                      fg='white',
                                      command=lambda: show_frame(review_Ticket))
    home_To_Log_Button = tk.Button(main_menu,
                                   text='View Logs',
                                   width=25,
                                   height=2,
                                   bg='black',
                                   fg='white',
                                   command=lambda: show_frame(review_logs))
    home_To_Quit_Button = tk.Button(main_menu, text='Quit',
                                    fg='white',
                                    bg='black',
                                    height=2,
                                    width=25,
                                    command=lambda: close())

    # Create Ticket Widgets
    create_User_Title_Label = tk.Label(Create_Ticket_Sub_Frame1, text='Ticket Title')
    create_User_Title_Entry = tk.Entry(Create_Ticket_Sub_Frame1, width=50, bg='white', fg='black')
    create_Ticket_ID_Label = tk.Label(Create_Ticket_Sub_Frame1, text='Ticket#')
    create_Ticket_ID_entry = tk.Label(Create_Ticket_Sub_Frame1, text=count, width=50)
    create_User_Label = tk.Label(Create_Ticket_Sub_Frame1, text='Name', width=50)
    create_User_Entry = tk.Label(Create_Ticket_Sub_Frame1, text=os.getlogin(), width=50, fg='black')
    create_Date_Created_Label = tk.Label(Create_Ticket_Sub_Frame1, text='Creation Date', width=50)
    create_Date_Created_Entry = tk.Label(Create_Ticket_Sub_Frame1, text=str(datetime.now().strftime('%m/%d/%Y')),
                                         width=50)
    create_Priority_Label = tk.Label(Create_Ticket_Sub_Frame1, text='Priority', width=50)
    create_Priority_Entry = tk.Entry(Create_Ticket_Sub_Frame1, width=50, bg='white', fg='black')
    # Set Priority options to be selected from
    priority_Options_inside = tkinter.StringVar(Create_Ticket_Sub_Frame1)
    priority_Options_inside.set('Please Select Priority')
    Dropdown_Priority = tkinter.OptionMenu(Create_Ticket_Sub_Frame1, priority_Options_inside, *priority_Options)
    create_Description_Label = tk.Label(Create_Ticket_Sub_Frame1, text='Enter Description of issue', width=50)
    create_Description_Entry = tk.Entry(Create_Ticket_Sub_Frame1, width=50, bg='white', fg='black')
    create_Note_Label = tk.Label(Create_Ticket_Sub_Frame1, text='Notes', width=100)
    create_Note_Entry = Text(Create_Ticket_Sub_Frame1, width=100, height=5)
    create_Push_Ticket = tk.Button(Create_Ticket_Sub_Frame1, text='Submit Ticket', width=25, height=2, fg='white',
                                   bg='black', command=lambda: ticket_submit())
    create_To_Home_Button = tk.Button(Create_Ticket_Sub_Frame1, text='Return', width=25, height=2, bg='black',
                                      fg='white', command=lambda: show_frame(main_menu))
    # Review Live Logs Widgets
    review_Live_Update_load = tk.Button(review_Menu_frame, text='Load Entry', width=25, height=2, bg='black',
                                        fg='white', command=lambda: select_record())
    review_Live_Update_Button = tk.Button(review_Menu_frame, text='Update Entry', width=25, height=2, bg='black',
                                          fg='white', command=lambda: update_record())
    review_Live_Update_Sub_Button = tk.Button(review_Menu_frame, text='Update Entry child', width=25, height=2,
                                              bg='black', fg='white', command=lambda: update_record_sub())
    review_Live_Complete_Ticket = tk.Button(review_Menu_frame, text='Mark Complete', width=25, height=2, bg='black',
                                            fg='white',
                                            command=lambda: mark_job_complete())
    review_Live_To_Home_Button = tk.Button(review_Menu_frame,
                                           text='Return',
                                           width=25,
                                           height=2,
                                           bg='black',
                                           fg='white',
                                           command=lambda: show_frame(main_menu))
    review_Live_Pull_ID_Label = tk.Label(review_Information_frame, text='ID', width=43, bg='grey')
    review_Live_Pull_ID_Entry = tk.Entry(review_Information_frame, width=50)
    review_Live_Pull_Status_Label = tk.Label(review_Information_frame, text='Status', width=43, bg='grey')
    review_Live_Pull_Status_Entry = tk.Entry(review_Information_frame, width=50)
    review_Live_Pull_Priority_Label = tk.Label(review_Information_frame, text='Priority', width=43, bg='grey')
    # review_Live_Pull_Priority_Entry = tk.Entry(review_Information_frame, width=50)
    priority_Options_inside_Review = tkinter.StringVar(review_Information_frame)
    priority_Options_inside_Review.set('Please Select Priority')
    Dropdown_Priority_Review = tkinter.OptionMenu(review_Information_frame, priority_Options_inside_Review, *priority_Options)
    Dropdown_Priority_Review.config(width=43)
    review_Live_Pull_Admin_Notes_Label = tk.Label(review_Information_frame, text='Admin Notes', width=86, bg='grey')
    review_Live_Pull_Admin_Notes_Entry = tk.Entry(review_Information_frame, width=100)
    # Main Screen Label
    pull_data_label = tk.Label(main_menu, text='Welcome to our village', width=25, height=2)
    review_Logs_To_Home_Button = tk.Button(review_logs, text='Return', width=25, height=2, bg='black', fg='white',
                                           command=lambda: show_frame(main_menu))

    # positional assignments
    # Home Positions
    # pull_data_label.pack(anchor='n',pady=25)
    # home_To_Create_Button.pack(anchor='w')
    # home_To_Log_Button.pack(anchor='e')
    # home_To_Review_Button.pack(anchor='sw',padx=100,pady=100)
    # home_To_Quit_Button.pack(anchor='center')

    # no
    # Main Menu Positions
    pull_data_label.grid(row=0, column=3, padx=2, pady=2, sticky='nesw')
    home_To_Create_Button.grid(row=5, column=2, padx=5, pady=5)
    home_To_Review_Button.grid(row=5, column=4, padx=5, pady=5)
    home_To_Log_Button.grid(row=6, column=4, padx=5, pady=5)
    home_To_Quit_Button.grid(row=50, column=3, pady=5, padx=10, sticky='nesw')
    space = tk.Label(main_menu)
    space.grid(row=7, columnspan=50)
    space.grid(row=8, columnspan=50)
    # Create Ticket Positions
    create_User_Title_Label.grid(row=0, column=1, padx=2, pady=2)
    create_User_Title_Entry.grid(row=1, column=1, padx=2, pady=2)
    create_Ticket_ID_Label.grid(row=0, column=2, padx=2, pady=2)
    create_Ticket_ID_entry.grid(row=1, column=2, padx=2, pady=2)
    create_User_Label.grid(row=2, column=0, padx=2, pady=0)
    create_User_Entry.grid(row=3, column=0, padx=2, pady=2)
    create_Priority_Label.grid(row=2, column=1, padx=2, pady=2)
    # create_Priority_Entry.grid(row=3, column=1, padx=2, pady=0)
    Dropdown_Priority.grid(row=3, column=1, padx=2, pady=0)
    create_Date_Created_Label.grid(row=2, column=2, padx=2, pady=15)
    create_Date_Created_Entry.grid(row=3, column=2, padx=2, pady=0)
    create_Description_Label.grid(row=4, column=1, padx=2, pady=15)
    create_Description_Entry.grid(row=5, column=1, padx=2, pady=0)
    create_Note_Label.grid(row=6, column=0, padx=2, pady=15, columnspan=5)
    create_Note_Entry.grid(row=7, column=0, padx=2, pady=0, columnspan=5)
    create_Push_Ticket.grid(row=10, column=0, padx=2, pady=200)
    create_To_Home_Button.grid(row=10, column=2, padx=2, pady=200)

    # Review Live Positions
    review_Live_Update_load.pack(padx=5, pady=5, side='left')
    review_Live_Update_Button.pack(padx=5, pady=5, side='left')
    review_Live_Update_Sub_Button.pack(padx=5, pady=5, side='left')
    review_Live_Complete_Ticket.pack(padx=5, pady=5, side='left')
    review_Live_To_Home_Button.pack(padx=5, pady=5, side='right')
    review_Live_Pull_ID_Label.grid(row=0, column=0, padx=2, pady=2)
    review_Live_Pull_ID_Entry.grid(row=1, column=0, padx=2, pady=2)
    review_Live_Pull_Status_Label.grid(row=0, column=1, padx=2, pady=2)
    review_Live_Pull_Status_Entry.grid(row=1, column=1, padx=2, pady=2)
    review_Live_Pull_Priority_Label.grid(row=0, column=2, padx=2, pady=2)
    Dropdown_Priority_Review.grid(row=1, column=2, padx=2, pady=2)
    # review_Live_Pull_Priority_Entry.grid(row=1, column=2, padx=2, pady=2)
    review_Live_Pull_Admin_Notes_Label.grid(row=0, column=3, padx=2, pady=2)
    review_Live_Pull_Admin_Notes_Entry.grid(row=1, column=3, padx=2, pady=2)
    # Review Logs to positions
    review_Logs_To_Home_Button.pack(padx=5, pady=5)

    show_frame(main_menu)
    root.update()

    live_tree.bind("<ButtonRelease-1>", clicker)
    root.mainloop()
