import sqlite3
import datetime

class Persona:
    def __init__(self, dni, apellido, nombre='', movil=''):
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
        self.movil= movil


def ingresa_visita(persona):
    """Guarda los datos de una persona al ingresar"""
    conn = sqlite3.connect('recepcion.db')

    q = f"""SELECT dni FROM personas WHERE dni = '{persona.dni}'"""

    resu = conn.execute(q)

    if resu.fetchone():
        print("ya existe")
    else:
        q = f"""INSERT INTO personas (dni, nombre, apellido, movil)
                VALUES ('{persona.dni}',
                        '{persona.nombre}',
                        '{persona.apellido}',
                        '{persona.movil}');"""
        print(q)
        conn.execute(q)
        conn.commit()
        
        destino = input("Ingrese destino> ")
        
        q = f"""INSERT INTO ingresos_egresos (dni, fechahora_in, fechahora_out, destino)
                    VALUES ('{persona.dni}',
                            '{datetime.datetime.now().replace(microsecond=0).isoformat()}',
                            'null',
                            '{destino}');"""
        conn.execute(q)
        conn.commit()
    
    conn.close()
    

def egresa_visita (dni):
    """Coloca fecha y hora de egreso al visitante con dni dado"""
    conn = sqlite3.connect('recepcion.db')
    
    q = f"""UPDATE ingresos_egresos SET fechahora_out = '{str(datetime.datetime.now().replace(microsecond=0).isoformat())}' WHERE dni = '{dni}'"""
    
    conn.execute(q)
    conn.commit()
    
    conn.close()


def lista_visitantes_en_institucion ():
    """Devuelve una lista de objetos Persona presentes en la institución"""
    conn = sqlite3.connect('recepcion.db')
    q = f"""SELECT *
            FROM personas
            INNER JOIN ingresos_egresos ON personas.dni = ingresos_egresos.dni
            WHERE ingresos_egresos.fechahora_out = 'null';"""

    resu = conn.execute(q)
    
    for fila in resu:
        print(fila)
    conn.close()


def busca_vistantes(fecha_desde, fecha_hasta, destino, dni):
    """ busca visitantes segun criterios """
    conn = sqlite3.connect('recepcion.db')

    q = f'''SELECT * 
             FROM personas 
             INNER JOIN ingresos_egresos ON personas.dni = ingresos_egresos.dni
             WHERE ingresos_egresos.fechahora_in LIKE '{fecha_desde}%' OR ingresos_egresos.fechahora_out LIKE '{fecha_hasta}%' OR ingresos_egresos.destino = '{destino}' OR ingresos_egresos.dni = '{dni}';
          '''

    resu = conn.execute(q)
    
    for fila in resu:
        print(fila)
    conn.close()


def iniciar():
    conn = sqlite3.connect('recepcion.db')

    qry = '''CREATE TABLE IF NOT EXISTS
                            personas
                    (dni TEXT NOT NULL PRIMARY KEY,
                     nombre   TEXT,
                     apellido TEXT  NOT NULL,
                     movil    TEXT  NOT NULL
           );'''

    conn.execute(qry)

    qry = '''CREATE TABLE IF NOT EXISTS
                            ingresos_egresos
                    (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                     dni TEXT NOT NULL,
                     fechahora_in TEXT  NOT NULL,
                     fechahora_out TEXT,
                     destino TEXT
           );'''

    conn.execute(qry)

if __name__ == '__main__':
    iniciar()

    # ingresa_visita(Persona('28123456', 'Álvarez', 'Ana', '02352-456789'))
    # ingresa_visita(Persona('48285192', 'Gimenez', 'Guillermo', '16327-289304'))
    # ingresa_visita(Persona('20481024', 'Pérez', 'Flor', '72949-928512'))
    # ingresa_visita(Persona('34929192', 'Torres', 'Mateo', '72949-192895'))
    # ingresa_visita(Persona('46204923', 'Bertoli', 'Lucas', '19243-123321'))
    
    # egresa_visita(20481024)
    # egresa_visita(46204923)
    
    # Imprimir a todas las personas que aún no hayan salido de la institución
    print("Lista de visitantes que aún se encuentran en la institución: ")
    lista_visitantes_en_institucion()

    print('\n\n\n')

    # Imprimir a todas las personas, sin importar si se encuentren o no en la institución, en los que alguno de los datos coincidan
    print("Lista de visitantes según los criterios dados: ")
    busca_vistantes("2022-5-11T", "2022-5-11T", "Secretaría", 3492192)
