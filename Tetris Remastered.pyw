import time
import tkinter as tk
import random
import sys
import threading
import subprocess
main=tk.Tk()
main.geometry("640x480")
main.configure(bg="BLACK")
main.title("Tetris Remastered")
def off():
    main.destroy()
    subprocess.run("python main_sp.pyw")
    
def on():
    def hoster():
        
        join_but.destroy()
        host_but.destroy()
        import socket
        hn=socket.gethostname()
        ip_addr=socket.gethostbyname(hn)
        s=socket.socket()
        s.bind(("",8585))
        s.listen(4)
        ip_split=ip_addr.split(".")
        host_label["text"]='''Waiting For devices
CODE : {}'''.format(ip_split[-1])
        
        leb_def=tk.Label(text="Enter Your Name",font=("ariel.ttf",15),bg="BLACK",fg="WHITE")
        leb_def.pack()
        leb_def.place(x=100,y=250)
        priv_host=tk.StringVar()
        host_name_priv=tk.Entry(textvariable=priv_host,font=("ariel.ttf",15))
        host_name_priv.pack()
        host_name_priv.place(x=290,y=250)

        def mainloop(): 
            clients={}  # <<< create a def
            while True:
                
                conn, addr = s.accept()  # thread issue, not showing tkinter
                print(addr, 'connected')
                def highstart():
                    main.destroy()
                    conn.send("$startgame$")
                    subprocess.run("python main_mp.pyw")
                    
                game_starter=tk.Button(text="Start Game",command=highstart,font=("ariel.ttf",15))
                game_starter.pack()
                game_starter.place(x=290,y=250)
                cli_dat=conn.recv(1024)
                if cli_dat[0:6]==b"$name$":
                    clients[addr[0]]=cli_dat[6:]
                
                    

        threading.Thread(target=mainloop).start() # <<< run loop on new thread
        
        


    def joiner():
        join_but.destroy()
        def conn_to_host():
            hn=socket.gethostname()
            ip_addr=socket.gethostbyname(hn)
            ip_split=ip_addr.split(".")
            ddd=codevar.get()
            ip_split.pop(-1)
            ip_split.append(ddd)
            hostip=''
            for lulu in ip_split:
                hostip=hostip+lulu+"."

            s=socket.socket()
            print(hostip[0:-1])
            s.connect((hostip,8585))
            namecoded="$name$"+namevar.get()
            s.send(namecoded.encode())
            host_wait=tk.Label(text="Waiting For Host To Start Game...",font=("ariel.ttf",15),bg="BLACK",fg="WHITE")
            host_wait.pack()
            host_wait.place(x=200,y=150)
            while True:
                if s.recv(1024)=="$startgame$":
                    main.destroy()
                    subprocess.run("python main_mp.pyw")
                    scr_fil=open("scores.data","r+")
                    score_cli=scr_fil.read()
                    dat_score="$score$"+score_cli
                    s.send(dat_score.encode())
                    
            
            
            
        import socket
        host_but.destroy()
        cli_code_leb=tk.Label(text="Enter CODE :",font=("ariel.ttf",15),bg="BLACK",fg="WHITE")
        cli_code_leb.pack()
        cli_code_leb.place(x=50,y=100)
        
        
        cli_name_leb=tk.Label(text="Enter Name :",font=("ariel.ttf",15),bg="BLACK",fg="WHITE")
        cli_name_leb.pack()
        cli_name_leb.place(x=50,y=200)

        codevar=tk.StringVar()
        code_field=tk.Entry(text="Enter CODE :",textvariable=codevar,font=("ariel.ttf",15))
        code_field.pack()
        code_field.place(x=200,y=100)
        namevar=tk.StringVar()
        name_field=tk.Entry(text="Enter Your Name",textvariable=namevar,font=("ariel.ttf",15))
        name_field.pack()
        name_field.place(x=200,y=200)

        connect_but=tk.Button(text="Connect",command=conn_to_host)
        connect_but.pack()
        connect_but.place(x=100,y=300)
        
        



    leb.destroy()
    offline.destroy()
    online.destroy()

    host_but=tk.Button(text="Host Game",command=hoster,font=("ariel.ttf",15))
    host_but.pack()
    host_but.place(x=140,y=200)

    join_but=tk.Button(text="Join game",command=joiner,font=("ariel.ttf",15))
    join_but.pack()
    join_but.place(x=390,y=200)

    host_label=tk.Label(text="",bg="BLACK",fg="WHITE",font=("ariel.ttf",15))
    host_label.pack()
    host_label.place(x=210,y=100)








leb=tk.Label(text="TETRIS Remastered",font=("ariel.ttf",25),fg="WHITE",bg="BLACK")
leb.pack()
leb.place(x=170,y=100)

offline=tk.Button(text="Singleplayer",command=off,font=("ariel.ttf",15))
offline.pack()
offline.place(x=100,y=200)

online=tk.Button(text="Multiplayer (Local)",command=on,font=("ariel.ttf",15))
online.pack()
online.place(x=350,y=200)

main.mainloop()