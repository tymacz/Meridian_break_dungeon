from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Personnages import Personnage
    from Inventaires import Inventaire

class Item(ABC):
    def __init__(self, nom: str, poids: float, valeur: int):
        self.nom = nom
        self.poids = poids
        self.valeur = valeur

    @abstractmethod
    def utiliser(self, utilisateur: "Personnage"):
        """Chaque objet définit comment il est utilisé."""
        pass


class Potion(Item):
    def __init__(self, nom: str, poids: float, valeur: int, soin: int):
        super().__init__(nom, poids, valeur)
        self.soin = soin

    def utiliser(self, utilisateur: "Personnage", inventaire: "Inventaire"):
        utilisateur.recevoir_soin(self.soin)
        print(f"🧪 {utilisateur.name} boit {self.nom} et récupère {self.soin} PV.")
        inventaire.retirer(self)


class Arme(Item):
    def __init__(self, nom: str, poids: float, valeur: int, degats_bonus: int):
        super().__init__(nom, poids, valeur)
        self.degats_bonus = degats_bonus


    def utiliser(self, utilisateur: "Personnage", inventaire: "Inventaire"):
        utilisateur.equiper_arme(self)
        inventaire.retirer(self)


class Materiel(Item):
    # L'__init__ du parent (Item) est automatiquement hérité si on ne le redéfinit pas.

    def utiliser(self, utilisateur: "Personnage"):
        # L'objet respecte le contrat abstrait, même si son effet est de ne rien faire.
        print(f"🔧 L'objet {self.nom} ne peut pas être consommé ou équipé directement.")
