import random
import time
import socket
import json
import threading

# Estados possíveis  
VAZIO = 0
ARVORE = 1
FOGO = 2

def criar_matriz(n, prob_arvore=0.6):
    """Cria uma matriz nxn com árvores distribuídas aleatoriamente."""
    return [
        [ARVORE if random.random() < prob_arvore else VAZIO for _ in range(n)]
        for _ in range(n)
    ]

def dividir_matriz_em_regioes(n, num_clientes):
    """Divide a matriz em regiões horizontais para distribuir entre clientes."""
    linhas_por_cliente = n // num_clientes
    regioes = []
    for i in range(num_clientes):
        inicio = i * linhas_por_cliente
        fim = n if i == num_clientes - 1 else (i + 1) * linhas_por_cliente
        regioes.append((inicio, fim))
    return regioes

def extrair_regiao_com_bordas(matriz, linha_inicio, linha_fim):
    """Extrai região com bordas para cálculo correto da vizinhança."""
    n = len(matriz)
    inicio_expandido = max(0, linha_inicio - 1)
    fim_expandido = min(n, linha_fim + 1)
    
    regiao = [matriz[i][:] for i in range(inicio_expandido, fim_expandido)]
    
    return {
        'matriz': regiao,
        'linha_inicio_original': linha_inicio,
        'linha_fim_original': linha_fim,
        'offset_original': linha_inicio - inicio_expandido
    }


class ServidorForestFire:
    def __init__(self, porta=8000):
        self.porta = porta
        self.clientes = []
        self.servidor_socket = None
        
    def iniciar_servidor(self):
        """Inicia o servidor e aceita conexões."""
        self.servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servidor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.servidor_socket.bind(('localhost', self.porta))
            self.servidor_socket.listen(4)
            print(f"Servidor iniciado na porta {self.porta}")
            return True
        except Exception as e:
            print(f"Erro ao iniciar servidor: {e}")
            return False
    
    def aceitar_clientes(self, num_clientes):
        """Aceita conexões de clientes."""
        print(f"Aguardando {num_clientes} clientes...")
        while len(self.clientes) < num_clientes:
            try:
                cliente_socket, endereco = self.servidor_socket.accept()
                self.clientes.append({'socket': cliente_socket, 'endereco': endereco})
                print(f"Cliente {len(self.clientes)} conectado de {endereco}")
            except Exception as e:
                print(f"Erro: {e}")
                break
    
    def enviar_dados(self, cliente_id, dados):
        """Envia dados para um cliente."""
        try:
            mensagem = json.dumps(dados).encode('utf-8')
            tamanho = len(mensagem)
            cliente = self.clientes[cliente_id]
            cliente['socket'].sendall(tamanho.to_bytes(4, byteorder='big'))
            cliente['socket'].sendall(mensagem)
            return True
        except:
            return False
    
    def receber_dados(self, cliente_id):
        """Recebe dados de um cliente."""
        try:
            cliente = self.clientes[cliente_id]
            tamanho_bytes = cliente['socket'].recv(4)
            tamanho = int.from_bytes(tamanho_bytes, byteorder='big')
            
            dados_bytes = b''
            while len(dados_bytes) < tamanho:
                chunk = cliente['socket'].recv(min(tamanho - len(dados_bytes), 4096))
                if not chunk:
                    break
                dados_bytes += chunk
            
            return json.loads(dados_bytes.decode('utf-8'))
        except:
            return None
    
    def processar_iteracao(self, matriz, num_clientes, prob_crescimento=0.01, prob_fogo=0.0001):
        """Processa uma iteração distribuída."""
        n = len(matriz)
        regioes = dividir_matriz_em_regioes(n, num_clientes)
        
        # Envia trabalho para clientes
        for i in range(num_clientes):
            regiao_data = extrair_regiao_com_bordas(matriz, regioes[i][0], regioes[i][1])
            trabalho = {
                'comando': 'processar',
                'regiao': regiao_data,
                'prob_crescimento': prob_crescimento,
                'prob_fogo': prob_fogo
            }
            self.enviar_dados(i, trabalho)
        
        # Recebe resultados
        nova_matriz = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(num_clientes):
            resultado = self.receber_dados(i)
            if resultado:
                linha_inicio, linha_fim = regioes[i]
                matriz_resultado = resultado['matriz_processada']
                for idx, linha_global in enumerate(range(linha_inicio, linha_fim)):
                    nova_matriz[linha_global] = matriz_resultado[idx]
        
        return nova_matriz
    
    def simular_distribuida(self, n, iteracoes, num_clientes):
        """Executa simulação distribuída completa."""
        print(f"Simulação {n}x{n}, {iteracoes} iterações, {num_clientes} clientes")
        
        self.aceitar_clientes(num_clientes)
        matriz = criar_matriz(n)
        
        inicio = time.time()
        for i in range(iteracoes):
            matriz = self.processar_iteracao(matriz, num_clientes)
            if i % 20 == 0:
                print(f"Iteração {i}")
        fim = time.time()
        
        # Encerra clientes
        for i in range(num_clientes):
            self.enviar_dados(i, {'comando': 'encerrar'})
        
        tempo = fim - inicio
        print(f"Tempo distribuído: {tempo:.4f}s")
        return tempo
    
    def fechar(self):
        """Fecha conexões."""
        for cliente in self.clientes:
            try:
                cliente['socket'].close()
            except:
                pass
        if self.servidor_socket:
            try:
                self.servidor_socket.close()
            except:
                pass


if __name__ == "__main__":
    # Exemplo de uso simples
    import sys
    
    if len(sys.argv) >= 4:
        n = int(sys.argv[1])  # tamanho da matriz
        iteracoes = int(sys.argv[2])  # número de iterações  
        num_clientes = int(sys.argv[3])  # número de clientes
        
        servidor = ServidorForestFire()
        if servidor.iniciar_servidor():
            servidor.simular_distribuida(n, iteracoes, num_clientes)
            servidor.fechar()
    else:
        print("Uso: python servidor.py <tamanho> <iteracoes> <clientes>") 
        print("Exemplo: python servidor.py 300 20 2")