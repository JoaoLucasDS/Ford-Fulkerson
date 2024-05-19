class Vertice(object): #Objeto Vertice
  def __init__(self,tag):
    self.tag = tag #String de visualização

  def __repr__(self):
    return "%s" % (self.tag)

class Aresta(object): #Objeto Aresta
  def __init__(self,verticeEntr: Vertice,verticeSaid: Vertice, capacidade):
    self.verticeEntr = verticeEntr #Objeto vertice de origem da aresta
    self.verticeSaid = verticeSaid #Objeto vertice de destino da aresta

    self.capacidade = capacidade #capacidade maxima de fluxo para a aresta
    self.fluxo = 0 #respresentação do fluxo contido em uma aresta

  def __repr__(self):
    return "%s -> %s:%s" % (self.verticeEntr.tag, self.verticeSaid.tag, self.capacidade)

class RedeDeFluxo(object): #Objeto Grafo ou Rede de fluxo
  def __init__(self):
    self.listaVertices = {}  #Dicionario contendo vertices como chave e suas arestas adjacentes como valor, como uma lista de adjacencia

    self.fluxoMax = {} #Dicionario que acumula o fluxo 

  #Vertices
  def verificaVertice(self,vert): #verificação simples de um vertice para controle de erros
    if isinstance(vert,Vertice): 
      return True
    return False

  def addVert(self,vert): #função de adição de vertice ao dicionario do objeto Rede de fluxo
    if self.verificaVertice(vert): #chamda para a verificação simples de vertice
      self.listaVertices[vert] = [] #definição do vertice como chave do dicionario "listaVertice"
    else:
      print("Erro: Espera-se um Vertice")

  def listaAdj(self,vert): #função simples para retorno da lista de adjacencia de um vertice
    return self.listaVertices.get(vert)
    
  #Arestas
  def AddAresta(self, verticeEntr, verticeSaid, capacidade = 0): #função de adição de aresta ao grafo
    if self.verificaVertice(verticeEntr) and self.verificaVertice(verticeSaid): #verifica vertices de entrada e saida para formar a aresta
      aresta = Aresta(verticeEntr, verticeSaid, capacidade) #cria-se um objeto aresta
      revAresta = Aresta(verticeSaid, verticeEntr, 0) #Cria-se uma aresta espelhada para valores negativos encontrados no caminho entre dois vertices

      aresta.duplicata = revAresta
      revAresta.duplicata = aresta

      self.listaVertices[verticeEntr].append(aresta) #a aresta é atribuida como valor a chave respresentante de seu vertice de origem no dicionario "listaVertice"
      self.listaVertices[verticeSaid].append(revAresta)
    else:
      print("Erro: Espera-se uma Aresta entre dois Vertice")
    
  #Busca
  def Busca(self,origem,destino,caminho):
    if origem == destino:
      return caminho
    for aresta in self.listaAdj(origem):
      res = aresta.capacidade - self.fluxoMax[aresta] #definice-se a capacidade maxima restante de fluxo para cada aresta adjacente ao vertice de origem, considerando a quantiade já utilizada em outros execuções armazenada em "fluxoMax"
      if res > 0 and not (aresta, res) in caminho: #verifica se existe capacidade maxima restante de fluxo
        resultante = self.Busca(aresta.verticeSaid, destino, caminho + [(aresta, res)]) #repete o processo para os vertice encontrados nas aresta adjacentes da origem, defindo estes como novas origens
        if resultante != None: #se existe caminho, retorna o mesmo
          return resultante
  
  #Ford Fulkerson
  def FordFulkersonCormen(self,s,t):
    print("Executando Ford-Fulkerson")
    for vert in self.listaVertices: #definicie incialmente no dicionario de "fluxoMax" o valor 0 para cada aresta
      for aresta in self.listaAdj(vert): 
        self.fluxoMax[aresta] = 0
        self.fluxoMax[aresta.duplicata] = 0

    p = self.Busca(s,t,[]) #verifica a exitencia de um caminho na rede entre s(origem) e t(destino), atribuindo tal caminho para a veriavel p
    while p!=None:
      fluxoPossivel = min(res for aresta,res in p) #define o fluxo maximo possivel considerando a capacidade de cada aresta em um caminho p
      for aresta, res in p:
        self.fluxoMax[aresta] += fluxoPossivel #Adiconada no dicionario de "fluxoMax" ao valor fluxo maximo possivel para o caminho encontrado de cada aresta 
        self.fluxoMax[aresta.duplicata] -= fluxoPossivel #Reduz no dicionario de "fluxoMax" ao valor fluxo maximo possivel para cada aresta de retorno no caminho encontrado 
      
      #print(p)
      p = self.Busca(s,t,[]) #define novo caminho entre s(origem) e t(destino) para o processo acima

    return sum(self.fluxoMax[aresta] for aresta in self.listaAdj(s)) #retorna a soma dos itens de cada aresta adjacente a s(origem) definida durante a função