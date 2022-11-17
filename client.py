from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import (
    QApplication,
    QDesktopWidget,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QWidget,
)
import pdb, requests, sys, validators, webbrowser

""" ------------------------------------------ """
""" On trie les imports par ordre alphabétique """
""" ------------------------------------------ """


class MainWindow(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.zone_texte_longueur = 150
        self.zone_texte_largeur = 30
        
        self.initUI()


        
    def initUI(self):

        self.setWindowTitle("IP Logger")                # On donne le titre de la fenetre
        self.setWindowIcon(QtGui.QIcon('logo.png'))     # On met un beau logo
        self.resize(400,400)                            # On redéfinit la taille de la fenetre en 400 par 400
        self.centrer()                                  # On appelle la fonction pour centrer la fenetre
        
        
        self.zone_ip()      # On appelle les fonctions permettant d'afficher la zone de texte correspondant à l'IP
        self.zone_api()     # On appelle les fonctions permettant d'afficher la zone de texte correspondant à l'API
        self.zone_host()    # On appelle les fonctions permettant d'afficher la zone de texte correspondant à l'host
               
        
        """ On crée le bouton qui va permettre de valider les inputs utilisateur """
        
        button = QPushButton('Envoyer les données', self)        # On définit le titre du bouton      
        button.setToolTip('Envoyer les données maintenant ?')    # On configure ce qui va s'afficher lorsque l'on passe la souris au dessus du bouton
        button.move(130,285)                                    # On séléctionne la position du bouton
        button.clicked.connect(self.on_click)                   # On appelle la fonction "on_click" lorsque l'on clique sur le bouton
   
        
        """ On style le bouton """
        
        button.setStyleSheet("QPushButton"
                             "{"
                             "background-color : #7dbdda;"      # On définit un fond pour le bouton dans les tons bleus
                             "}"
                             "QPushButton::hover"               # Losque l'on passe la souris sur le bouton
                             "{"
                             "background-color : #7dda99;"      # On définit un fond pour le bouton dans les tons verts
                             "}"
                             "QPushButton::pressed"             # Lorsque le bouton est appuyé 
                             "{"
                             "background-color : #48d873;"      # On définit un fond pour le bouton dans les tons verts
                             "}"
                             )
        
        self.show()                                             # On affiche la fenetre 
     



    @pyqtSlot()
    def on_click(self):
        
        """On définit la fonction qui va gérer l'appui sur le bouton"""
        
        ip = self.zone_texte_ip.text()                                   # On prend le résultat de la zone de texte ip qu'on stocke dans une variable
        api = self.zone_texte_api.text()                                 # On prend le résultat de la zone de texte api qu'on stocke dans une variable
        host = self.zone_texte_hostname.text()                           # On prend le résultat de la zone de texte hostname qu'on stocke dans une variable
        
        host_join = "".join(['http://', host, '/iplogger/', ip, '?apikey=', api]) # On concatene la string avec un "".join
        ping = "".join(['http://', host, '/'])

        result = self.requete(host_join)                                       # On appelle la fonction requete() qui va s'occuper d'envoyer la requete au server


        if not validators.url(ping) or not requests.ConnectionError:            # On regarde si l'url est valide si on arrive à contacter correctement l'host.
            QMessageBox.about(self, "Erreur critique",  "host invalide")
            
        elif result.get("Erreur "):                                                 # On regarde si il y a une erreur dans l'un des champs
            QMessageBox.about(self, "Erreur critique", str(result.get("Erreur ")))
        
        else:
            latitude = str(result.get("latitude"))                                                  # On récupère la latitude
            longitude = str(result.get("longitude"))                                                # On récupère la longitude
            url = "".join(['https://www.openstreetmap.org/?mlat=', latitude, '&mlon=', longitude, '#map=14/', latitude, '/', longitude])     # On crée l'url openstreetmap avec la longitude et latitude récupéré
            self.open_web(url)                                                                     # On ouvre l'url
 



    def centrer(self):
        
        """On définit la fonction qui va gérer le centrage de la fenetre """
        
        geometrie_fenetre = self.frameGeometry()                            # On obtient la géometrie de la fenetre
        pointer_fenetre = QDesktopWidget().availableGeometry().center()     # On bouge le pointer au milieu de l'écran
        geometrie_fenetre.moveCenter(pointer_fenetre)                       # On définit la géométrie de la fenetre au centre de l'écran
        self.move(geometrie_fenetre.topLeft())                              # On bouge la fenetre au centre de l'écran


      
    def zone_ip(self):
        
        """ On crée la première zone de texte consacré à l'IP """
        
        self.label_ip = QLabel("Entrez votre IP :", self)                                 # On crée un label "entrez votre IP"
        self.label_ip.move(125, 50)                                                       # On bouge le label au dessus de la zone de texte correspondante
        
        self.zone_texte_ip = QLineEdit(self)                                              # On définit la première zone de texte
        self.zone_texte_ip.move(125, 75)                                                  # On définit une position pour la zone de texte
        self.zone_texte_ip.resize(self.zone_texte_longueur,self.zone_texte_largeur)       # On définit une taille pour la zone de texte
        self.zone_texte_ip.setStyleSheet("border-radius: 5px; color: blue;")              # On définit la couleur du texte


    def zone_api(self):
        
        """ On crée la seconde zone de texte consacré à l'API """
        
        self.label_api = QLabel("Entrez votre clé d'API :", self)                           # On crée un label "entrez votre clé d'API"
        self.label_api.move(125, 125)                                                       # On bouge le label au dessus de la zone de texte correspondante
        
        self.zone_texte_api = QLineEdit(self)                                               # On définit la première zone de texte
        self.zone_texte_api.move(125, 150)                                                  # On définit une position pour la zone de texte
        self.zone_texte_api.resize(self.zone_texte_longueur, self.zone_texte_largeur)       # On définit une taille pour la zone de texte
        self.zone_texte_api.setStyleSheet("border-radius: 5px; color: blue;")               # On définit la couleur du texte
   
    
    def zone_host(self):   
        
        """ On crée la dernière zone de texte consacré à l'hostname  """
        
        self.label_hostname = QLabel("Entrez le host :", self)                                   # On crée un label "entrez le host"
        self.label_hostname.move(125, 200)                                                       # On bouge le label au dessus de la zone de texte correspondante
        
        self.zone_texte_hostname = QLineEdit(self)                                               # On définit la première zone de texte
        self.zone_texte_hostname.move(125, 225)                                                  # On définit une position pour la zone de texte
        self.zone_texte_hostname.resize(self.zone_texte_longueur, self.zone_texte_largeur)       # On définit une taille pour la zone de texte
        self.zone_texte_hostname.setStyleSheet("border-radius: 5px; color: blue;")               # On définit la couleur du texte


    def requete(self, url):
        
        """ Prend en paramètre une string (url) et retourne le json de la l'url demandé si celui ci renvoit un code 200 """
        
        try:
            req = requests.get(url)             
            if(req.status_code != 200):     # On check si on parvient bien à accéder à l'url demandé
                QMessageBox.about(self, "Erreur critique", "Impossible de contacter l'adresse demandé")   # Si une erreur se produit on affiche un message
            else:
                return req.json()           # Si tout se passe bien on convertit la requete en json
        except Exception as e:              # Si une exception est trouvé on la retourne
            return e
  
    
    def open_web(self, url): 
        
        """ Prend en paramètre une string (url) """
        """ Sert à ouvrir une page web """
        
        webbrowser.open(url)
  
            
                         
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainWindow()
    app.exec_()
