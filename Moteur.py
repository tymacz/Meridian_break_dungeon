from typing import TYPE_CHECKING
import time

from Salle import Coffre, Salle
from Sauvegarde import SaveManager

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

    def lancer_exploration(self, salle_depart: "Salle"):
        salle_actuelle = salle_depart

        print("\n🏰 B I E N V E N U E   D A N S   L E   D O N J O N 🏰")

        while self.joueur.role.pv > 0:
            print(f"\n" + "=" * 50)
            print(f"📍 Vous êtes dans : {salle_actuelle.nom}")
            print(f"   {salle_actuelle.description}")
            print("=" * 50)

            if salle_actuelle.marchand:
                m = salle_actuelle.marchand
                print(f"🏪 {m.nom} vous fait signe de vous approcher.")

                en_boutique = True
                while en_boutique:
                    print(f"\n🪙 Votre Or : {self.joueur.money} 🪙")
                    choix_boutique = input(
                        "Voulez-vous (A)cheter, (V)endre ou (Q)uitter la boutique ? "
                    ).upper()

                    if choix_boutique == "A":
                        m.afficher_catalogue()
                        if m.inventaire.items:
                            idx = input(
                                "Numéro de l'article à acheter (ou 'q' pour annuler) : "
                            )
                            if idx.isdigit():
                                m.vendre_au_joueur(int(idx), self.joueur)

                    elif choix_boutique == "V":
                        print("\n--- VOTRE INVENTAIRE ---")
                        self.joueur.inventaire.afficher()
                        if self.joueur.inventaire.items:
                            idx = input(
                                "Numéro de l'article à vendre (ou 'q' pour annuler) : "
                            )
                            if idx.isdigit():
                                m.racheter_du_joueur(int(idx), self.joueur)

                    elif choix_boutique == "Q":
                        print(f"👋 {m.nom} vous salue : 'Revenez quand vous voulez !'")
                        en_boutique = False

            if salle_actuelle.ennemi and salle_actuelle.ennemi.role.pv > 0:
                print(f"⚠️ Un {salle_actuelle.ennemi.name} bloque le passage !")

                self.ennemi = salle_actuelle.ennemi
                self.lancer_combat()

                if self.joueur.role.pv <= 0:
                    break

                enemi_mort = salle_actuelle.ennemi

                print(f"\n💀 {enemi_mort.name} a été vaincu ! Vous fouillez sa dépouille. . .")

                item_loot = enemi_mort.inventaire.items[0] if enemi_mort.inventaire.items else None

                salle_actuelle.coffre = Coffre(contenu_item=item_loot, contenu_argent=enemi_mort.money)
                salle_actuelle.ennemi = None 

                print(f"\nLa salle est maintenant sécurisée.")

            print("\nSorties disponibles :", ", ".join(salle_actuelle.sorties.keys()))
            choix = input(
                "Action (Nord/Sud/Est/Ouest) | 'I' (Inventaire) | 'E' (Équipement) | 'F' (Fouiller) | 'S' (Sauvegarder) : "
            ).capitalize()

            if choix == "E":
                self.joueur.afficher_equipement()

            elif choix == "I":
                self.joueur.inventaire.afficher()
                if self.joueur.inventaire.items:
                    action = input("Entrez le numéro de l'objet à utiliser,'J' suivi du numéro pour jeter (ex: J0) ou 'JALL' pour jeter tous les objets : ").upper()

                    if action.startswith("J") and action[1:].isdigit():
                        index = int(action[1:])
                        if 0 <= index < len(self.joueur.inventaire.items):
                            objet_jete = self.joueur.inventaire.items.pop(index)
                            print(f"🗑️ Vous avez jeté {objet_jete.nom}.")

                    elif action == "JALL":
                        while self.joueur.inventaire.items:
                            objet_jete = self.joueur.inventaire.items.pop()
                            print(f"🗑️ Vous avez jeté {objet_jete.nom}.")

                    elif action.isdigit() and 0 <= int(action) < len(self.joueur.inventaire.items):
                        objet = self.joueur.inventaire.items[int(action)]
                        objet.utiliser(lanceur=self.joueur, inventaire=self.joueur.inventaire)
            elif choix == "F":
                # Vérification de la présence d'un coffre
                if salle_actuelle.coffre:
                    salle_actuelle.coffre.ouvrir(self.joueur)
                else:
                    print("🔍 Vous fouillez la pièce mais ne trouvez rien d'intéressant.")
            elif choix == "S":
                SaveManager.sauvegarder(self.joueur)
            elif choix in salle_actuelle.sorties:
                salle_actuelle = salle_actuelle.sorties[choix]
                print(f"🚶 {self.joueur.name} se dirige vers le {choix}...")

            else:
                print("❌ Direction invalide ou mur bloquant.")

        print("\n💀 Fin de la partie. Merci d'avoir joué !")

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
            print("2. Utiliser une compétence")
            print("3. Ouvrir l'inventaire")
            choix = input("Votre choix (1/2/3) : ")

        if choix == "1":
            personnage.attaquer(adversaire)

        elif choix == "2":
            competences = personnage.role.competences
            if not competences:
                print("⚠️ Aucune compétence disponible ! Vous perdez votre tour.")
            else:
                for i,comp in enumerate(competences):
                    print(f"{i}. {comp.nom} (Coût : {comp.cout} {personnage.role.nom_ressource})")
                index = input("Entrez le numéro de la compétence à utiliser (ou 'q' pour annuler) : ")
                if index.isdigit() and 0 <= int(index) < len(competences):
                    reussite = competences[int(index)].executer(
                        lanceur=personnage, cible=adversaire
                    )
                    if not reussite:
                        print("Action annulée.")

        elif choix == "3":
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
                        utilisateur=personnage, inventaire=personnage.inventaire, cible=adversaire
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
                combattant.subir_effets()

                if cible.role.pv <= 0:
                    print(f"\n💀 {cible.name} s'effondre...")
                    break
                combattant.role.regenerer_ressource()
                # Le combattant joue son tour
                self.menu_action(personnage=combattant, adversaire=cible)
                time.sleep(1)  # Petite pause pour rendre le terminal lisible

                # Vérification de mort immédiate avant que le second puisse riposter
                if cible.role.pv <= 0:
                    print(f"\n💀 {cible.name} s'effondre...")
                    break

            self.tour_actuel += 1

        # Fin du combat
        if self.joueur.role.pv > 0:
            vainqueur = self.joueur
            perdant = self.ennemi
        else:
            vainqueur = self.ennemi
            perdant = self.joueur
        print(
            f"\n🏆 Vainqueur : {vainqueur.name} (PV restants : {vainqueur.role.pv}) !"
        )

        xp_donne = perdant.level * 50

        if vainqueur == self.joueur:
            vainqueur.gagner_exp(xp_donne)
        else : 
            print(f"☠️ {self.joueur.name} a péri. L'aventure s'arrête ici.")

        SaveManager.sauvegarder(self.joueur)
