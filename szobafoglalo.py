from abc import ABC, abstractmethod
from datetime import datetime, timedelta

class Szoba(ABC):
    def __init__(self, ar, szobaszam):
        self._ar = ar
        self._szobaszam = szobaszam

    @property
    def ar(self):
        return self._ar

    @ar.setter
    def ar(self, ertek):
        self._ar = ertek

    @property
    def szobaszam(self):
        return self._szobaszam

    @abstractmethod
    def szoba_info(self):
        pass

class EgyagyasSzoba(Szoba):
    ALAPAR = 40000  

    def __init__(self, szobaszam, tengerpartranezo):
        super().__init__(EgyagyasSzoba.ALAPAR, szobaszam)
        self.tengerpartranezo = tengerpartranezo

    def szoba_info(self):
        return f"Egyágyas szoba, Szobaszám: {self.szobaszam}, Ár: {self.ar} Ft, Tengerparti nézet: {'Igen' if self.tengerpartranezo else 'Nem'}"

class KetagyasSzoba(Szoba):
    ALAPAR = 60000  

    def __init__(self, szobaszam, szin):
        super().__init__(KetagyasSzoba.ALAPAR, szobaszam)
        self.szin = szin

    def szoba_info(self):
        return f"Kétagyas szoba, Szobaszám: {self.szobaszam}, Ár: {self.ar} Ft, Szín: {self.szin}"


class Szalloda:
    def __init__(self, nev):
        self._nev = nev
        self._szobak = []
        self._foglalasok = []

    def szoba_hozzaadas(self, szoba):
        if not isinstance(szoba, Szoba):
            raise ValueError("Csak Szoba típusú objektum adható hozzá.")
        self._szobak.append(szoba)

    def foglalas_hozzaadas(self, szobaszam, datum):
        szoba = self.szoba_kereses(szobaszam)
        if szoba and all(f.szobaszam != szobaszam or f.datum != datum for f in self._foglalasok):
            foglalas = Foglalas(szobaszam, datum, szoba.ar)
            self._foglalasok.append(foglalas)
            return foglalas.ar
        else:
            return None

    def foglalas_torles(self, szobaszam, datum):
        for foglalas in self._foglalasok:
            if foglalas.szobaszam == szobaszam and foglalas.datum == datum:
                self._foglalasok.remove(foglalas)
                return True
        return False

    def foglalasok_listazasa(self):
        return self._foglalasok

    def szoba_kereses(self, szobaszam):
        for szoba in self._szobak:
            if szoba.szobaszam == szobaszam:
                return szoba
        return None

class Foglalas:
    def __init__(self, szobaszam, datum, ar):
        self.szobaszam = szobaszam
        self.datum = datum
        self.ar = ar

    def __repr__(self):
        return f"Foglalás - Szobaszám: {self.szobaszam}, Dátum: {self.datum}, Ár: {self.ar} Ft"

def datum_ellenorzes(datum):
    try:
        datetime.strptime(datum, '%Y-%m-%d')
        return datetime.strptime(datum, '%Y-%m-%d') >= datetime.now()
    except ValueError:
        return False

def main():
    szalloda = Szalloda("Hotel Relax")
    szalloda.szoba_hozzaadas(EgyagyasSzoba(101, True))
    szalloda.szoba_hozzaadas(KetagyasSzoba(102, "pink"))
    szalloda.szoba_hozzaadas(EgyagyasSzoba(103, False))
    szalloda.foglalas_hozzaadas(101, '2024-05-10')
    szalloda.foglalas_hozzaadas(102, '2024-05-10')
    szalloda.foglalas_hozzaadas(103, '2024-05-10')
    szalloda.foglalas_hozzaadas(101, '2024-05-11')
    szalloda.foglalas_hozzaadas(102, '2024-05-12')

    while True:
        print("\n1. Foglalás\n2. Lemondás\n3. Foglalások listázása\n4. Kilépés")
        valasztas = input("Válassz egy opciót: ")
        if valasztas == "1":
            szobaszam = int(input("Add meg a szobaszámot: "))  
            datum = input("Add meg a dátumot (ÉÉÉÉ-HH-NN formátumban): ")
            if datum_ellenorzes(datum):
                ar = szalloda.foglalas_hozzaadas(szobaszam, datum)
                if ar:
                    print(f"Foglalás rögzítve. Ár: {ar} Ft")
                else:
                    print("A szoba ezen a napon már foglalt vagy nem létezik.")
            else:
                print("Érvénytelen dátum.")
        elif valasztas == "2":
            szobaszam = int(input("Add meg a szobaszámot: "))  
            datum = input("Add meg a dátumot (ÉÉÉÉ-HH-NN formátumban): ")
            if szalloda.foglalas_torles(szobaszam, datum):
                print("Foglalás törölve.")
            else:
                print("Nincs ilyen foglalás.")
        elif valasztas == "3":
            foglalasok = szalloda.foglalasok_listazasa()
            for foglalas in foglalasok:
                print(foglalas)
        elif valasztas == "4":
            break

if __name__ == "__main__":
    main()

