from Personnages import Personnage
from Items import Arme, Potion
from Roles import Thief, Mage
from Moteur import GameEngine
from IA import ComportementPrudent  

if __name__ == "__main__":
    # 1. Création des combattants
    joueur = Personnage("Maxence", Thief())
    boss = Personnage("Seigneur Démon", Mage())
    boss.role.pv = 80
    joueur.role.pv = 100
    boss.ia = ComportementPrudent()

    # 2. Préparation de l'inventaire du joueur
    epee = Arme(nom="Dague Empoisonnée", poids=2.0, valeur=100, degats_bonus=25)
    potion = Potion(nom="Potion de Soin Majeure", poids=0.5, valeur=50, soin=50)

    joueur.inventaire.ajouter(epee)
    joueur.inventaire.ajouter(potion)

    # 3. Lancement du moteur de jeu
    moteur = GameEngine(joueur=joueur, ennemi=boss)
    moteur.lancer_combat()
