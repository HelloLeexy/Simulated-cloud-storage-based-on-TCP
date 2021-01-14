import socket
import time
import struct
import zlib
import os
from multiprocessing import Process
import multiprocessing as mp
import threading
import json
import argparse


def _argparse():
 parser = argparse.ArgumentParser(description="This is description!")
 parser.add_argument('--ip', action='store', required=True,
 dest='address', help='The path of input Vb')
 return parser.parse_args()


def sendNews1(dictSend,ip):
    print('send news 22')
    ck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #Initializes the socket
    ck.settimeout(5)
    try:
        ck.connect(ip)  #An attempt to connect to the target host will throw an exception if it fails, which is not handled here for simplicity
    except IOError as e:
        print(e)
        ck.close()
    else:
        ck.send(bytes('111', encoding='utf8'))
        print('connect and send my news 33')
        info = str(ck.recv(4), encoding='utf8')
        if info == '0001':
            print(info, 'send news other information 36')
            ck.send(dictSend.encode())
            ck.close()

def sendNews(dictSend, ip1, ip2):
    sendNews1(dictSend, ip1)
    sendNews1(dictSend, ip2)

def sendPartUpdateNews1(difftime, ip):
    print('send news 44')
    ck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #Initializes the socket
    ck.settimeout(5)
    try:
        ck.connect(ip)  # An attempt to connect to the target host will throw an exception if it fails, which is not handled here for simplicity
    except IOError as e:
        print(e)
        ck.close()
    else:
        ck.send(bytes('777', encoding='utf8'))
        print('connect and send my news 33')
        info1 = str(ck.recv(3), encoding='utf8')
        if info1=='444':
            ck.send(difftime.encode())
            info=str(ck.recv(3), encoding='utf8')
            if info == '111':
                information=str(difftime)
                mypath = information.split('$')[1]
                with open(mypath, 'rb') as f:
                    while True:
                        data3 = f.read(210000)
                        ck.send(data3)
                        break
                info1 = str(ck.recv(3), encoding='utf8')
                if info1=='888':
                    ck.close()
            elif info=='888':
                ck.close()
        else:
            ck.close()

def sendPartUpdateNews(difftime,ip1,ip2):
    sendPartUpdateNews1(difftime, ip1)
    sendPartUpdateNews1(difftime, ip2)

def FileScanner(get_file_dict, ip1, ip2):
    dict = {}
    for root, dirs, files in os.walk(r"share"):
        for file in files:
            path = os.path.join(root, file)
            sp = '\\'
            if sp not in path:
                sp = '/'
            fixtime = str(os.path.getmtime(path))
            size = str(os.path.getsize(path))
            dict2 = {'$' + path + '$': '$' + fixtime + '$' + size + '$'}
            dict.update(dict2)
    while True:
        dict3 = {}
        for root, dirs, files in os.walk(r"share"):
            for file in files:
                path = os.path.join(root, file)
                sp = '\\'
                if sp not in path:
                    sp = '/'
                filename = path.split(sp)[-1]  # Split the path string to get the file name
                fixtime = str(os.path.getmtime(path))
                size = str(os.path.getsize(path))
                dicttime1={'$' + path + '$': '$' + fixtime + '$'}
                dict2 = {'$' + path + '$': '$' + fixtime + '$' + size + '$'}
                dict3.update(dict2)
        differ = set(dict3).difference(set(dict))

        if differ == set():
            print('no new file 71')
            timediff=set(dict3.items()).difference(set(dict.items()))
            if timediff==set():
                print('nofixed')
            else:
                print('testing part update')
                info=str(timediff)
                allpath=info.split('$')[1]
                olddic=dict['$' + allpath + '$']
                oldtime=olddic.split('$')[1]
                oldsize=olddic.split('$')[2]
                newtime=info.split('$')[3]
                newzise=info.split('$')[4]
                if float(newtime)-float(oldtime)>1.2:
                    if int(oldsize)==int(newzise):
                        print(info,'is part updating!!!')
                        sendPartUpdateNews(info, ip1, ip2)
                        dict=dict3
                    else:
                        print('no trouble')
                else:
                    print('no part update')
        else:
            print('fixed 77')
            t1 = json.dumps(dict3, ensure_ascii=False)
            print(t1)
            sendNews(t1, ip1, ip2)
            dict = dict3
        time.sleep(1)

