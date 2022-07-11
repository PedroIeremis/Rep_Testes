#bibliotecas usadas, além de importar outro programa
import os, struct, threading, socket, time
import funcions


#definição de IP, Porta e lista para administrar clientes online
ip = '127.0.0.1'
port = 5555
clients = []


#definição de alguns protocolos e ativação do servidor
CODEX = 'utf-8'
TAM_REQS = 8
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind((ip, port))
serv.listen(3)


#função que refe a interatividade com o cliente
def interact(data):
    try:
        lfunc = funcions.func()
        st = struct.pack('I', len(lfunc))
        data.send(st)
        time.sleep(0.1)
        data.send(lfunc.encode(CODEX))

        msg = 'PASS STRUCT'
        st = struct.pack('I', len(msg))
        data.send(st)
        time.sleep(0.1)
        data.send(msg.encode(CODEX))

        while True:

            tam_req = data.recv(TAM_REQS)
            st_req = struct.unpack('I', tam_req)[0]
            req = data.recv(st_req)

            if req == b'\\q':
                print(f'Cliente: {data} efetuando logoff...')
                clients.remove(data)
                return print('Conexão fechada!')

            elif req == b'\\f':
                caminho_arq_dir = os.chdir('E:\Programas_Pycharm_VsCode\client_server_SERVER\TAL\server_files')
                lista_arq_dir = os.listdir(caminho_arq_dir)
                lista = ''
                for i in lista_arq_dir:
                    lista += '\n'+i
                st = struct.pack('I', len(lista))
                data.send(st)
                time.sleep(0.5)
                data.send(lista.encode(CODEX))
            
            elif req == b'\\d':
                caminho_arq_dir = os.chdir('E:\Programas_Pycharm_VsCode\client_server_SERVER\TAL\server_files')
                lista_arq_dir = os.listdir(caminho_arq_dir)

                tam_nome_arq = data.recv(TAM_REQS)
                st = struct.unpack('I', tam_nome_arq)[0]
                nome_arq = data.recv(st).decode(CODEX)

                with open(nome_arq, 'rb') as arq:
                    ler = arq.read()
                    st = struct.pack('I', len(ler))
                    data.send(st)

                    pos = 0
                    while pos < len(ler):
                        data.send(ler[pos:pos+2048])
                        pos += 2048

            elif req == b'\\u':
                caminho_arq_dir = os.chdir('E:\Programas_Pycharm_VsCode\client_server_SERVER\TAL\server_files')
                tam_nome_arq = data.recv(TAM_REQS)
                st = struct.unpack('I', tam_nome_arq)[0]
                nome_arq = data.recv(st).decode(CODEX)

                tam_arq = data.recv(TAM_REQS)
                st = struct.unpack('I', tam_arq)[0]
                
                pos = 0
                print(f'Cliente {data} está subindo arquivo de {st} bytes')
                with open(nome_arq, 'wb') as arq:
                    while pos < st:
                        dados = data.recv(2048)
                        pos += 2048
                        arq.write(dados)

            else:
                pass

    except Exception as e:
        print(f'\nHouve algum erro na interatividade com cliente ou ele encerrou conexão.\nERROR: {e}')



#multipla conexão ao servidor
def conn():
    try:
        while True:
            print(f'Aguardando a nova conexão com cliente. No IP: < {ip} > | E na porta: < {port} >')
            data, cli = serv.accept()
            print(f'\nConexão feita por: {data} | {cli}\n')
            clients.append(data)
            th1 = threading.Thread(target=interact, args=(data, ))
            th1.start()
    except Exception as e:
        print(f'Houve algum erro no estabelecimento de nova conexão ou na chamda da interatividade com cliente.\n\nERROR: {e}')

conn()
