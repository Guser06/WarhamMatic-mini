import random
import numpy as np

global dados_aux

# Funcion para tirar dados

def Dados(n_dados):
    global res_dados
    res_dados=[]
    res_dados = np.array([random.randint(1, 6) for _ in range(1, (n_dados+1))])
    return res_dados

# Generar números que representen los dados tirados para iniciar la partida
t = 0

while True:
    dados = Dados(10)
    Dado_TurnoSM = random.choice(dados)
    print(f"Dado Space Marines {Dado_TurnoSM}")
    Dado_TurnoTy = random.choice(dados)
    print(f"Dado Tyranidos {Dado_TurnoTy}")
    if Dado_TurnoSM < Dado_TurnoTy:
        print("Comienzan los Tyranidos")
        t = 1
        break
    elif Dado_TurnoSM > Dado_TurnoTy:
        print("Comienzan los Marines Espaciales")
        t = 2
        break

dados_aux = []

# Nombres de cada estadística
StatsTx = ["Movimiento", "Resistencia", "Salvación",
           "Heridas", "Liderazgo", "Control de objetivo"]
ArmaTx = ["Alcance", "No. de Ataques",
          "Habilidad", "Fuerza", "Perforación", "Daño"]

# Estructura base para los ejercitos
# Clase Base Unidad


class Individuo:
    def __init__(self, nombre, stats_base, rango=None, mele=None, dmg=0):
        self.nombre = nombre
        self.stats_base = stats_base
        self.rango = rango or [0] * 6  # Arma de rango
        self.mele = mele or [0] * 6  # Arma cuerpo a cuerpo
        self.dmg = dmg
        self.vivo = True

    def D_stats(self):
        return dict(zip(StatsTx, self.stats_base))

    def D_Arma(self):
        return dict(zip(ArmaTx, self.rango))

    def D_Mele(self):
        return dict(zip(ArmaTx, self.mele))

    def recibir_dano(self, dano):
        self.dmg += dano
        if self.dmg >= self.stats_base[3]:  # Si daño >= heridas
            self.vivo = False
            print(f"{self.nombre} ha muerto.")

    def __repr__(self):
        estado = "Vivo" if self.vivo else "Muerto"
        return f"{self.nombre} ({estado}): Stats {self.D_stats()}"

# Clase Grupo


class Grupo:
    def __init__(self, nombre):
        self.nombre = nombre
        self.miembros = []
        self.mov = 0
        self.atk = 0

    def agregar(self, unidad):
        self.miembros.append(unidad)

    def eliminar_muertos(self):
        self.miembros = [
            Individuo for tropa in self.miembros if Individuo.vivo == False]

    def __repr__(self):
        return f"{self.nombre}:\n" + "\n".join(str(miembro) for miembro in self.miembros)

# Clases de tropas
# Marines
# Clase Capitan en armadura exterminador


class Capitan(Individuo):
    def __init__(self):
        super().__init__("Capitán en armadura Exterminador", [
            5, 5, 2, 6, 4, 1], [24, 2, 2, 4, 0, 1], [0, 5, 2, 5, 2, 2])

# Clase Marine Exterminador


class Exterminador(Individuo):
    def __init__(self, num):
        super().__init__(f"Marine Exterminador #{num}", [
            5, 5, 2, 3, 5, 1], [24, 2, 3, 4, 0, 1], [0, 3, 4, 8, 2, 2])

# Clase Sargento en armadura Exterminador


class SgtExt(Individuo):
    def __init__(self):
        super().__init__("Sargento Exterminador", [5, 5, 2, 3, 5, 1], [
            24, 2, 3, 4, 0, 1], [0, 3, 3, 5, 2, 1])

# Clase Exterminador con cañon de asalto


class ExtAsa(Individuo):
    def __init__(self):
        super().__init__("Marine Exterminador con cañon de asalto", [
            5, 5, 2, 3, 5, 1], [24, 6, 3, 6, 0, 1], [0, 3, 4, 8, 2, 2])

# Clase Marine Infernus


