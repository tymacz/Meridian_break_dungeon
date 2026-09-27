from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Personnages import Personnage


class ComportementIA(ABC):
    @abstractmethod
    def agir(self, entite: "Personnage", adversaire: "Personnage"):
        pass


# Stratégie 1 : Bête et méchant
class ComportementAgressif(ComportementIA):
    def agir(self, entite: "Personnage", adversaire: "Personnage"):
        print(f"😡 {entite.name} attaque sauvagement sans réfléchir !")
        entite.attaquer(adversaire)


class ComportementPrudent(ComportementIA):
    def agir(self, entite: "Personnage", adversaire: "Personnage"):
        if entite.role.pv < 30:
            soin = 25
            print(
                f"😰 {entite.name} se sent en danger ! Il incante un sort de guérison."
            )
            entite.recevoir_soin(soin)
        else:
            print(f"😈 {entite.name} vous observe de haut et lance son assaut !")
            entite.attaquer(adversaire)
