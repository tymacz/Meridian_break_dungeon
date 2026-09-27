from typing import TYPE_CHECKING
from Inventaires import Inventaire

if TYPE_CHECKING:
    from Personnages import Personnage
    from Items import Item

class Marchand:
    def __init__(self, nom: str):
        self.nom = nom
        self.inventaire = Inventaire(capacite_max=100.0) # Le marchand a de la place

    def afficher_catalogue(self):
        print(f"\n" + "="*40)
        print(f"🛒 {self.nom.upper()} - CATALOGUE")
        print("="*40)
        if not self.inventaire.items:
            print("   Le marchand n'a plus rien à vendre !")
        else:
            for i, item in enumerate(self.inventaire.items):
                print(f"[{i}] {item.nom} (Poids: {item.poids}kg) - Prix: {item.valeur} 🪙")
        print("="*40)

    def vendre_au_joueur(self, index: int, joueur: "Personnage"):
        if index < 0 or index >= len(self.inventaire.items):
            print("❌ Article invalide.")
            return

        item = self.inventaire.items[index]

        # Vérification de l'or
        if joueur.money < item.valeur:
            print(f"❌ Vous n'avez pas assez d'or ! (Il vous manque {item.valeur - joueur.money} 🪙)")
            return

        # Vérification du poids dans l'inventaire du joueur
        if joueur.inventaire.poids_actuel + item.poids > joueur.inventaire.capacite_max:
            print("❌ Votre inventaire est trop lourd pour porter cet objet !")
            return

        # Transaction
        joueur.money -= item.valeur
        self.inventaire.retirer(item)
        joueur.inventaire.ajouter(item)
        print(f"✅ Vous avez acheté {item.nom} pour {item.valeur} 🪙.")

    def racheter_du_joueur(self, index_inventaire: int, joueur: "Personnage"):
        if index_inventaire < 0 or index_inventaire >= len(joueur.inventaire.items):
            print("❌ Article invalide dans votre inventaire.")
            return

        item = joueur.inventaire.items[index_inventaire]
        # Le marchand rachète l'objet à sa pleine valeur (ou tu peux appliquer un ratio, ex: item.valeur // 2)
        prix_revente = item.valeur

        # Transaction
        joueur.inventaire.retirer(item)
        self.inventaire.ajouter(item)
        joueur.money += prix_revente
        print(f"✅ Vous avez vendu {item.nom} pour {prix_revente} 🪙.")