class Infernus(Individuo):
    def __init__(self, num):
        super().__init__(f"Marine Infernus #{num}", [6, 4, 3, 2, 6, 1], [
            12, random.choice(dados), 6, 5, 0, 1], [0, 3, 3, 4, 0, 1])

# Clase Sargento Infernus


class SgtInf(Individuo):
    def __init__(self):
        super().__init__("Sargento Infernus", [6, 4, 3, 2, 6, 1], [
            12, 1, 3, 4, 0, 1], [0, 3, 3, 4, 0, 1])

# Tyranidos
# Clase Termagante Tyranido


class Termagante(Individuo):
    def __init__(self, num):
        super().__init__(f"Termagante #{num}", [6, 3, 5, 1, 9, 2], [
            18, 1, 4, 5, 0, 1], [0, 1, 4, 3, 0, 1])

# Clase Enjambre devorador Tyranido


class EnjDevorador(Individuo):
    def __init__(self, num):
        super().__init__(f"Enjambre Devorador #{num}", [
            6, 2, 5, 4, 10, 1], rango=None, mele=[0, 4, 5, 2, 0, 1])

# Clase Saltador


class VonRyan(Individuo):
    def __init__(self, num):
        super().__init__(f"Saltador de Von Ryan #{num}", [
            10, 5, 4, 3, 9, 1], rango=None, mele=[0, 6, 3, 6, 1, 1])

# Clase Tyranido Primus


class Primus(Individuo):
    def __init__(self):
        super().__init__("Tyranido Alado Primus", [
            12, 5, 4, 5, 4, 1], rango=None, mele=[0, 6, 2, 5, 1, 1])

# Clase Psicofago Tyranido


class Psicofago(Individuo):
    def __init__(self):
        super().__init__("Psicofago Tyranido", [8, 9, 3, 10, 4, 3], [
            12, random.choice(dados), 1, 6, 1, 1], [0, (random.choice(dados))+3, 3, 6, 1, 2])

# ----------------------------Crear objetos/tropas y grupos/unidades------------------------------------#

def Crear_unidades():

    global Uni_Tyra, Uni_SM

    # Crear unidades Termagantes
    termas1 = [Termagante(i) for i in range(1, 11)]
    enjambre1 = EnjDevorador(1)

    termas2 = [Termagante(j) for j in range(1, 11)]
    enjambre2 = EnjDevorador(2)

    # Crear grupos
    unidadT_5 = Grupo("Unidad Tyranida 5: Termagantes y Enjambre")
    unidadT_5.agregar(enjambre1)
    for terma in termas1:
        unidadT_5.agregar(terma)

    unidadT_4 = Grupo("Unidad Tyranida 4: Termagantes y Enjambre")
    unidadT_4.agregar(enjambre2)
    for Terma in termas2:
        unidadT_4.agregar(Terma)

    # Crear unidad Saltadores de Von Ryan
    VonRyan_ = [VonRyan(k) for k in range(1, 4)]
    unidadT_3 = Grupo("Unidad Tyranida 3: Saltadores de Von Ryan")
    for Von in VonRyan_:
        unidadT_3.agregar(Von)

    # Crear unidad Tyranido Primus
    Primus_ = Primus()
    unidadT_1 = Grupo("Unidad Tyranida 1: Tyranido Alado Primus")
    unidadT_1.agregar(Primus_)

    # Crear unidad Psicofago Tyranido
    Psicofago_ = Psicofago()
    unidadT_2 = Grupo("Unidad Tyranida 2: Psicofago Tyranido")
    unidadT_2.agregar(Psicofago_)

    # Crear unidades Space Marines
    # Capitan
    Capitan_ = Capitan()
    unidadSM_1 = Grupo("Unidad Marines 1: Capitán en Armadura Exterminador")
    unidadSM_1.agregar(Capitan_)

    # Exterminadores
    Exter = [Exterminador(l) for l in range(1, 4)]
    SgtExt_ = SgtExt()
    ExtAsa_ = ExtAsa()

    unidadSM_2 = Grupo("Unidad Marines 2: Marines Exterminadores")
    unidadSM_2.agregar(SgtExt_)
    unidadSM_2.agregar(ExtAsa_)
    for Ex in Exter:
        unidadSM_2.agregar(Ex)

    # Infernus
    Infer_ = [Infernus(z) for z in range(1, 5)]
    SgtInf_ = SgtInf()

    unidadSM_3 = Grupo("Unidad Marines 3: Marines Infernus")
    unidadSM_3.agregar(SgtInf_)
    for I in Infer_:
        unidadSM_3.agregar(I)

    # Verificar la creación correcta de unidades
    # Tyranidos
    Uni_Tyra = [unidadT_1, unidadT_2, unidadT_3, unidadT_4, unidadT_5]
    try:
        all(Uni_Tyra)
    except:
        Crear_Tyr = False
    else:
        Crear_Tyr = True

    # Space Marines
    Uni_SM = [unidadSM_1, unidadSM_2, unidadSM_3]
    try:
        all(Uni_SM)
    except:
        Crear_SM = False
    else:
        Crear_SM = True

    if Crear_SM == True and Crear_Tyr == True:
        print("Todas las unidades fueron creadas")


