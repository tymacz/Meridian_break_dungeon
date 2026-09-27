from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Personnages import Personnage

class Effet(ABC):
    def __init__(self, nom: str, duree: int):
        self.nom = nom
        self.duree = duree  # Nombre de tours avant disparition

    @abstractmethod
    def appliquer(self, cible: "Personnage"):
        """Applique l'effet sur la cible et réduit la durée."""
        pass

# Implémentation concrète : Le Poison
class Poison(Effet):
    def __init__(self, duree: int = 3, degats_par_tour: int = 5):
        super().__init__(nom="Poison", duree=duree)
        self.degats = degats_par_tour

    def appliquer(self, cible: "Personnage"):
        print(f"🤢 {cible.name} souffre du poison et perd {self.degats} PV !")
        cible.recevoir_degats(self.degats)
        self.duree -= 1