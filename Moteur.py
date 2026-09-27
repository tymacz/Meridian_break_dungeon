from typing import TYPE_CHECKING
import time

if TYPE_CHECKING:
    from Personnages import Personnage


class GameEngine:
    def __init__(self, joueur: "Personnage", ennemi: "Personnage"):
        self.joueur = joueur
        self.ennemi = ennemi
        self.tour_actuel = 1

    def determiner_initiative(self) -> list["Personnage"]:
        """Retourne la liste des combattants triée par vitesse (le plus rapide en premier)."""
        if self.joueur.role.speed >= self.ennemi.role.speed:
            return [self.joueur, self.ennemi]
        return [self.ennemi, self.joueur]

    def menu_action(self, personnage: "Personnage", adversaire: "Personnage"):
        """Affiche le menu et gère l'action du joueur (si c'est un humain)."""
        print(f"\n--- C'est au tour de {personnage.name} ! ---")

        if personnage.ia is not None:
            personnage.ia.agir(entite=personnage, adversaire=adversaire)
            return

        # Menu pour le joueur
        choix = ""
        while choix not in ["1", "2"]:
            print("Que voulez-vous faire ?")
            print("1. Attaquer")
            print("2. Ouvrir l'inventaire")
            choix = input("Votre choix (1/2) : ")

        if choix == "1":
            personnage.attaquer(adversaire)

        elif choix == "2":
            personnage.inventaire.afficher()
            if personnage.inventaire.items:
                index = input(
                    "Entrez le numéro de l'objet à utiliser (ou 'q' pour annuler) : "
                )
                if index.isdigit() and 0 <= int(index) < len(
                    personnage.inventaire.items
                ):
                    objet = personnage.inventaire.items[int(index)]
                    objet.utiliser(
                        utilisateur=personnage, inventaire=personnage.inventaire
                    )
                else:
                    print(
                        "Action annulée, vous perdez votre tour à fouiller dans votre sac !"
                    )
            else:
                print("Votre sac est vide, vous perdez votre tour !")

    def lancer_combat(self):
        print(f"\n⚔️ LE COMBAT COMMENCE : {self.joueur.name} VS {self.ennemi.name} ⚔️")

        ordre = self.determiner_initiative()
        print(f"💨 {ordre[0].name} est le plus rapide et frappe en premier !")

        # La fameuse Game Loop
        while self.joueur.role.pv > 0 and self.ennemi.role.pv > 0:
            print(f"\n================ TOUR {self.tour_actuel} ================")

            for combattant in ordre:
                # Définir qui est la cible
                cible = self.ennemi if combattant == self.joueur else self.joueur

                # Le combattant joue son tour
                self.menu_action(personnage=combattant, adversaire=cible)
                time.sleep(1)  # Petite pause pour rendre le terminal lisible

                # Vérification de mort immédiate avant que le second puisse riposter
                if cible.role.pv <= 0:
                    print(f"\n💀 {cible.name} s'effondre...")
                    break

            self.tour_actuel += 1

        # Fin du combat
        vainqueur = self.joueur if self.joueur.role.pv > 0 else self.ennemi
        print(
            f"\n🏆 Vainqueur : {vainqueur.name} (PV restants : {vainqueur.role.pv}) !"
        )