Crear_unidades()
# ---------------------------------Fin Creación de Unidades---------------------------------------------#

# ///Pruebas de unidades///
# Remover comillas para ejecutar
""""
print(unidadSM_1.nombre)
print("")
print(f"{unidadSM_2.miembros[0]}")
print("")
print(unidadT_5.nombre)
print("")
print(unidadT_5.miembros[0])
print("")
#Se espera la impresion de los nombres y miembros de unidades, esta sería la forma de acceder a
# las listas de unidades

print(SgtExt_.D_Mele())
print("")
#Se espera la impresion de las estadisticas cuerpo a cuerpo del sargento exterminador
print(SgtExt_.mele[1])
print("")
#Se espera la impresion de la primera estadistica del arma cuerpo a cuerpo del sargento exterminador
print(Psicofago_.vivo)
print("")
#Se espera la impresion del valor booleano, si es verdadero, el psicofago esta vivo
print(unidadSM_2.__repr__)
print("")
#Se espera la impresion de los miembros de la escuadra de exterminadores
print(Exter[1].nombre)
#Se espera la impresion del nombre del miembro #2 de la escuadra de exterminadores
print(Exter[1].mele[1])
#Se espera la impresion de la caracteristica no. de ataques del arma mele del exterminador 2
#Usando esta sintaxis con el resto de grupos/unidades, listas, etc. es posible comenzar a crear
#operaciones y funciones de interacciones entre las undades

print("\nSimulación de combate:")  #Solo asignar daño
unidadT_5.miembros[0].recibir_dano(4)  # Daño al enjambre
unidadT_5.miembros[1].recibir_dano(2)  # Daño a un termagante
print(unidadT_5)   #Ver estado de la unidad despues de recibir daño
print("")


print("\nSimulación de movimiento:")  #Solo mostrar datos
print(f"La unidad a mover sera: {unidadSM_1.nombre}")  #Nombre de la unidad
#Movimiento de la unidad
print(f"Se movera {unidadSM_1.miembros[0].stats_base[0]} pulgadas")
print("")
"""

# Funciones de interacciones

def Estatico(Unidad):
    if Unidad.mov >= 1:
        print(f"La {Unidad} se quedara estática ")
        print("No puedes mover mas esta unidad")
        Unidad.mov -= 1
        return Unidad.mov
    else:
        print("Ya haz movido demasiado la unidad como para hacer esto")
        return Unidad.mov


def Normal(Unidad):
    if Unidad.mov >= 1:
        print(f"La {Unidad.nombre} realizara un movimiento de maximo {Unidad.miembros[-1].stats_base[0]} pulgadas")
        Unidad.mov -= 1
        return Unidad.mov
    else:
        print("Ya haz movido demasiado la unidad como para hacer esto")
        return Unidad.mov


