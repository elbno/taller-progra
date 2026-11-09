from sqlalchemy import create_engine, String, Integer, Boolean, ForeignKey, Select
from sqlalchemy.orm import DeclarativeBase, relationship, Session, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Sala(Base):
    __tablename__ = "salas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    capacidad: Mapped[int] = mapped_column(Integer, nullable=False)
    disponible: Mapped[bool] = mapped_column(Boolean, default=True)

    reservas: Mapped[list["Reserva"]] = relationship("Reserva", back_populates="sala", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        estado = "disponible" if self.disponible else "No disponible"
        return f"Sala(id={self.id}, nombre='{self.nombre}', capacidad={self.capacidad}, estado='{estado}')"

class Reserva(Base):
    __tablename__ = "reservas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    estudiante: Mapped[str] = mapped_column(String(100), nullable=False)
    sala_id: Mapped[int] = mapped_column(Integer, ForeignKey(Sala.id), nullable=False)
    fecha: Mapped[str]= mapped_column(String(10), nullable=False)

    sala: Mapped["Sala"] = relationship("Sala", back_populates="reservas")


    def __repr__(self) -> str:
        return f"Reserva(id={self.id}, estudiante='{self.estudiante}', sala_id={self.sala_id}, fecha='{self.fecha}')"


engine = create_engine("sqlite:///reservas.db", echo=False)
Base.metadata.create_all(engine)


def insertar_sala(nombre: str, capacidad: int):
    if not nombre.strip():
        print("ERROR: El nombre de la sala no puede estar vacio")
        return

    if capacidad <= 0:
        print("ERROR: La capacidad debe ser mayor a 0")
        return

    with Session(engine) as session:
        with session.begin():
            nueva_sala = Sala(nombre=nombre.strip(), capacidad=capacidad, disponible=True)
            session.add(nueva_sala)
            print(f"OK: Sala '{nombre}' (Capacidad: {capacidad}) registrada con éxito.")

def consultar_salas():
    with Session(engine) as session:
        stmt = Select(Sala)
        salas = session.scalars(stmt).all()

        if not salas:
            print("\n No hay salas registradas")
            return

        print("\n Listado de salas:")
        for s in salas:
            estado = "disponible" if s.disponible else "no disponble"
            print(f"ID: {s.id}  Nombre: {s.nombre}  Capacidad: {s.capacidad}  Estado: {estado}")


def registrar_reserva(estudiante: str, sala_id: int, fecha:str):
    if not estudiante.strip():
        print("ERROR: Estudiante no puede estar vacio")
        return
    
    with Session(engine) as session:
        with session.begin():
            sala = session.get(Sala, sala_id)
        if not sala:
            print(f"ERROR: La sala con id {sala_id} no existe")
            return
        if not sala.disponible:
            print(f"ERROR: La sala seleccionada no esta disponible")
            return

def consultar_reserva():
    with Session(engine) as session:
        stmt = Select(Reserva)
        reservas = session.scalars(stmt).all()

        if not reservas:
            print("\n No hay reservas registradas")

        print("\n Listado de reservas:")
        for r in reservas:
            print(f"ID:{r.id}, estudiante: {r.estudiante}, Sala: {r.sala.nombre}, Fecha: {r.fecha} ")



def cancelar_reserva(id_reserva: int):
    with Session(engine) as session:
        with session.begin():
            reserva = reserva.get(Reserva, id_reserva)
            if not reserva:
                print("No se puede eliminar la reserva debido a que no existe")
                return

            sala = session.get(Sala, reserva.sala_id)
            if sala:
                sala.disponible = True
                
            session.delete(reserva)
            print(f"Ok, la reserva {id_reserva} ha sido borrada y vuelve a estar disponible")

def menu():
    print(" SISTEMA DE RESERVAS DE SALAS ")
    print("1. Registrar sala")
    print("2. Consultar salas")
    print("3. Registrar reserva")
    print("4. Consultar reservas")
    print("5. Cancelar reserva")
    print("0. Salir")

    opcion = input("Ingrese una opcion: ").strip()

    if opcion == "1":
        nombre = input("Ingrese el nombre")
        try:
            capacidad = int(input("Ingrese la capacidad: "))
            insertar_sala(nombre, capacidad)

        except ValueError:
            print("ERROR: La capacidad debe ser un numero entero")

    elif opcion == "2":
        consultar_salas()

    elif opcion == "3":
        try:
            sala_id = int(input("Ingrese el ID de la sala a reservar: "))
            estudiante = input("Nombre del estudiante: ")
            fecha = input("Fecha (AAAA/MM/DD): ")
            registrar_reserva(estudiante, sala_id, fecha)
        except ValueError:
            print("ERROR: El ID de la sala debe ser un numero entero.")

    elif opcion == "4":
        consultar_reserva()

    elif opcion == "5":
        try:
            id_reserva = int(input("Ingrese el ID de la reserva a cancelar: "))
            cancelar_reserva(id_reserva)
        except ValueError:
            print("ERROR: El ID de la reserva debe ser un numero entero.")

    elif opcion == "0":
        print("Saliendo...")


    else:
        print("Opcion no valida")

if __name__ == "__main__":
    menu()




        

        