def compress(infile, dst, level=9):
    infile = open(infile, 'rb')
    dst = open(dst, 'wb')
    compress = zlib.compressobj(level)
    data = infile.read(1024)
    while data:
        dst.write(compress.compress(data))
        data = infile.read(1024)
    dst.write(compress.flush())


def decompress(infile, dst):
    infile = open(infile, 'rb')
    dst = open(dst, 'wb')
    decompress = zlib.decompressobj()
    data = infile.read(1024)
    while data:
        dst.write(decompress.decompress(data))
        data = infile.read(1024)
    dst.write(decompress.flush())


def sayHello1(get_file_dict, ip):
    print(ip)
    ck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Initializes the socket
    ck.settimeout(5)
    try:
        ck.connect(ip)  # Try to connect to the target host, and skip this step if an exception is thrown if it fails

    except IOError as e:
        print(e)
        ck.close()
    else:
        ck.send(bytes('000', encoding='utf8'))
        print('connected sayhello1 117')
        info = str(ck.recv(4), encoding='utf8')
        if info == '0001':
            dict0 = {}
            for root, dirs, files in os.walk(r"share"):
                for file in files:
                    path = os.path.join(root, file)
                    sp = '\\'
                    if sp not in path:
                        sp = '/'
                    filename = path.split(sp)[-1]  # Split the path string to get the file name
                    fixtime = str(os.path.getmtime(path))
                    size = str(os.path.getsize(path))
                    dict2 = {'$' + path + '$': '$' + fixtime + '$' + size + '$'}
                    dict0.update(dict2)

            mydict = dict0
            print(mydict, 'say hello1 mycidt 137')
            dSend = json.dumps(mydict, ensure_ascii=False)
            len_mydic = struct.pack('i', len(dSend))  # Package filename length to prevent sticky packets
            ck.send(len_mydic)  # First send the filename length,4 bytes
            ck.send(dSend.encode())
            sentence = ck.recv(1024).decode()
            otherdict = json.loads(sentence)
            print(otherdict, 'sayhello1 recv other dic 143')
            FileDownloader(mydict, otherdict, ip)
            ck.close()


def sayHello(get_file_dict, ip1, ip2):
    sayHello1(get_file_dict, ip1)
    sayHello1(get_file_dict, ip2)


def makealldict(mydic,dic1, dic2,ip):
    differ = set(dic1.items()).difference(set(dic2.items()))
    print(dic1, '111111')
    print(dic2, '222222')
    if differ == set():
        print('no need part updateed 319')
    else:
        for key in differ:
            print(differ, 'Filedownloader item is different 322')
            path = str(key)
            othername = path.split('$')[1]
            print(othername, 'other name')
            otherfixtime = path.split('$')[3]
            print(otherfixtime, 'otherfixtime')
            othersize = path.split('$')[4]
            print(othersize, 'othersize')
            mydic = dic2['$' + othername + '$']
            myfixtime = mydic.split('$')[1]
            mysize = mydic.split('$')[2]
            mykey = '$' + othername + '$'
            print(mydic, '22222222222221')
            print(mykey, '222222222')
            print(mysize, '242424')
            print(othersize, '252525')
            if int(mysize) - int(othersize) > -1:
                print('no broeaken continue send 342')
            else:
                print('need broken continue resive')
                dic2[mykey] = '$' + myfixtime + '$' + othersize + '$'
    print(dic2, '313131311')
    FileDownloader(mydic, dic2, ip)
