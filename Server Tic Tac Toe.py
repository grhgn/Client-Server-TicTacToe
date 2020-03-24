from socket import *
from _thread import *
import pickle

s = socket((AF_INET),SOCK_STREAM)
ip = "127.0.0.1"
port = 8080
s.bind((ip,port))
s.listen(50)
print("Listeing in " + ip + ":" + str(port))
print("Waiting for other player...")

def check(btns, iterasi):
    menang = 0
    for i in range(3):
        if ((btns[i][0] == btns[i][1] and btns[i][0] == btns[i][2] and btns[i][0] != 0)
            or (btns[0][i] == btns[1][i] and btns[0][i] == btns[2][i] and btns[0][i] != 0)):
            return "win"

    if menang==0:
        if((btns[0][0] == btns[1][1] and btns[0][0] == btns[2][2] and btns[0][0] != 0)
        or (btns[0][2] == btns[1][1] and btns[0][2] == btns[2][0] and btns[0][2] != 0)):
            return  "win"

    if menang==0 and iterasi==9:
        return "draw"

def start_game(socketp1, socketp2, btns, iterasi, addrp1, addrp2):
    while True:
        try:
            jalan1 = socketp1.recv(1024).decode("utf-8")
            row_x = int(int(jalan1) / 3)
            column_x = int(int(jalan1) % 3)
            btns[row_x][column_x] = "X"
            win_x = check(btns, iterasi)
            iterasi += 1
            print(iterasi)
            if (win_x == "win"):
                jalan12 = pickle.dumps(([jalan1, "", "lose"]))
                socketp2.send(jalan12)
                jalan12 = pickle.dumps(([jalan1, "X", win_x]))
                socketp1.send(jalan12)
                print("Game diakhiri dangan kemenangan " + str(addrp1) + " dan kekalahan " + str(addrp2))
                break
            elif (win_x == "draw"):
                jalan12 = pickle.dumps(([jalan1, "", win_x]))
                socketp2.send(jalan12)
                jalan12 = pickle.dumps(([jalan1, "X", win_x]))
                socketp1.send(jalan12)
                print("Game diakhiri dangan seri antara " + str(addrp1) + " dan " + str(addrp2))
                break
            else:
                jalan12 = pickle.dumps(([jalan1, "X", None]))
                socketp2.send(jalan12)
        except:
            try:
                try:
                    jalan13 = pickle.dumps((["", "", "error"]))
                    socketp1.send(jalan13)
                except:
                    jalan13 = pickle.dumps((["", "", "error"]))
                    socketp2.send(jalan13)
                finally:
                    print("Salah satu pemain keluar")
            except:
                print("Both Player Closed Unexpectedly")
            break
        try:
            jalan2 = socketp2.recv(1024).decode("utf-8")
            row_o = int(int(jalan2) / 3)
            column_o = int(int(jalan2) % 3)
            btns[row_o][column_o] = "O"
            win_o = check(btns, iterasi)
            iterasi += 1
            print(iterasi)
            if (win_o == "win"):
                jalan22 = pickle.dumps(([jalan2, "", "lose"]))
                socketp1.send(jalan22)
                jalan22 = pickle.dumps(([jalan2, "O", win_o]))
                socketp2.send(jalan22)
                print("Game diakhiri dangan kemenangan " + str(addrp2) + " dan kekalahan " + str(addrp1))
                break
            elif (win_o == "draw"):
                jalan12 = pickle.dumps(([jalan2, "", win_o]))
                socketp1.send(jalan12)
                jalan12 = pickle.dumps(([jalan1, "O", win_o]))
                print("Game diakhiri dangan seri antara " + str(addrp2) + " dan " + str(addrp1))
                socketp2.send(jalan12)
                break
            else:
                jalan22 = pickle.dumps(([jalan2, "O", None]))
                socketp1.send(jalan22)
        except:
            try:
                try:
                    jalan13 = pickle.dumps((["", "", "error"]))
                    socketp2.send(jalan13)
                except:
                    jalan13 = pickle.dumps((["", "", "error"]))
                    socketp1.send(jalan13)
                finally:
                    print("Salah satu pemain keluar")
            except:
                print("Both Player Closed Unexpectedly")
            break
    socketp1.close()
    socketp2.close()

pemain = []
pemain_sekarang = []
while True:
    iterasi = 1
    btns = [[0 for x in range(3)] for y in range(3)]
    clientsocket, addr = s.accept()
    print ('Dapat Koneksi Dari', addr)
    jumlah = len(pemain) + 1
    id_pemain = "player" + str(jumlah)
    pemain.append([id_pemain, addr, clientsocket])
    pesan = "play"
    mulai = ""
    if (len(pemain) % 2 == 0):
        for i in range(len(pemain)):
            if (i % 2 == 0):
                list_pesan = pickle.dumps(([pesan, "X"]))
            else:
                list_pesan = pickle.dumps(([pesan, "O"]))
            socket = pemain[i][2]
            socket.send(list_pesan)
        mulai = "start"
        pemain_sekarang = pemain
        pemain = []
    if mulai == "start":
        socketp1 = pemain_sekarang[0][2]
        socketp2 = pemain_sekarang[1][2]
        addrp1 = pemain_sekarang[0][1]
        addrp2 = pemain_sekarang[1][1]
        print("Game telah dimulai antara " + str(addrp1) + " Dan " + str(addrp2))
        start_new_thread(start_game, (socketp1, socketp2, btns, 1, addrp1, addrp2))


