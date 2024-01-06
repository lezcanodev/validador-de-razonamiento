
#Para limpiar el cmd entre cada entrada
import os
from index import ArbolPremisa 


class AppRazonamiento:
    def __init__(self):
        # Contiene las preposiciones atomicas ingresadas por el usuario, ej: "Hace calor"
        self._preposicionesAtomicas = []
        # Contiene los simbolos que representa a cada preposicion atomica, ej: p
        self._simbolosPreposicionesAtomicas = []
        # Contiene las premisas ingresadas por el usuario
        self._premisas = []
        # Contiene la conclusion del razonamiento
        self.conclusion = ""
    
    

    # Crea un bucle donde el usuario ingresa las preposiciones atomicas hasta que ingrese -1
    def ingresarPreposiciones(self):        
        while True: 
            os.system('cls')  
            print()     
            print("   1. Ingrese -1 para agregar la conclusion")
            print("   2. Formato de la preposiciones: [simbolo]:[preposicion atomica (opcional)] ej: p: Hoy es sabado ")

            print("")   
            self.printPreposiciones()
            print("")
            preposicionAtomica = input('Ingrese una prepo. atomica: ')
            if preposicionAtomica == '-1': break
            simbolo = preposicionAtomica.split(":")[0]
            preposicionAtomica = preposicionAtomica.split(":")[1]
            self._preposicionesAtomicas.append(preposicionAtomica.strip())
            self._simbolosPreposicionesAtomicas.append(simbolo.strip())

        
    # imprime las preposiciones atomicas
    def printPreposiciones(self):
        print("Preposiciones atomicas")
        print("----------------------")
        for i in range(len(self._preposicionesAtomicas)):
            print("\t", self._simbolosPreposicionesAtomicas[i],": ",self._preposicionesAtomicas[i])

    # imprime las premisas
    def printPremisas(self):
        print("Premisas")
        print("---------")
        for i in range(len(self._premisas)):
            print(f'\t p{i+1}: ', self._premisas[i])
    
    # imprime el razonamiento
    def printRazonamiento(self):
        os.system('cls') 
        print("Razonamiento")
        print("------------")
        print()

        mayorLongitudPremisa = 0
        for premisa in self._premisas:
            mayorLongitudPremisa = mayorLongitudPremisa if mayorLongitudPremisa > len(premisa) else len(premisa)
            print(" P: ", premisa)

        print(" ", end="")
        for i in range(mayorLongitudPremisa+4):
            print("-", end="")

        print("\n C: ",self.conclusion)

    # Crea un bucle donde el usuario ingresa las premisas y cuando ingresa -1 se le pide la conclusion y finaliza el bucle
    def ingresarPremisas(self):
        while True:
            os.system('cls')
            print() 
            print("   1. Ingrese -1 para agregar la conclusion")
            print("   2. Simbolos:  \n\t^ (conjuncion)\n\tv (disyuncion)\n\t-> (implicacion)\n\t<-> (doble impli.)\n\t! (negacion) ")
            print("   3. ejemplos premisas: p -> q, (p->r) v s, !r ")
            print()
            self.printPreposiciones()
            self.printPremisas()
            print()
            premisa = input('Ingrese una premisa: ')
            if(premisa == '-1'): break
            self._premisas.append(premisa)


        self.conclusion = input('Ingrese una conclusion: ')

    # Verficia si el razonamiento es valido, hallando primero la condicional correspondiente y luego la evaluamos
    def  esRazonamientoValido(self):
        condicionalCorrespondiente = ""

        for i in range(len(self._premisas)):
            condicionalCorrespondiente += f'({self._premisas[i]})'    
            if i < len(self._premisas)-1: condicionalCorrespondiente+='^'
        condicionalCorrespondiente += f'->({self.conclusion})'


        a = ArbolPremisa()
        a.add(condicionalCorrespondiente) 
        resultado = a.esValido()
        if(len(resultado) == 0):
            print("El razonamiento es valido")
        else:
            print("El razonamiento es invalido, por que con los siguientes valores")
            print("conduce a premisas ciertas y conclusion falsa")
            for simboloPremisa in resultado.keys():
                print(" ",simboloPremisa,": ", resultado[simboloPremisa]) 

            


app = AppRazonamiento()
app.ingresarPreposiciones()
app.ingresarPremisas()
app.printRazonamiento()
app.esRazonamientoValido()