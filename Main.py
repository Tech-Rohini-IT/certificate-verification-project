from tkinter import messagebox 
from tkinter import * 
from tkinter import simpledialog 
import tkinter 
from tkinter import filedialog 
from tkinter.filedialog import askopenfilename 
from Block import * 
from Blockchain import * 
from hashlib import sha256 
import os 
main = Tk() 
main.title("Blockchain Based Certificate Validation") 
main.geometry("1300x1200") 
global filename 
blockchain = Blockchain() 
if os.path.exists('blockchain_contract.txt'): 
    with open('blockchain_contract.txt', 'rb') as fileinput:
        blockchain = pickle.load(fileinput) 
    fileinput.close() 
def saveCertificate(): 
    global filename 
    Text.delete('1.0', END) 
    filename = askopenfilename(initialdir = "certificate_templates") 
    with open(filename,"rb") as f: 
        bytes = f.read() 
    f.close() 
    roll_no = tf1.get() 
    name = tf2.get() 
    contact = tf3.get() 
    if len(roll_no) > 0 and len(name) > 0 and len(contact) > 0: 
        digital_signature = sha256(bytes).hexdigest(); 
        data = roll_no+"#"+name+"#"+contact+"#"+digital_signature 
        blockchain.add_new_transaction(data) 
        hash = blockchain.mine() 
        b = blockchain.chain[len(blockchain.chain)-1] 
        Text.insert(END,"Blockchain Previous Hash : "+str(b.previous_hash)+"\nBlock No : "+str(b.index)+"\nCurrent Hash : "+str(b.hash)+"\n") 
        Text.insert(END,"Certificate Digital Signature : "+str(digital_signature)+"\n\n") 
        blockchain.save_object(blockchain,'blockchain_contract.txt') 
    else: 
        Text.insert(END,"Please enter Roll No") 
def verifyCertificate(): 
    text.delete('1.0', END) 
    filename = askopenfilename(initialdir = "certificate_templates") 
    with open(filename,"rb") as f: 
        bytes = f.read() 
    f.close() 
    digital_signature = sha256(bytes).hexdigest(); 
    flag = True 
    for i in range(len(blockchain.chain)): 
        if i > 0: 
            b = blockchain.chain[i] 
            data = b.transactions[0] 
            arr = data.split("#") 
            if arr[3] == digital_signature: 
                text.insert(END,"Uploaded Certificate Validation Successfull\n") 
                text.insert(END,"Details extracted from Blockchain after Validation\n\n") 
                text.insert(END,"Roll No : "+arr[0]+"\n") 
                text.insert(END,"Student Name : "+arr[1]+"\n") 
                text.insert(END,"Contact No   : "+arr[2]+"\n") 
                text.insert(END,"Digital Sign : "+arr[3]+"\n") 
                flag = False 
                break 
            if flag: 
                text.insert(END,"Verification failed or certificate modified") 
                font = ('times', 15, 'bold') 
                title = Label(main, text='Blockchain Based Certificate Validation') 
                title.config(bg='bisque', fg='purple1')   
                title.config(font=font)            
                title.config(height=3, width=120)        
                title.place(x=0,y=5) 
                font1 = ('times', 13, 'bold') 
                l1 = Label(main, text='Roll No :') 
                l1.config(font=font1) 
                l1.place(x=50,y=100) 
                tf1 = Entry(main,width=20) 
                tf1.config(font=font1) 
                tf1.place(x=180,y=100) 
                l2 = Label(main, text='Student Name :') 
                l2.config(font=font1) 
                l2.place(x=50,y=150) 
                tf2 = Entry(main,width=20) 
                tf2.config(font=font1) 
                tf2.place(x=180,y=150) 
                l3 = Label(main, text='Contact No :') 
                l3.config(font=font1) 
                l3.place(x=50,y=200) 
                tf3 = Entry(main,width=20) 
                tf3.config(font=font1) 
                tf3.place(x=180,y=200) 
                saveButton = Button(main, text="Save Certificate with Digital Signature", command=saveCertificate) 
                saveButton.place(x=50,y=250) 
                saveButton.config(font=font1) 
                verifyButton = Button(main, text="Verify Certificate", command=verifyCertificate)
                verifyButton.place(x=420,y=250) 
                verifyButton.config(font=font1) 
                font1 = ('times', 13, 'bold') 
                text=Text(main,height=15,width=120) 
                scroll=Scrollbar(text) 
                text.configure(yscrollcommand=scroll.set) 
                text.place(x=10,y=300) 
                text.config(font=font1) 
                main.config(bg='cornflower blue') 
                main.mainloop() 
