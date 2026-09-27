from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from Effets import Poison

if TYPE_CHECKING:
    from Personnages import Personnage
    from Inventaires import Inventaire

class Item(ABC):
    def __init__(self, nom: str, poids: float, valeur: int):
        self.nom = nom
        self.poids = poids
        self.valeur = valeur

    @abstractmethod
    def utiliser(self, utilisateur: "Personnage", inventaire: "Inventaire", cible: "Personnage" = None):
        """Chaque objet définit comment il est utilisé."""
        pass
    
    def to_dict(self) -> dict:
        """Convertit l'objet en dictionnaire pour la sérialisation."""
        return {
            "nom": self.nom,
            "poids": self.poids,
            "valeur": self.valeur,
            "type": self.__class__.__name__,
        }


class Potion(Item):
    def __init__(self, nom: str, poids: float, valeur: int, soin: int):
        super().__init__(nom, poids, valeur)
        self.soin = soin

    def utiliser(self, utilisateur: "Personnage", inventaire: "Inventaire", cible: "Personnage" = None):
        utilisateur.recevoir_soin(self.soin)
        print(f"🧪 {utilisateur.name} boit {self.nom} et récupère {self.soin} PV.")
        inventaire.retirer(self)
    
    def to_dict(self) -> dict:
        """Convertit la potion en dictionnaire pour la sérialisation."""
        data = super().to_dict()
        data["soin"] = self.soin
        return data


class Arme(Item):
    def __init__(self, nom: str, poids: float, valeur: int, degats_bonus: int):
        super().__init__(nom, poids, valeur)
        self.degats_bonus = degats_bonus

    def to_dict(self) -> dict:
        """Convertit l'arme en dictionnaire pour la sérialisation."""
        data = super().to_dict()
        data["degats_bonus"] = self.degats_bonus
        return data

    def utiliser(self, utilisateur: "Personnage", inventaire: "Inventaire", cible: "Personnage" = None):
        utilisateur.equiper_arme(self)
        inventaire.retirer(self)


class Armure(Item):
    def __init__(
        self, nom: str, poids: float, valeur: int, defense_bonus: int, emplacement: str
    ):
        super().__init__(nom, poids, valeur)
        self.defense_bonus = defense_bonus
        self.emplacement = emplacement  # Doit être "Tete" ou "Torse"

    def utiliser(
        self,
        lanceur: "Personnage",
        inventaire: "Inventaire",
        cible: "Personnage" = None,
    ):
        if self.emplacement in lanceur.equipements:
            lanceur.equiper(self, self.emplacement)
            inventaire.retirer(self)
        else:
            print(
                f"❌ Impossible d'équiper {self.nom} : Emplacement '{self.emplacement}' inconnu."
            )

class Materiel(Item):
    # L'__init__ du parent (Item) est automatiquement hérité si on ne le redéfinit pas.

    def utiliser(self, utilisateur: "Personnage", inventaire: "Inventaire", cible: "Personnage" = None):
        # L'objet respecte le contrat abstrait, même si son effet est de ne rien faire.
        print(f"🔧 L'objet {self.nom} ne peut pas être consommé ou équipé directement.")


class FioleDePoison(Item):
    def __init__(self, nom: str = "Fiole de Poison", poids: float = 0.2, valeur: int = 20):
        super().__init__(nom=nom, poids=poids, valeur=valeur)

    def utiliser(
        self,
        utilisateur: "Personnage",
        inventaire: "Inventaire",
        cible: "Personnage" = None,
    ):
        if cible is not None:
            print(f"🧪 {utilisateur.name} jette une {self.nom} sur {cible.name} !")
            cible.ajouter_effet(Poison(duree=3, degats_par_tour=5))
            inventaire.retirer(self)
        else:
            print("❌ Impossible d'utiliser cet objet hors combat (aucune cible) !")
