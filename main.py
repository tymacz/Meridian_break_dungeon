from Marchand import Marchand
from Personnages import Personnage
from Items import Arme, Armure, Potion, FioleDePoison
from Roles import Thief, Mage
from Moteur import GameEngine
from IA import ComportementPrudent  
from Salle import Coffre, Salle
from Sauvegarde import SaveManager
from VueConsole import VueConsole

if __name__ == "__main__":
    vue = VueConsole()
    print("🎮 Bienvenue dans le jeu de combat !\n")
    print("1. Nouvelle partie")
    print("2. Charger une partie")
    choix = input("Votre choix (1/2) : ")
    joueur = None

    if choix == "2":
        joueur = SaveManager.charger()
    if joueur is None:
        nom_joueur = input("Entrez le nom de votre personnage : ")
        joueur = Personnage(name=nom_joueur, role=Thief())
        SaveManager.sauvegarder(joueur)
        
    forgeron = Marchand("Balthazar le Forgeron")
    forgeron.inventaire.ajouter(Potion(nom="Potion de Soin", poids=0.5, valeur=30, soin=30))
    forgeron.inventaire.ajouter(Arme(nom="Hache de Guerre", poids=6.0, valeur=120, degats_bonus=20))
    entree = Salle("L'Entrée Sombre", "L'air est lourd. Des toiles d'araignées recouvrent les murs.")
    couloir = Salle("Le Couloir Humide", "L'eau goutte du plafond. Vous entendez des bruits au Nord.")
    salle_boss = Salle("La Salle du Trône", "Une immense pièce éclairée par des torches vacillantes.")
    armurerie = Salle("L'Armurerie Abandonnée", "Des râteliers vides jonchent le sol.")
    boutique_salle = Salle("L'Échoppe Sécurisée", "Un feu crépite dans l'âtre. L'endroit a l'air sûr.")
    boutique_salle.marchand = forgeron
    # 3. Le Maillage (Le Graphe)
    # Entrée <-> (Nord) <-> Couloir
    entree.lier("Nord", couloir)

    # Couloir <-> (Nord) <-> Salle du Boss
    couloir.lier("Nord", salle_boss)

    # Couloir <-> (Est) <-> Armurerie
    couloir.lier("Est", armurerie)
    couloir.lier("Ouest", boutique_salle)
    boss = Personnage("Seigneur Démon", Mage())
    boss.role.pv = 80
    boss.level = 5
    joueur.role.pv = 200
    boss.ia = ComportementPrudent()

    salle_boss.ennemi = boss

    plastron_or = Armure(
        nom="Plastron en Or",
        poids=15.0,
        valeur=200,
        defense_bonus=20,
        emplacement="Torse",
    )
    armurerie.coffre = Coffre(contenu_item=plastron_or)
    couloir.coffre = Coffre(contenu_argent=50)
    # 3. Lancement du moteur de jeu
    moteur = GameEngine(joueur=joueur, ennemi=boss)
    moteur.lancer_exploration(salle_depart=entree)
