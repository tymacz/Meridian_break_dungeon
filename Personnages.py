from Roles import Role
from Inventaires import Inventaire
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from Items import Arme
    from IA import ComportementIA
    
class Personnage:
    def __init__(self, name: str, role: Role):
        self.name = name
        self.role = role
        self.level = 1
        self.exp = 0
        self.money = 0
        self.inventaire = Inventaire(capacite_max=15.0)
        self.arme_equipee: Optional["Arme"] = None
        self.ia: Optional["ComportementIA"] = None

    def __str__(self) -> str:
        return f"Hi, I'm {self.name}, my class is {self.role.name} and I'm level {self.level}"

    @property
    def attaque_totale(self) -> int:
        bonus = self.arme_equipee.degats_bonus if self.arme_equipee else 0
        return self.role.attack + bonus

    def equiper_arme(self, arme: 'Arme'):
        if self.arme_equipee is not None:
            ancienne_arme = self.arme_equipee
            print(f"🔄 {self.name} déséquipe {ancienne_arme.nom} pour la ranger.")
            self.inventaire.ajouter(ancienne_arme)
        self.arme_equipee = arme
        print(f"🛡️ {self.name} s'équipe de {arme.nom} ! Son attaque passe à {self.attaque_totale}.")

    def attaquer(self, cible: "Personnage"):
        self.role.offensive_action(attaquant=self, cible=cible)

    def recevoir_degats(self, montant: int):
        self.role.pv -= montant
        if self.role.pv < 0:
            self.role.pv = 0
        print(f"   -> Il reste {self.role.pv} PV à {self.name}.")

    def recevoir_soin(self, montant: int):
        self.role.pv += montant
        # Idéalement, il faudrait stocker les PV_MAX dans Role pour ne pas dépasser
        print(f"   -> Il reste {self.role.pv} PV à {self.name}.")
