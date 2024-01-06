
class ArbolPremisa:
    def __init__(self):
        # terminos de enlance ordenados por jerarquia
        self.terminosEnlance = ['<->', '->','^', 'v','!']

        # Es un diccionario que relaciona un termino de enlance con su funcion para evaluarla
        # p y q son preposiciones atomicas
        self.evaluarTerminoEnlance = {}
        self.evaluarTerminoEnlance['<->'] = lambda p,q: self.evaluarTerminoEnlance['->'](p,q) and self.evaluarTerminoEnlance['->'](q,p)
        self.evaluarTerminoEnlance['->'] = lambda p,q: (not p) or q
        self.evaluarTerminoEnlance['^'] = lambda p,q: p and q
        self.evaluarTerminoEnlance['v'] = lambda p,q: p or q
        self.evaluarTerminoEnlance['!'] = lambda p,q: not p if p != None else not q
        
        self.raiz = None
        
        self.preposicionesAtomicas = []

        # Si la premisa tiene parentesis entonces se almacenara el valor
        # dentro de los parentesis en el diccionario y se pondra un
        # alias en la premisa original
        self.alias = {}
        self.contadorAlias = 0

        # Almacena la referencia a los nodos que contienen las preposiciones
        # atomicas, estos serian las hojas del arbol
        self.refPreposicion = []

    #Procesa la precisa para luego construir el arbol de premisas
    def procesarPremisa(self, premisa):
        ini = [0]
        i = 0
        cantParentesis = 0
        premisaSinEspacios = ""
        
        # Quitamos todos los espacios de la premisa
        for c in premisa:
            premisaSinEspacios += c.strip()
        
        premisa = premisaSinEspacios

        # A todas las subpremisas que estan dentro de un parentesis
        # les ponemos un alias y guardamos en el diccionario
        # ejemplo: (p^q) -> (pvq) lo transforma a alias0 -> alias1
        for c in premisa:
            if c == '(':
                cantParentesis+=1
                ini.append(i)
            elif c == ')':
                ini1 = ini.pop()+1
                cantParentesis-=1
                keyAlias = "alias" + str(self.contadorAlias)
                self.alias[keyAlias] = premisa[ini1:i]
                self.contadorAlias+=1
                prevI = i
                i = len(premisa[:ini1-1]) + len(keyAlias) - 1
                premisa = premisa[:ini1-1]+keyAlias+premisa[prevI+1:]
            

            i+=1

        # Verficamos que la premisa final solo tenga dos subpremisas y un termino de enlance
        # ejemplo:
        #    p^q^s tiene tres subpremisas, entonces el siguiente codigo lo transforma a
        #    (p^q)^s y esta premisa resultante se vuelve a procesar y el resultado final sera
        #   alias0^s
        premisaSeModifico = False
        for terminoEnlance in self.terminosEnlance:
            if terminoEnlance in premisa:
                if(terminoEnlance == '!'): continue
                partesPremisa = premisa.split(terminoEnlance)
                if len(partesPremisa) > 2:
                    premisaSeModifico = True
                    n = ""
                    
                    for i in range(1, len(partesPremisa), 2):
                        n += "("+partesPremisa[i-1]+terminoEnlance+partesPremisa[i]+")"
                        if i < len(partesPremisa)-1:
                            n+=terminoEnlance
                
                    if len(partesPremisa)%2 != 0: n+=partesPremisa[-1]

                    premisa = n
                    
                    break
        
        # si la premisa no fue modificada por el precesamiento anterior entonces
        # retornamos la premisa sino volvemos a procesar la premisa
        return premisa if not premisaSeModifico else self.procesarPremisa(premisa)

    def add(self, premisa):
        premisa = self.procesarPremisa(premisa)
        self._construirArbol(premisa, self.raiz)

    # construye el arbol de la premisa
    def _construirArbol(self, premisa, nodo, iNodo=0):

        exiteTerminoEnlance = False
        for terminoEnlance in self.terminosEnlance:
            if terminoEnlance in premisa:
                premisas = premisa.split(terminoEnlance)
                exiteTerminoEnlance = True
                if(self.raiz is None):   

                    self.raiz = NodoPremisa(terminoEnlance, len(premisas))
                    self.raiz.izq = NodoPremisa()
                    self.raiz.der = NodoPremisa()
                    if(terminoEnlance != '!'): self._construirArbol(premisas[0], self.raiz.izq)
                    self._construirArbol(premisas[1], self.raiz.der)

                else:
                    #print("segundo ",premisa)
                    nodo.set(terminoEnlance)
                    nodo.izq = NodoPremisa()
                    nodo.der = NodoPremisa()
                    if(terminoEnlance != '!'): self._construirArbol(premisas[0], nodo.izq)
                    self._construirArbol(premisas[1], nodo.der)
                    

                break

        # si no existe termino de enlance estamos en una preposicion 
        # atomica
        if not exiteTerminoEnlance:
            
            # verificamos que no sea un alias, en caso que lo sea obtenemos su valor del diccionario
            # lo procesamos y seguimos construyendo el arbol de la premisa
            if(premisa in self.alias):
                self._construirArbol( self.procesarPremisa(self.alias[premisa]), nodo)
            else:
                nodo.set(premisa)

                if(premisa not in self.preposicionesAtomicas):
                    self.preposicionesAtomicas.append(premisa)

                # añadirmos una referencia al nodo hoja
                self.refPreposicion.append(nodo)
     


    # Determina si el razonamiento es valido, si es valido retorna un array vacio
    # en caso contrario retorna un diccionario que contiene los valores de las presposiciones
    # atomicas que conducen a premisas ciertas y conclusion falsa
    def esValido(self):
        # total de filas de nuestra tabla de verdad
        totalFilas = 2**len(self.preposicionesAtomicas)

        # representa la cantidad de True o False que debe agregar al arreglo
        # del diccionario valoresPreposicionAtom antes de cambiar de valor
        # ejemplo: si tenemos p y q, entonces salto = 2, entonces en el arreglo de p
        # se agregaran dos True antes de cambiar a False
        salto = totalFilas/2

        # un diccionario donde asocia cada preposicion atomica con un arreglo de los valores que tendra
        # ejmeplo: si tenemos p y q, entonces valoresPreposicionAtom["p"] = [True, True, False, False]
        # y valoresPreposicionAtom["q"] = [True, False, True, False]
        valoresPreposicionAtom = {}
        
        # Construimos el diccionario mencionado anteriormente
        for preposicionAtomica in self.preposicionesAtomicas:
            if preposicionAtomica not in valoresPreposicionAtom:
                valoresPreposicionAtom[preposicionAtomica] = []

            cambiarValor = salto
            for  i in range(totalFilas):
                
                if cambiarValor > 0:
                    valor = True
                else:
                    valor = False
                    if cambiarValor <= -1*salto:
                        valor = True
                        cambiarValor = salto

                valoresPreposicionAtom[preposicionAtomica].append(valor)
                cambiarValor-=1
            salto/=2

        razonamientoEsValido = True
        for i in range(totalFilas):
            for ref in self.refPreposicion:
                ref.resultado = valoresPreposicionAtom[ref.key][i]

            if self.evaluar(self.raiz) is False:
               razonamientoInvalidoValores = {}
               for ref in self.refPreposicion:
                   razonamientoInvalidoValores[ref.key] = valoresPreposicionAtom[ref.key][i]
               return razonamientoInvalidoValores
               
        return []
    
    # Evualuamos la premisa con los valores asiganadas a las preposiciones atomicas
    def evaluar(self, nodo):

        # si la key no esta en evaluarTerminoEnlance significa que es una preposicion
        # atomica por lo tanto retornamos su valor
        if nodo.key not in self.evaluarTerminoEnlance:
            return nodo.resultado

        # hallamos el resultado de evaluar el resultado del nodo izq y nodo der 
        nodo.resultado = self.evaluarTerminoEnlance[nodo.key](self.evaluar(nodo.izq), self.evaluar(nodo.der))
    
        return nodo.resultado

class NodoPremisa:
    def __init__(self, terminoEnlance=None, sizePrmisas=0):
        # Almacena un termino de enlance o una preposicion atomica
        # si es una preposicion atomica estamos en una hoja
        self.key = terminoEnlance

        # alamcena los valores que puede tomar la preposiciones atomicas o
        # el resultado de evaluar el termino de enlace
        self.resultado = None

        # alamcena el hijo izq y der de cada nodo
        self.izq = self.der = None
    
    def set(self, valor):
        self.key = valor


