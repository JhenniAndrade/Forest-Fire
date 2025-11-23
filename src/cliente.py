import random
import socket
import json
import sys

# Estados possíveis
VAZIO = 0
ARVORE = 1
FOGO = 2

def contar_vizinhos_fogo(matriz, i, j):
    """Conta quantos vizinhos estão em chamas."""
    n, m = len(matriz), len(matriz[0]) if matriz else 0
    count = 0
    
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            if di == 0 and dj == 0:
                continue
            ni, nj = i + di, j + dj
            if 0 <= ni < n and 0 <= nj < m and matriz[ni][nj] == FOGO:
                count += 1
    return count

def processar_regiao(regiao_data, prob_crescimento=0.01, prob_fogo=0.0001):
    """Processa uma região da matriz aplicando as regras do Forest Fire."""
    matriz_expandida = regiao_data['matriz']
    offset_original = regiao_data['offset_original']
    linha_inicio = regiao_data['linha_inicio_original']
    linha_fim = regiao_data['linha_fim_original']
    
    altura_original = linha_fim - linha_inicio
    m_expandida = len(matriz_expandida[0]) if matriz_expandida else 0
    matriz_resultado = []
    
    for i_local in range(altura_original):
        linha_resultado = []
        i_expandida = i_local + offset_original
        
        for j in range(m_expandida):
            cel = matriz_expandida[i_expandida][j]
            
            if cel == VAZIO:
                novo_estado = ARVORE if random.random() < prob_crescimento else VAZIO
            elif cel == ARVORE:
                if random.random() < prob_fogo or contar_vizinhos_fogo(matriz_expandida, i_expandida, j) > 0:
                    novo_estado = FOGO
                else:
                    novo_estado = ARVORE
            elif cel == FOGO:
                novo_estado = VAZIO
            else:
                novo_estado = cel
                
            linha_resultado.append(novo_estado)
        matriz_resultado.append(linha_resultado)
    
    return matriz_resultado

class ClienteForestFire:
    def __init__(self, host='localhost', porta=8000):
        self.host = host
        self.porta = porta
        self.socket = None
        self.conectado = False
        
    def conectar(self):
        """Conecta ao servidor."""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.porta))
            self.conectado = True
            print(f"Conectado ao servidor {self.host}:{self.porta}")
            return True
        except Exception as e:
            print(f"Erro ao conectar: {e}")
            return False
    
    def enviar_dados(self, dados):
        """Envia dados para o servidor."""
        try:
            mensagem = json.dumps(dados).encode('utf-8')
            tamanho = len(mensagem)
            self.socket.sendall(tamanho.to_bytes(4, byteorder='big'))
            self.socket.sendall(mensagem)
            return True
        except:
            return False
    
    def receber_dados(self):
        """Recebe dados do servidor."""
        try:
            tamanho_bytes = self.socket.recv(4)
            if len(tamanho_bytes) != 4:
                return None
            tamanho = int.from_bytes(tamanho_bytes, byteorder='big')
            
            dados_bytes = b''
            while len(dados_bytes) < tamanho:
                chunk = self.socket.recv(min(tamanho - len(dados_bytes), 4096))
                if not chunk:
                    break
                dados_bytes += chunk
                
            return json.loads(dados_bytes.decode('utf-8'))
        except:
            return None
    
    def executar(self):
        """Loop principal do cliente."""
        while self.conectado:
            comando_data = self.receber_dados()
            if not comando_data:
                print("Conexão perdida")
                break
            
            comando = comando_data.get('comando')
            if comando == 'processar':
                regiao_data = comando_data['regiao']
                prob_crescimento = comando_data.get('prob_crescimento', 0.01)
                prob_fogo = comando_data.get('prob_fogo', 0.0001)
                
                matriz_processada = processar_regiao(regiao_data, prob_crescimento, prob_fogo)
                resultado = {'matriz_processada': matriz_processada}
                
                if not self.enviar_dados(resultado):
                    break
                    
            elif comando == 'encerrar':
                print("Encerrando cliente")
                break
    
    def desconectar(self):
        """Desconecta do servidor."""
        self.conectado = False
        if self.socket:
            try:
                self.socket.close()
            except:
                pass

if __name__ == "__main__":
    porta = 8000
    host = 'localhost'
    
    if len(sys.argv) > 1:
        try:
            porta = int(sys.argv[1])
        except:
            pass
    if len(sys.argv) > 2:
        host = sys.argv[2]
    
    print(f"Cliente Forest Fire conectando em {host}:{porta}")
    
    cliente = ClienteForestFire(host, porta)
    if cliente.conectar():
        try:
            cliente.executar()
        except KeyboardInterrupt:
            print("Interrompido pelo usuário")
        finally:
            cliente.desconectar()
    else:
        print("Falha na conexão")