def Avance(Unidad):
    if Unidad.mov >= 2 and Unidad.atk >= 2:
        adicional = (Unidad.miembros[-1].stats_base[0])+random.choice(dados)
        print(f"La {Unidad.nombre} realizara movimiento adicional de maximo {
              adicional} pulgadas")
        print(f"La {Unidad} no podrá moverse mas, cargar o disparar")
        Unidad.mov -= 2
        Unidad.atk -= 2
        return Unidad.mov, Unidad.atk
    else:
        print("Ya haz movido demasiado la unidad como para hacer esto")
        return Unidad.mov, Unidad.atk


def Retroceder(Unidad):
    if Unidad.mov >= 2 and Unidad.atk >= 2:
        print(f"La {Unidad} retrocedera maximo {
              Unidad.miembros[-1].stats_base[0]} pulgadas para alejarse")
        print(f"La {Unidad} no podrá moverse mas, cargar o disparar")
        Unidad.mov -= 2
        Unidad.atk -= 2
        return Unidad.mov, Unidad.atk
    else:
        print("Ya haz movido o atacado demasiado con la unidad como para hacer esto")
        pass
        return Unidad.mov, Unidad.atk


def Ataque(Unidad):
    # ¿Puede atacar?
    if Unidad.atk >= 2:
        print(f"Elija una unidad a la que atacar cuerpo a cuerpo con {Unidad}, usando el numero:  ")
        for n in contra:
            print(f"{n.nombre}")
        # Seleccionar a que unidad atacar
        x = int(input())-1
        blanco = contra[x]
        print(f"La {Unidad.nombre} va a atacar a {blanco.nombre}")
        # Para cada tropa en la unidad tirar tantos dados como cualidad A del arma (cuantos ataques)
        for u in Unidad.miembros:
            print(f"Atacara la tropa {u.nombre}")
            res_dados = Dados(u.mele[1])
            # Para cada dado, filtrar si el dado es mayor o igual a cualidad HP del arma (el ataque impacta)
            for _ in res_dados:
                if (_) >= (u.mele[2]):
                    print(f"El ataque {_} fue lanzado")
                    dados_aux.append(_)
                    # Comparar resistencias y fuerza para cada uno de los ataques (Ver si los ataques hacen daño)
                    for d in dados_aux:
                        # Tirar un dado para saber si el ataque hiere
                        res_dados1 = Dados(1)
                        # Calcular tirada de salvación
                        S = (blanco.miembros[0].stats_base[2]) + (u.mele[4])
                        print(f"Salvacion de las tropas atacadas es {S}")
                        # Comparar fuerza y resistencia
                        if (u.mele[3]) > 2*(blanco.miembros[0].stats_base[1]):
                            # Comparar fuerza y resistencia con el dado tirado
                            if res_dados1[0] >= 2:
                                print("El ataque atravezo la defensa")
                                # Tirar dado de salvación
                                res_dados2 = Dados(1)
                                # Comparar dado con Salvación
                                if res_dados2[0] <= S:
                                    # Efectuar daño
                                    blanco.miembros[0].recibir_dano(
                                        u.mele[3])
                                    print("El ataque logro herir")
                                    blanco.eliminar_muertos()
                                # El ataque fallo
                                else:
                                    print("El ataque no logro herir")
                            else:
                                print("El ataque no logro herir")

                        elif (u.mele[3]) > (blanco.miembros[0].stats_base[1]) and (u.mele[3]) < 2*(blanco.miembros[0].stats_base[1]):
                            if res_dados1[0] >= 3:
                                res_dados2 = Dados(1)
                                print("El ataque atravezo la defensa")
                                if res_dados2[0] <= S:
                                    blanco.miembros[0].recibir_dano(
                                        u.mele[3])
                                    print("El ataque logro herir")
                                    blanco.eliminar_muertos
                                else:
                                    print("El ataque no logro herir")
                            else:
                                print("El ataque no logro herir")

                        elif (u.mele[3]) == (blanco.miembros[0].stats_base[1]):
                            if res_dados1[0] >= 4:
                                res_dados2 = Dados(1)
                                print("El ataque atravezo la defensa")
                                if res_dados2[0] <= S:
                                    blanco.miembros[0].recibir_dano(
                                        u.mele[3])
                                    print("El ataque logro herir")
                                    blanco.eliminar_muertos
                                else:
                                    print("El ataque no logro herir")
                            else:
                                print("El ataque no logro herir")

                        elif (u.mele[3]) < (blanco.miembros[0].stats_base[1]) and 2*(u.mele[3]) > (blanco.miembros[0].stats_base[1]):
                            if res_dados1[0] >= 5:
                                res_dados2 = Dados(1)
                                print("El ataque atravezo la defensa")
                                if res_dados2[0] <= S:
                                    blanco.miembros[0].recibir_dano(
                                        u.mele[3])
                                    print("El ataque logro herir")
                                    blanco.eliminar_muertos
                                else:
                                    print("El ataque no logro herir")
                            else:
                                print("El ataque no logro herir")

                        elif 2*(u.mele[3]) < (blanco.miembros[0].stats_base[1]):
                            if res_dados1[0] >= 6:
                                res_dados2 = Dados(1)
                                print("El ataque atravezo la defensa")
                                if res_dados2[0] <= S:
                                    blanco.miembros[0].recibir_dano(
                                        u.mele[3])
                                    print("El ataque logro herir")
                                    blanco.eliminar_muertos
                                else:
                                    print("El ataque no logro herir")
                            else:
                                print("El ataque no logro herir")
        print("Fin del de ataque")
        print("Asi queda la unidad objetivo")
        print("-----------------------------")
        print(blanco.__repr__())
        print("-----------------------------")
        Unidad.atk -= 1
        return Unidad.mov, Unidad.atk

    else:
        print("No puedes atacar cuerpo a cuerpo")
    return Unidad.mov, Unidad.atk


