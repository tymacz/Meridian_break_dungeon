from typing import Optional, TYPE_CHECKING

from Marchand import Marchand


if TYPE_CHECKING:
    from Personnages import Personnage
    from Items import Item

class Salle:
    def __init__(self, nom: str, description: str):
        self.nom = nom
        self.description = description

        self.sorties: dict[str, "Salle"] = {}
        self.ennemi: Optional["Personnage"] = None
        self.coffre: Optional["Item"] = None
        self.marchand: Optional["Marchand"] = None

    def lier(self, direction: str, autre_salle: "Salle", bidirectionnel: bool = True):
        """Connecte cette salle à une autre dans la direction indiquée."""
        self.sorties[direction] = autre_salle

        if bidirectionnel:
            # Déduction de la direction opposée
            opposes = {"Nord": "Sud", "Sud": "Nord", "Est": "Ouest", "Ouest": "Est"}
            if direction in opposes:
                autre_salle.sorties[opposes[direction]] = self


class Coffre:
    def __init__(self, contenu_item: Optional["Item"] = None, contenu_argent: int = 0):
        self.item = contenu_item
        self.argent = contenu_argent
        self.est_ouvert = False 
        
    def ouvrir(self, joueur: "Personnage"):
        if self.est_ouvert:
            print("📦 Ce coffre a déjà été vidé.")
            return

        print("\n🎁 Vous forcez la serrure du coffre...")
        self.est_ouvert = True

        if self.item:
            joueur.inventaire.ajouter(self.item)
        elif self.argent > 0:
            joueur.money += self.argent
            print(
                f"💰 Vous trouvez {self.argent} pièces d'or ! (Total: {joueur.money} 🪙)"
            )
        else:
            print("💨 Le coffre est vide ! Quelle arnaque.")