def deal_client_request(get_file_dict, cli_addr, client):
    cmd = str(client.recv(3), encoding='utf8')
    print(cmd,'listen cmd 190')
    dict0 = {}
    for root, dirs, files in os.walk(r"share"):
        for file in files:
            path = os.path.join(root, file)
            sp = '\\'
            if sp not in path:
                sp = '/'
            fixtime = str(os.path.getmtime(path))
            size = str(os.path.getsize(path))
            dict2 = {'$' + path + '$': '$' + fixtime + '$' + size + '$'}
            dict0.update(dict2)

    mydict = dict0
    # hello
    if cmd == '000':
        client.send(bytes('0001', encoding='utf8'))
        len_data = client.recv(4)  # Accept the packaged file length data
        len_num = struct.unpack('i', len_data)[0]  # Parse the length and turn it into an int
        sentence = client.recv(len_num).decode()
        otherdict = json.loads(sentence)
        print(otherdict, '000,resive other dic 212')
        send1 = json.dumps(mydict, ensure_ascii=False)
        print(send1, '000,send my dic 214')
        client.send(send1.encode())
        client.close()


    # news
    elif cmd == '111':
        print('in 111 get a news 221',cli_addr)
        client.send(bytes('0001', encoding='utf8'))
        sentence = client.recv(1024).decode()
        otherdict = json.loads(sentence)
        myalldict={}
        print(otherdict, '111,otherdic 225')
        client.close()
        dic1=otherdict
        dic2=myalldict
        ticket = set(dic1).difference(set(dic2))
        if ticket == set():
            print('no different 7')
            makealldict(mydict,dic1, dic2, cli_addr)
        else:
            for key in ticket:
                value = dic1[key]
                print(value, '12')
                dic2[key] = value
                print(dic2, '14')
            makealldict(mydict,dic1, dic2, cli_addr)







    # get File
    elif cmd == '222':
        print(cli_addr)
        len_name = client.recv(4)  # Receive path length data, the length after packaging, to prevent sticky packets
        name_data = struct.unpack('i', len_name)[0]  # Parse the length and turn it into an int
        print(name_data)
        file_name = client.recv(name_data).decode('utf8')  # Get to path
        FILEPATH = file_name
        print('other require', FILEPATH)
        if os.path.isfile(FILEPATH):  # Determines whether the file exists, and if so, gets the file size
            client.send(bytes('666', encoding='utf8'))
            sum = 0
            sp = '\\'
            if sp not in FILEPATH:
                sp = '/'
            filename = FILEPATH.split(sp)[-1]  # Split the path string to get the file name
            data = os.path.getsize(FILEPATH)
            len_data = struct.pack('i', int(data))  # Package file length to prevent sticky packets
            client.send(len_data)  # Send the file length next,4 bytes
            cmd = str(client.recv(1024), encoding='utf8')
            print(cmd, '1313')
            if cmd == '001':
                client.close()  # Close the socket
            elif cmd == '002':
                dst = os.path.join('tempt', filename+'.sending')
                print(FILEPATH)
                compress(FILEPATH, dst)
                data1 = os.path.getsize(dst)
                len_data1 = struct.pack('i', int(data1))  # Package file length to prevent sticky packets
                client.send(len_data1)  # Send the file length again,4 bytes



                with open(dst, 'rb') as f:
                    while data1 > 0:
                        os.system('title sending:{}  sended {} KB'.format(filename, int(sum / 1024)))
                        data = f.read()
                        client.send(data)  # send file
                        data1 -= len(data)
                    cmd = str(client.recv(3), encoding='utf8')
                    print(cmd, '326')
                    if cmd == '003':
                        client.close()  # Close the socket
                try:
                    os.remove(dst)
                except IOError as e:
                    print(e,'File is used by other')
                else:
                    print('remove tmp file successful')
        else:
            client.send(bytes('333', encoding='utf8'))
            client.close()

    #Part update
    elif cmd == '777':
        client.send(bytes('444', encoding='utf8'))
        dataTime = client.recv(1024).decode()
        othername = dataTime.split('$')[1]
        otherfixtime = dataTime.split('$')[3]
        mydic = mydict['$' + othername + '$']
        print(mydict, 'differ in my dict 330')
        myfixtime = mydic.split('$')[1]
        if myfixtime-otherfixtime<0:
            client.send(bytes('111', encoding='utf8'))
            len_resive=0
            dst2=os.path.join('tempt',othername+'fixing')
            oldPath=os.path.join('share',othername)
            while len_resive < 210000:
                data3 = client.recv(1024)
                with open(dst2, 'ab') as f:
                    f.write(data3)
                len_resive = len_resive + len(data3)
            with open(oldPath, 'rb') as f:
                f.seek(210000)
                data2 = f.read()
            with open(dst2, 'ab')as f:
                f.write(data2)
            os.remove(oldPath)
            with open(dst2, 'rb')as f:
                data4 = f.read()
            with open(oldPath, 'ab')as f:
                f.write(data4)
            client.send(bytes('888', encoding='utf8'))
            os.remove(dst2)
        else:
            client.send(bytes('888', encoding='utf8'))
            client.close()