def Disparo(Unidad):
    # ¿Puede atacar?
    if Unidad.atk >= 1 and Unidad.miembros[-1].rango != None:
        print(f"Elija una unidad a la que disparar con {Unidad}, usando el numero:  ")
        for n in contra:
            print(f"{n.nombre}")
        # Seleccionar a que unidad atacar
        x = int(input())-1
        blanco = contra[x]
        print(f"La {blanco.nombre} esta a {Unidad.miembros[-1].rango[0]} de la {blanco.nombre}?")
        print(f"Ingrese S o N")
        v = input()
        if v == 'S' or 's':
            print(f"La {Unidad.nombre} va a atacar a {blanco.nombre}")
            # Para cada tropa en la unidad tirar tantos dados como cualidad A del arma (cuantos ataques)
            for u in Unidad.miembros:
                print(f"Atacara la tropa {u.nombre}")
                res_dados = Dados(u.rango[1])
                # Para cada dado, filtrar si el dado es mayor o igual a cualidad HP del arma (el ataque impacta)
                for _ in res_dados:
                    if int(_) >= (u.rango[2]):
                        print(f"El ataque {_} fue lanzado")
                        dados_aux.append(_)
                        # Comparar resistencias y fuerza para cada uno de los ataques (Ver si los ataques hacen daño)
                        for d in dados_aux:
                            # Tirar un dado para saber si el ataque hiere
                            res_dados1 = Dados(1)
                            # Calcular tirada de salvación
                            S = (blanco.miembros[0].stats_base[2]) + (u.rango[4])
                            print(f"Salvacion de las tropas atacadas es {S}")    

                            # Comparar fuerza y resistencia
                            if (u.rango[3]) > 2*(blanco.miembros[0].stats_base[1]):
                                # Comparar fuerza y resistencia con el dado tirado
                                if res_dados1[0] >= 2:
                                    print("El ataque atravezo la defensa")
                                    # Tirar dado de salvación
                                    res_dados2 = Dados(1)
                                    # Comparar dado con Salvación
                                    if res_dados2[0] <= S:
                                        # Efectuar daño
                                        blanco.miembros[0].recibir_dano(
                                        u.rango[3])
                                        print("El ataque logro herir")
                                        blanco.eliminar_muertos()
                                        # El ataque fallo
                                    else:
                                        print("El ataque no logro herir")
                                else:
                                    print("El ataque no logro herir")

                            elif (u.rango[3]) > (blanco.miembros[0].stats_base[1]) and (u.rango[3]) < 2*(blanco.miembros[0].stats_base[1]):
                                if res_dados1[0] >= 3:
                                    res_dados2 = Dados(1)
                                    print("El ataque atravezo la defensa")
                                    if res_dados2[0] <= S:
                                        blanco.miembros[0].recibir_dano(
                                        u.rango[3])
                                        print("El ataque logro herir")
                                        blanco.eliminar_muertos
                                    else:
                                        print("El ataque no logro herir")
                                else:
                                    print("El ataque no logro herir")

                            elif (u.rango[3]) == (blanco.miembros[0].stats_base[1]):
                                if res_dados1[0] >= 4:
                                    res_dados2 = Dados(1)
                                    print("El ataque atravezo la defensa")
                                    if res_dados2[0] <= S:
                                        blanco.miembros[0].recibir_dano(
                                        u.rango[3])
                                        print("El ataque logro herir")
                                        blanco.eliminar_muertos
                                    else:
                                        print("El ataque no logro herir")
                                else:
                                    print("El ataque no logro herir")

                            elif (u.rango[3]) < (blanco.miembros[0].stats_base[1]) and 2*(u.rango[3]) > (blanco.miembros[0].stats_base[1]):
                                if res_dados1[0] >= 5:
                                    res_dados2 = Dados(1)
                                    print("El ataque atravezo la defensa")
                                    if res_dados2[0] <= S:
                                        blanco.miembros[0].recibir_dano(
                                        u.rango[3])
                                        print("El ataque logro herir")
                                        blanco.eliminar_muertos
                                    else:
                                        print("El ataque no logro herir")
                                else:
                                    print("El ataque no logro herir")

                            elif 2*(u.rango[3]) < (blanco.miembros[0].stats_base[1]):
                                if res_dados1[0] >= 6:
                                    res_dados2 = Dados(1)
                                    print("El ataque atravezo la defensa")
                                    if res_dados2[0] <= S:
                                        blanco.miembros[0].recibir_dano(
                                        u.rango[3])
                                        print("El ataque logro herir")
                                        blanco.eliminar_muertos
                                    else:
                                        print("El ataque no logro herir")
                                else:
                                    print("El ataque no logro herir")
            print("Terminaron los disparos")
            print("Asi queda la unidad objetivo")
            print("-------------------------------")
            print(blanco.__repr__())
            print("-------------------------------")
            Unidad.atk -= 1
            return Unidad.mov, Unidad.atk
        
        else:
            print(f"La {Unidad.nombre} no puede atacar a la {blanco.nombre}")
            return Unidad.mov, Unidad.atk

    elif Unidad.atk < 1 and Unidad.miembros[-1].rango != None:
        print(f"Ya no puedes disparar con esta unidad")
        return Unidad.mov, Unidad.atk

    elif Unidad.miembros[-1].rango == None:
        print(f"Esta unidad no tiene arma a distancia para atacar")
        return Unidad.mov, Unidad.atk


