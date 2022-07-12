import socket, struct, time

ip = '127.0.0.1'
port = 5555

#protocolos
STRUCT_SERVER = 8
CODEX = 'utf-8'


def client():
    cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cli.connect((ip, port))

    tam = cli.recv(STRUCT_SERVER)
    print(f'Primeiro TAM: {tam}')
    st = struct.unpack('I', tam)[0]
    menu = cli.recv(st).decode(CODEX)
    time.sleep(0.1)

    tam = cli.recv(STRUCT_SERVER)
    print(f'Segundo TAM: {tam}')
    if b'\n' in tam:
        tam = tam.removeprefix(b'\n')
    if b'PAS' in tam:
        tam = tam.removesuffix(b'PAS')
    st = struct.unpack('I', tam)[0]
    msg = cli.recv(st).decode(CODEX)

    while True:
        print('-'*70)
        print(menu)
        op = input('\nOpção> ')

        st_env = struct.pack('I', len(op))
        cli.send(st_env)
        time.sleep(0.1)
        cli.send(op.encode(CODEX))
        print('-'*70)

        if op == '\\q':
            print('Encerrando...')
            time.sleep(0.3)
            cli.close()
            print('Conexão fechada!')
            break

        elif op == '\\f':
            msg = cli.recv(STRUCT_SERVER)
            st = struct.unpack('I', msg)[0]
            arqs = cli.recv(st)
            print('LISTA DE ARQUIVOS DO SERVIDOR:\n'+arqs.decode(CODEX))

        elif op == '\\d':
            nome_arquivo = input('Digite o nome do arquivo para baixar> ')
            st = struct.pack('I', len(nome_arquivo))
            cli.send(st)

            cli.send(nome_arquivo.encode(CODEX))
            tam_arquivo = cli.recv(STRUCT_SERVER)
            st = struct.unpack('I', tam_arquivo)[0]
            print(f'Tamanho do arquivo a receber, é de {st} bytes')
            #conteudo = b''
            pos = 0
            with open(nome_arquivo, 'wb') as arq:
                while pos < st:
                    dados = cli.recv(2048)
                    pos += 2048
                    arq.write(dados)

                #Segunda forma
                    #dados = cli.recv(2048+pos)
                    #pos += len(dados)
                    #conteudo += dados
                #arq.write(conteudo)

        elif op == '\\u':
            nome_arquivo = input('Nome do arquivo para enviar ao servidor (use a extensão)> ')
            st = struct.pack('I', len(nome_arquivo))
            cli.send(st)
            cli.send(nome_arquivo.encode(CODEX))

            pos = 0
            with open(nome_arquivo, 'rb') as arq:
                ler = arq.read()
                st = struct.pack('I', len(ler))
                cli.send(st)
                while pos < len(ler):
                    cli.send(ler[pos:pos+2048])
                    pos += 2048

        else:
            print(f'\nOpção < {op} > é inválida!\nTente novamente.')
        
        print()
client()