def TCPListener(get_file_dict):
    print('listening 295')
    # Create the socket
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind port number
    sk.bind(("", 20020))
    # Sets the listener to change the active socket to the passive socket
    sk.listen(128)

    # A circular call to Accept allows multiple clients to connect simultaneously and multiple clients
    while True:
        client, cli_addr = sk.accept()
        # Print socket size after successful connection
        print(cli_addr)
        clientip0=cli_addr[0]
        clientqi=(clientip0,20020)
        print(clientqi,'316')
        print('TCP get a new connected 308')
        # Create child threads
        sub_thread = threading.Thread(target=deal_client_request, args=(get_file_dict, clientqi, client))
        # Promoter thread
        sub_thread.start()

def FileDownloader(mydict, otherdict, ip):

    print('start file Downloader 320')
    print(mydict,'compare mydic 322')
    print(otherdict,'compare other dict 322')
    ticks = set(otherdict).difference(set(mydict))
    if ticks == set():
        print('non diffenenct 316')
        differ = set(otherdict.items()).difference(set(mydict.items()))
        if differ == set():
            print('need part updateed 319')
        else:
            for key in differ:
                print(differ, 'Filedownloader item is different 322')
                path = str(key)
                othername = path.split('$')[1]
                othersize = path.split('$')[4]
                print(path, 'different item 327')
                print(othername)
                mydic = mydict['$' + othername + '$']
                print(mydict,'differ in my dict 330')
                myfixtime = mydic.split('$')[1]
                mysize = mydic.split('$')[2]
                if int(mysize) - int(othersize)>-1:
                    print('no broeaken continue send 342')

                else:
                    print(mysize,'352')
                    print(othersize,'353')
                    print('needs broeaken continue send 344')
                    AskFileDownloader(othername, ip)
                    print(othername)
                    print(othername, '1')
                    print(mysize, '2')
                    print(myfixtime, '3')
    else:
        for key in ticks:
            path = str(key)
            filepath = path.split('$')[1]
            print(filepath, 'ask downloader 361')
            AskFileDownloader(filepath, ip)