def Carga(Unidad):
    # ¿Puede atacar?
    if Unidad.atk >= 1 and Unidad.mov >= 1:
        print(f"Elija una unidad contra la que cargar con {Unidad}, usando el numero:  ")
        for n in contra:
            print(f"{n.nombre}")
        # Seleccionar a que unidad atacar
        x = int(input())-1
        blanco = contra[x]
        print(f"Cual es la distancia entre la {Unidad.nombre} y la {blanco.nombre}?")
        print("Ingrese un numero")
        d = int(input())
        if d <= 12:
            res_dados = Dados(2)
            print(f"Los dados salieron {res_dados[0]+res_dados[1]}")
            if (res_dados[0]+res_dados[1]) < d:
                print(f"La carga de la {Unidad.nombre} ha fallado")
                Unidad.mov -= 1
                Unidad.atk -= 1
                return Unidad.mov, Unidad.atk
            
            else:
                print(f"La {Unidad.nombre} va a atacar a {blanco.nombre}")
                # Para cada tropa en la unidad tirar tantos dados como cualidad A del arma (cuantos ataques)
                for u in Unidad.miembros:
                    print(f"Atacara la tropa {u.nombre}")
                    res_dados = Dados(u.mele[1])
                    # Para cada dado, filtrar si el dado es mayor o igual a cualidad HP del arma (el ataque impacta)
                    for _ in res_dados:
                        if (_) >= (u.mele[2]):
                            print(f"El ataque {_} fue lanzado")
                            dados_aux.append(_)
                            # Comparar resistencias y fuerza para cada uno de los ataques (Ver si los ataques hacen daño)
                            for d in dados_aux:
                                # Tirar un dado para saber si el ataque hiere
                                res_dados1 = Dados(1)
                                # Calcular tirada de salvación
                                S = (blanco.miembros[0].stats_base[2]) + (u.mele[4])
                                print(f"Salvacion de las tropas atacadas es {S}")
                                # Comparar fuerza y resistencia
                                if (u.mele[3]) > 2*(blanco.miembros[0].stats_base[1]):
                                    # Comparar fuerza y resistencia con el dado tirado
                                    if res_dados1[0] >= 2:
                                        print("El ataque atravezo la defensa")
                                        # Tirar dado de salvación
                                        res_dados2 = Dados(1)
                                        # Comparar dado con Salvación
                                        if res_dados2[0] <= S:
                                            # Efectuar daño
                                            blanco.miembros[0].recibir_dano(
                                                u.mele[3])
                                            print("El ataque logro herir")
                                            blanco.eliminar_muertos()
                                            # El ataque fallo
                                        else:
                                            print("El ataque no logro herir")
                                    else:
                                        print("El ataque no logro herir")

                                elif (u.mele[3]) > (blanco.miembros[0].stats_base[1]) and (u.mele[3]) < 2*(blanco.miembros[0].stats_base[1]):
                                    if res_dados1[0] >= 3:
                                        res_dados2 = Dados(1)
                                        print("El ataque atravezo la defensa")
                                        if res_dados2[0] <= S:
                                            blanco.miembros[0].recibir_dano(
                                                u.mele[3])
                                            print("El ataque logro herir")
                                            blanco.eliminar_muertos
                                        else:
                                            print("El ataque no logro herir")
                                    else:
                                        print("El ataque no logro herir")

                                elif (u.mele[3]) == (blanco.miembros[0].stats_base[1]):
                                    if res_dados1[0] >= 4:
                                        res_dados2 = Dados(1)
                                        print("El ataque atravezo la defensa")
                                        if res_dados2[0] <= S:
                                            blanco.miembros[0].recibir_dano(
                                                u.mele[3])
                                            print("El ataque logro herir")
                                            blanco.eliminar_muertos
                                        else:
                                            print("El ataque no logro herir")
                                    else:
                                        print("El ataque no logro herir")

                                elif (u.mele[3]) < (blanco.miembros[0].stats_base[1]) and 2*(u.mele[3]) > (blanco.miembros[0].stats_base[1]):
                                    if res_dados1[0] >= 5:
                                        res_dados2 = Dados(1)
                                        print("El ataque atravezo la defensa")
                                        if res_dados2[0] <= S:
                                            blanco.miembros[0].recibir_dano(
                                                u.mele[3])
                                            print("El ataque logro herir")
                                            blanco.eliminar_muertos
                                        else:
                                            print("El ataque no logro herir")
                                    else:
                                        print("El ataque no logro herir")

                                elif 2*(u.mele[3]) < (blanco.miembros[0].stats_base[1]):
                                    if res_dados1[0] >= 6:
                                        res_dados2 = Dados(1)
                                        print("El ataque atravezo la defensa")
                                        if res_dados2[0] <= S:
                                            blanco.miembros[0].recibir_dano(
                                                u.mele[3])
                                            print("El ataque logro herir")
                                            blanco.eliminar_muertos
                                        else:
                                            print("El ataque no logro herir")
                                    else:
                                        print("El ataque no logro herir")
                print("Fin del de la carga")
                print("Asi queda la unidad objetivo")
                print("-----------------------------")
                print(blanco.__repr__())
                print("-----------------------------")
                Unidad.atk -= 1
                Unidad.mov -= 1
                return Unidad.mov, Unidad.atk

        else:
            print("No puedes cargar ahora, estas muy lejos")
            return Unidad.atk, Unidad.mov
        
    else:
        print("No puedes cargar ahora")
        return Unidad.atk, Unidad.mov


