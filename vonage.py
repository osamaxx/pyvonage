"""
By Edson Dario
27/02/2018
"""
from time import sleep
import sys, serial as pyserial

class Vonage():
    porta = ""
    ip = ""
    mascara = ""
    roteador = ""
    tftp = ""
    conexao = ""
    statusserial = False
    
    def __init__(self):
        self.configurarParametros()    
       
    def abrirConexao(self):
        self.conexao = pyserial.Serial\
                       (self.porta, 115200, xonxoff=True, timeout=4)
        if self.conexao.isOpen() == True:
            self.statusserial = True
        else:
            print("Não foi possivel abrir conexão na porta " + self.porta + "\
ou porta já está em uso. Aplicação encerrada.")
            sys.exit(1)
        
    def enviarCmd(self,cmd=None):
        if self.statusserial == True:
            cmd = cmd or ""
            if len(cmd) == 1:
                self.conexao.write(bytes(cmd, encoding='ascii'))
            else:
                self.conexao.write(bytes(cmd + "\r", encoding='ascii'))
                sleep(0.5)
        else:
            print("Porta serial não está aberta ou está ocupada. \
Comando não enviado.")

    def statusAtual(self):
        if self.statusserial == True:
            debug = self.conexao.readline().decode('ascii')
            debug = debug.split()
            return(debug)

    def configurarParametros(self):
        self.porta = input("\tPorta serial(Ex.: COM5 ou /dev/ttyUSB0) --> ")
        if self.porta == "":
            self.porta = "/dev/ttyUSB0"
        self.ip = input("\tIP (Ex.: 192.168.1.10) --> ")
        if self.ip == "":
            self.ip = "192.168.1.10"
        self.mascara = input("\tMáscara (Ex.: 255.255.255.0) --> ")
        if self.mascara == "":
            self.mascara = "255.255.255.0"
        self.roteador = input("\tRoteador (Ex.: 192.168.1.1) --> ")
        if self.roteador == "":
            self.roteador = "192.168.1.1"
        self.tftp = input("\tIP servidor TFTP: (Ex. 192.168.1.131) -->")
        if self.tftp == "":
            self.tftp = "192.168.1.131"

    def exibir(self):
        pass
    
    def downgrade(self):

        if self.statusserial == False:
            self.abrirConexao()
            
        print("\tCMD --> Aguardando aparelho ser ligado.")
        while True:
            status = self.statusAtual()
            y = "'p'"
            for x in status:
                if x == y:
                    self.enviarCmd('p')
                    sleep(1)
                    print("\tCMD --> Configurando parâmetro iniciais.")
                    self.enviarCmd(self.ip)
                    self.enviarCmd(self.mascara)
                    self.enviarCmd(self.roteador)
                    self.enviarCmd("")
                    self.enviarCmd("")
                    sleep(1)
                    print("\tCMD --> Configurando servidor TFTP.")
                    self.enviarCmd("d")
                    self.enviarCmd(self.tftp)
                    self.enviarCmd("301u.bin")
                    print("\tCMD --> Efetuando download do firmware.")

                    status = str(self.statusAtual())
                    while status != "['(0-3)[2]:']":
                        status = str(self.statusAtual())
                    print("\tCMD --> Armazenando na memória 1")
                    self.enviarCmd("1")
                    self.enviarCmd("")
                    sleep(9)
                    
                    status = str(self.statusAtual())
                    while status != "['Store', 'parameters', 'to', 'flash?', '[n]']":
                        status = str(self.statusAtual())
                                                
                    self.enviarCmd("y")
                    self.enviarCmd("")
                    sleep(1)

                    self.enviarCmd("d")
                    self.enviarCmd(self.tftp)
                    self.enviarCmd("301u.bin")
                    
                    status = str(self.statusAtual())
                    while status != "['(0-3)[2]:']":
                        status = str(self.statusAtual())
                    print("\tCMD --> Armazenando na memória 2")
                    self.enviarCmd("2")
                    self.enviarCmd("")
                    sleep(9)
                    
                    status = str(self.statusAtual())
                    while status != "['Store', 'parameters', 'to', 'flash?', '[n]']":
                        status = str(self.statusAtual())
                                                
                    self.enviarCmd("y")
                    self.enviarCmd("")
                    sleep(1)

                    print("\tCMD --> Downgrade executado com sucesso!")
                    self.enviarCmd("z")
                    self.conexao.close()
                    sys.exit(0)
                    
print("###  Configurador - Vonage VDV21/VDV22/VDV23 para qualquer servidor.")
print("\n# 1º Conecte cabo serial/TTL corretamente no aparelho. (RX,TX,GND)")
print("\n# 2º Conecte cabo na porta USB/serial do PC.")
print("\n# 3º No Gerenciador de tarefas do Windows, identifique porta serial. \
Ex.: COM5.")

input("\n# 4º Pressione Enter e informe dados.")
vdv = Vonage()

input("\n# 5º Pressione Enter novamente. Logo após, sem pressa, \
ligue o dispositivo.")
vdv.downgrade()
