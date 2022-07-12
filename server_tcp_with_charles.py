#bibliotecas usadas, além de imPORTar outro programa
import os, struct, threading, socket, time
import funcions

#definição de alguns protocolos e ativação do servidor
IP = '127.0.0.1'
PORT = 5555
CODEX = 'utf-8'
TAM_STRUCT = 8

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind((IP, PORT))
serv.listen(3)

def dir(req):
    if req.decode(CODEX) == '\\f':
        global caminho_arq_dir
        caminho_arq_dir = os.chdir('E:\Programas_Pycharm_VsCode\TAL\Charles\Servidor\server_files')
    else:
        os.chdir('E:\Programas_Pycharm_VsCode\TAL\Charles\Servidor\server_files')


#FAZER
def process_recv(data):
    tam_req = data.recv(TAM_STRUCT)
    st_req = struct.unpack('I', tam_req)[0]
    time.sleep(0.1)
    req = data.recv(st_req)
    pass

def process_env(data, dados):
    st = struct.pack('I', len(dados))
    data.send(st)
    time.sleep(0.1)
    data.send(dados.encode(CODEX))

#função que refe a interatividade com o cliente
def interact(data, cli):
    try:
        dados = funcions.func()
        process_env(data, dados)
        process_env(data, dados='PASS STRUCT')

        while True:
            tam_req = data.recv(TAM_STRUCT)
            st_req = struct.unpack('I', tam_req)[0]
            time.sleep(0.1)
            req = data.recv(st_req)


            if req == b'\\q':
                print(f'Cliente: {cli} efetuando logoff...', end='')
                return print(' Conexão fechada!')


            elif req == b'\\f':
                dir(req)
                lista_arq_dir = os.listdir(caminho_arq_dir)
                dados = ''
                for i in lista_arq_dir:
                    dados += '\n'+i
                process_env(data, dados)
            

            elif req == b'\\d':
                dir(req)
                tam_nome_arq = data.recv(TAM_STRUCT)
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
                dir(req)
                tam_nome_arq = data.recv(TAM_STRUCT)
                st = struct.unpack('I', tam_nome_arq)[0]
                nome_arq = data.recv(st).decode(CODEX)

                tam_arq = data.recv(TAM_STRUCT)
                st = struct.unpack('I', tam_arq)[0]
                
                pos = 0
                print(f'Cliente {cli} está subindo arquivo de {st} bytes')
                with open(nome_arq, 'wb') as arq:
                    while pos < st:
                        dados = data.recv(2048)
                        pos += 2048
                        arq.write(dados)


            else:
                print('-'*70)
                print(f'\nRELATÓRIO\n\nCliente {cli}\nEnviou a Opção Inválida: < {req.decode(CODEX)} >.\n')
                print('-'*70)

    except Exception as e:
        print(f'\nHouve algum erro na interatividade com cliente ou ele encerrou conexão.\nERROR: {e}')


#multIPla conexão ao servidor
def conn():
    while True:
        try:
            print(f'Aguardando nova conexão com cliente. No IP: < {IP} > | E na PORTa: < {PORT} >')
            data, cli = serv.accept()
            print(f'\nConexão feita por: {data}\n')
            th1 = threading.Thread(target=interact, args=(data, cli))
            th1.start()
        except Exception as e:
            print(f'Houve algum erro no estabelecimento de nova conexão ou na chamda da função de interatividade com cliente {data}.\n\nERROR: {e}')
            continue
conn()