##Bucle principal de la partida##
cont_rondas = 0
max_rondas = 8

while True:

    if (t%2) == 0:
        unidades, contra = Uni_SM, Uni_Tyra
    else: unidades, contra = Uni_Tyra, Uni_SM
    
    if cont_rondas >= max_rondas or not any([unidad.vivo for grupo in Uni_SM + Uni_Tyra for unidad in grupo.miembros]):
        print("La partida ha terminado.")
        break

    #Modificar el orden a Movimiento, disparo, carga, combate#
    for Unidad in unidades:
        Unidad.mov = 2
        Unidad.atk = 2
        print(f"Elija un movimiento para hacer con {Unidad.nombre}:")
        accion = input()
        if accion.lower() in ['estatico', 'estatica']:
            Unidad.mov = Estatico(Unidad)
        elif accion.lower() in ['normal']:
            Unidad.mov = Normal(Unidad)
        elif accion.lower() in ['avance', 'extra']:
            Unidad.mov, Unidad.atk = Avance(Unidad)
        elif accion.lower() in ['retroceder', 'retrocede']:
            Unidad.mov, Unidad.atk = Retroceder(Unidad)
        else:
            print("La acción seleccionada es inválida.")

        print(f"Movimientos restantes: {Unidad.mov}, Ataques restantes: {Unidad.atk}")

    for Unidad in unidades:
        print(f"Elija disparar o no con {Unidad.nombre}, si ya está en combate cuerpo a cuerpo no podrá disparar")
        print(f"La unica excepción a esta regla es el Psicofago")
        accion = input()
        
        if accion.lower() in ['si', 'disparo', 'distancia', 'rango', 'disparar']:
            Unidad.atk = Disparo(Unidad)
        if accion.lower() in ['no', 'no disparar', 'estatico']:
            pass
        else:
            print("La acción seleccionada es inválida.")
        
        print(f"Movimientos restantes: {Unidad.mov}, Ataques restantes: {Unidad.atk}")

    for Unidad in unidades:
        print(f"Elija cargar o no con {Unidad.nombre}")
        accion = input()

        if accion.lower() in ['si', 'carga', 'cargar', 'ataque', 'atacar']:
            Unidad.mov, Unidad.atk = Carga(Unidad)
        elif accion.lower() in ['no', 'no cargar', 'no atacar']:
            pass
        else:
            print("La acción seleccionada es inválida.")

    for Unidad in unidades:
        print(f"Si la {Unidad.nombre} ya está en combate cuerpo a cuerpo, elija si debe pelear en este turno")
        accion = input()

        if accion.lower() in ['si', 'combate', 'mele', 'melee', 'cuerpo', 'cuerpo a cuerpo']:
            Unidad.atk = Ataque(Unidad)
        elif accion.lower() in ['no', 'no pelear', 'no mele', 'no cuerpo a cuerpo', 'no luchar']:
            pass
        else:
            print("La acción seleccionada es inválida.")

    if (t%2) == 0:
        Uni_SM, Uni_Tyra = unidades, contra
    else: Uni_Tyra, Uni_SM =  unidades, contra
    
    cont_rondas += 1
    t += 1