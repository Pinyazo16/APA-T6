class Alumno:
    """
    Clase usada para el tratamiento de las notas de los alumnos. Cada uno
    incluye los atributos siguientes:

    numIden:   Número de identificación. Es un número entero que, en caso
               de no indicarse, toma el valor por defecto 'numIden=-1'.
    nombre:    Nombre completo del alumno.
    notas:     Lista de números reales con las distintas notas de cada alumno.
    """

    def __init__(self, nombre, numIden=-1, notas=[]):
        self.numIden = numIden
        self.nombre = nombre
        self.notas = [nota for nota in notas]

    def __add__(self, other):
        """
        Devuelve un nuevo objeto 'Alumno' con una lista de notas ampliada con
        el valor pasado como argumento. De este modo, añadir una nota a un
        Alumno se realiza con la orden 'alumno += nota'.
        """
        return Alumno(self.nombre, self.numIden, self.notas + [other])

    def media(self):
        """
        Devuelve la nota media del alumno.
        """
        return sum(self.notas) / len(self.notas) if self.notas else 0

    def __repr__(self):
        """
        Devuelve la representación 'oficial' del alumno. A partir de copia
        y pega de la cadena obtenida es posible crear un nuevo Alumno idéntico.
        """
        return f'Alumno("{self.nombre}", {self.numIden!r}, {self.notas!r})'

    def __str__(self):
        """
        Devuelve la representación 'bonita' del alumno. Visualiza en tres
        columnas separas por tabulador el número de identificación, el nombre
        completo y la nota media del alumno con un decimal.
        """
        return f'{self.numIden}\t{self.nombre}\t{self.media():.1f}'

import re

def leeAlumnos(ficAlumnos):
    """
    Esta función lee un fichero con datos de alumnos y devuelve un diccionario con los datos leídos.

    >>> alumnos = leeAlumnos('alumnos.txt')
    >>> for alumno in alumnos:
    ...     print(alumnos[alumno])
    ...
    171     Blanca Agirrebarrenetse 9.5
    23      Carles Balcells de Lara 4.9
    68      David Garcia Fuster     7.0
    """

    diccAlumnos = {}

    expID = r'\s*(?p<id>\d+)\s+'
    expNom = r'(?p<nom>[\w\s]+?)\s+'
    expNotes = r'(?p<notes>[\d.\s]+)\s*'
    # expresion = re.compile(r'\s*(?p<id>\d+)\s+(?p<nom>[\w\s]+?)\s+(?p<notes>[\d.\s]+)\s*')
    expresion = re.compile(expID + expNom + expNotes)

    with open(ficAlumnos, 'rt') as fpAlumnos:
        for linea in fpAlumnos:
            match = expresion.search(linea)
            if match is not None:
                numIden = int(match['id'])
                nombre = match['nom']
                notas_str = match['notes']
                notas = list(map(float, notas_str))
                
                diccAlumnos[nombre] = Alumno(nombre, numIden, notas)
    return diccAlumnos

if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags= doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS)
