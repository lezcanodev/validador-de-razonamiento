# Validador de razonamientos de logica preposicional
determina si un razonamiento de logica preposicional es valido o no valido. A partir del razonamiento se construye un arbol donde cada nodo represente un termino de enlance y los nodos hojas son las preposiciones
atomicas por ultimo se recorre el arbol recursivamente evaluando los resultados de evaluar las preposiciones atomicas con los terminos de enlance hasta llegar a la raiz,
el resultado final es un booleano true = razonamiento valido y false = razonamiento no valido