def AskFileDownloader(filepath, ip):
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Initializes the socket
    try:
        sk.connect(ip)  # An attempt to connect to the target host will throw an exception if it fails, which is next
    except IOError as e:
        print(e)
        sk.close()
    else:
        sk.send(bytes('222', encoding='utf8'))
        sp = '\\'
        if sp not in filepath:
            sp = '/'
        filename = filepath.split(sp)[-1]  # Split the path string to get the file name
        midname=filepath.split(sp)[-2]
        if midname == 'share':
            print('It is a file path 436')
            mypath=os.path.join('share',filename)
        else:
            path3 = os.path.join('share',midname)
            folder3 = os.path.exists(path3)
            mypath=os.path.join('share',midname,filename)
            if not folder3:
                os.makedirs(path3)
        len_name = struct.pack('i', len(filepath))  # Package filename length to prevent sticky packets
        sk.send(len_name)  # First send the filename length,4 bytes
        sk.send(filepath.encode('utf8'))  # Send file name
        cmd = str(sk.recv(3), encoding='utf8')
        print(cmd)
        if cmd == '333':
            sk.close()
        else:
            len_data = sk.recv(4)  # Accept the packaged file length data
            len_num = struct.unpack('i', len_data)[0]  # Parse the length and turn it into an int
            print(len_num)
            dst1 = os.path.join('tempt', filename+'.lefting')
            print(filepath)
            if os.path.isfile(mypath):  # Determines whether the file exists, and if so, gets the file size
                len_size = os.path.getsize(mypath)
                if len_num-len_size>0:
                    print('file waiting depression')
                    os.remove(mypath)
                    print('broken file has been delete')
                    try:
                        decompress(dst1, mypath)
                    except ellipsis as e:
                        print('file has complete')
                    else:
                        os.remove(dst1)
                        sk.send(bytes('001', encoding='utf8'))
                        sk.close()

                else:
                    print('file has been compelete 463')
                    sk.send(bytes('001', encoding='utf8'))
                    sk.close()
            else:
                len_size = 0  # If not, the file size is 0 and the compression requires a breakpoint to continue
                len_num = len_num - len_size  # Reassign the length of the data to be accepted
                print(len_size)
                if len_num == 0:  # If the length of the file to be accepted is 0, the file is accepted
                    print('exist')
                    sk.close()
                else:  # If it's not 0, it already exists
                    sk.send(bytes('002', encoding='utf8'))
                    len_data2 = sk.recv(4)  # Accept the packaged file length data
                    len_num2 = struct.unpack('i', len_data2)[0]  # Parse the length and turn it into an int
                    if os.path.isfile(dst1):  # Determines whether the file exists, and if so, gets the file size
                        len_size2 = os.path.getsize(dst1)
                        time.sleep(0.05)
                        len_size3=os.path.getsize(dst1)
                        if len_size3-len_size2>0:
                            print('this file is reciving ! 481')
                            sk.close()
                        else:
                            print('no problem 484')
                    else:
                        len_size2 = 0  # If not, the file size is 0 and needs to be accepted in its entirety
                    print(len_size2)
                    need_len = len_num2 - len_size2  # Reassign the length of the data to be accepted
                    while len_size2 - 1024 > 0:
                        # If the length is greater than 1024, continue to accept as 1024
                        print('waiting recv 530')
                        a = sk.recv(1024)
                        print('recving   532')
                        len_size2 = len_size2 - len(a)
                    a = sk.recv(len_size2)  # Accept the data received
                    a = 0
                    while need_len > 0:  # Receives the data after the breakpoint and writes to the file
                        data = sk.recv(1024)
                        with open(dst1, 'ab') as f:
                            f.write(data)
                        need_len = need_len - len(data)
                    decompress(dst1, mypath)
                    sk.send(bytes('003', encoding='utf8'))
                    sk.close()
                    os.remove(dst1)

                    print('next')



def makefile():
    path1 = os.path.join('share')
    path2 = os.path.join('tempt')
    folder1 = os.path.exists(path1)
    folder2 = os.path.exists(path2)
    if not folder1:
        os.makedirs(path1)
    if not folder2:
        os.makedirs(path2)


def runStep(ip1, ip2):
    makefile()
    get_file_dict = mp.Manager().dict({})
    p2 = Process(target=TCPListener, args=(get_file_dict,))
    p2.start()
    sayHello(get_file_dict, ip1, ip2)
    p1 = Process(target=FileScanner, args=(get_file_dict, ip1, ip2))
    p1.start()


def main():
    parser = _argparse()
    ip1 = (parser.address.split(',')[0], 20020)
    ip2 = (parser.address.split(',')[-1], 20020)
    print(ip1, '123')
    print(ip2, '456')
    runStep(ip1, ip2)


if __name__ == '__main__':
    main()
