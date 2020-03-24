from tkinter import *
from tkinter import messagebox
from functools import partial
from socket import *
from _thread import *
from tkinter import font
import pickle

s = socket((AF_INET), SOCK_STREAM)
ip = "127.0.0.1"
port = 8080
print("Conneting to" + ip + ":" + str(port))
s.connect((ip,port))
print("Connected to " + ip + ":" + str(port))

window = Tk()
window.title("Tic Tac Toe")
window.geometry("550x500")

helve = font.Font(family='Helvetica', size=12, weight='bold')
player = 'X'
opponent_simbol = 'O'
giliran = 1

def clicked(btn, i, j):
    global giliran
    global player
    global s
    if (btn["text"]== " " and giliran==1) :
        btn["text"]=player
        nomor_tombol = i*3+j
        s.send(str(nomor_tombol).encode("utf-8"))
        giliran=0

iterasi = 1

btns = [[0 for x in range(3)] for y in range(3)]
for i in range(3):
    for j in range(3):
        btns[i][j] = Button(window,text=" ",bg="white",fg="black",width=3,height=1, font=('Helvetica', 50))
        btns[i][j].config(command = partial(clicked, btns[i][j], i, j))
        btns[i][j].grid(row=i+10, column=j+3)

def recvThread (s):
    global btns
    global giliran
    global iterasi
    while True:
        if iterasi != 0:
            messagebox.showinfo("Pemberitahuan Permainan", "Kamu Giliran Ke-" + str(iterasi) + " Sebagai " + player)
        data = pickle.loads(s.recv(4096))
        if(data[2] == "win"):
            messagebox.showinfo("Selamat! " + player, "Kamu Memenangkan Pertandingan!")
            window.destroy()
        elif(data[2] == "lose"):
            messagebox.showinfo("Kalah! " + player, "Kamu Kalah dalam Pertandingan!")
            window.destroy()
        elif(data[2] == "draw"):
            messagebox.showinfo("Draw! " + player, "Kamu seri dalam permaini ini!")
            window.destroy()
        elif (data[2] == "error"):
            messagebox.showinfo("Game Error!", "Player lain keluar atau server terjadi sebuah error")
            window.destroy()
        if (data[1] != ""):
            #nomor_tombol = int(s.recv(1024).decode("utf-8"))
            nomor_tombol = int(data[0])
            opponent_simbol = data[1]
            row = int(nomor_tombol/3)
            column = int(nomor_tombol%3)
            btns[row][column]["text"]=opponent_simbol
            giliran=1
            iterasi = iterasi+2
pesan = s.recv(4096)
if pesan:
    data = pickle.loads(pesan)
    player = data[1]
    if player == "O":
        giliran = 0
        iterasi = 0
    else:
        giliran = 1
        iterasi = 1
    lbl2 = Label(window, text="          ")
    lbl2.grid(row=1, column=1)
    lbl3 = Label(window, text="          ")
    lbl3.grid(row=1, column=2)
    lbl4 = Label(window, text="          ")
    lbl4.grid(row=1, column=3)
    lbl1 = Label(window, text="Kamu Sebagai " + player)
    lbl1.config(font=("Arial", 11))
    lbl1.grid(row=1, column=4)

    start_new_thread(recvThread, (s,))

    window.mainloop()