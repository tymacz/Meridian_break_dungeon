from Roles import Role
from Inventaires import Inventaire
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from Items import Item
    from IA import ComportementIA
    from Effets import Effet

class Personnage:
    def __init__(self, name: str, role: Role):
        self.name = name
        self.role = role
        self.level = 1
        self.exp = 0
        self.money = 0
        self.inventaire = Inventaire(capacite_max=15.0)
        self.equipements: dict[str, Optional["Item"]] = {
            "Arme": None,
            "Tete": None,
            "Torse": None,
        }
        self.ia: Optional["ComportementIA"] = None
        self.effets_actifs: list['Effet'] = [] 

    def __str__(self) -> str:
        return f"Hi, I'm {self.name}, my class is {self.role.name} and I'm level {self.level}"

    @property
    def attaque_totale(self) -> int:
        arme = self.equipements["Arme"]
        bonus = arme.degats_bonus if arme else 0
        return self.role.attack + bonus
    @property  
    def defense_totale(self) -> int:
        bonus = 0
        for slot in ["Tete", "Torse"]:
            piece = self.equipements[slot]
            if piece:
                bonus += piece.defense_bonus
        return self.role.defense + bonus

    def equiper(self, item: 'Item', slot: str):
        ancien = self.equipements.get(slot)
        if ancien:
            print(f"🔄 {self.name} déséquipe {ancien.nom}.")
            self.inventaire.ajouter(ancien)

        self.equipements[slot] = item
        print(f"🛡️ {self.name} s'équipe de {item.nom} ({slot}) !")
        print(f"📊 Stats actuelles -> Attaque: {self.attaque_totale} | Défense: {self.defense_totale}")

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

    def ajouter_effet(self, effet: 'Effet'):
        self.effets_actifs.append(effet)
        print(f"⚠️ {self.name} est maintenant affecté par {effet.nom} pour {effet.duree} tours !")

    def subir_effets(self):
        if not self.effets_actifs:
            return

        print(f"\n--- 🌀 Effets de statut sur {self.name} ---")
        for effet in self.effets_actifs[:]:
            effet.appliquer(cible=self)

            if effet.duree <= 0:
                print(f"✨ L'effet {effet.nom} s'est dissipé sur {self.name}.")
                self.effets_actifs.remove(effet)
    def gagner_exp(self, montant: int):
        self.exp += montant
        print(f"🌟 {self.name} gagne {montant} points d'expérience !")

        palier = self.level*100
        while self.exp >= palier:
            self.exp -= palier
            self.monter_niveau()
            palier = self.level *100

    def monter_niveau(self):
        self.level += 1
        print(f"🎉 NIVEAU SUPÉRIEUR ! {self.name} atteint le niveau {self.level} !")

        self.role.pv += 15
        self.role.attack += 5
        self.role.defense += 2

        print(f"💪 Statistiques mises à jour : PV={self.role.pv}, Attaque={self.role.attack}, Défense={self.role.defense}")

    def afficher_equipement(self):
        print(f"\n" + "=" * 30)
        print(f"🛡️ ÉQUIPEMENT DE {self.name.upper()} 🛡️")
        print("=" * 30)

        for slot, piece in self.equipements.items():
            nom = piece.nom if piece else "--- Vide ---"
            print(f"[{slot.ljust(5)}] : {nom}")

        print("-" * 30)
        print(f"⚔️ Attaque Totale : {self.attaque_totale}")
        print(f"🛡️ Défense Totale : {self.defense_totale}")
        print("=" * 30 + "\n")

    def to_dict(self) -> dict:
        """Convertit le personnage en dictionnaire pour la sérialisation."""
        return {
            "name": self.name,
            "level": self.level,
            "exp": self.exp,
            "money": self.money,
            "role": self.role.to_dict(),
            "inventaire": [item.to_dict() for item in self.inventaire.items],
        }
