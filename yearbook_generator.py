from PIL import ImageFilter
from PIL import Image, ImageDraw, ImageFont, ImageOps
import math 
import os
from eleves_data import eleves
from image_data import images_paths
from citations_data import citations_files



def ecrire_texte_multiligne(draw, texte, position, font, largeur_max, couleur="black", espacement=4):
    mots = texte.split()
    lignes = []
    ligne_actuelle = "  "

    for mot in mots:
        test   = (ligne_actuelle + "  " + mot).strip()
        w = draw.textlength(test, font=font)
        if w <= largeur_max:
            ligne_actuelle = test
        else:
            lignes.append(ligne_actuelle)
            ligne_actuelle = mot
    lignes.append(ligne_actuelle)

    x, y = position
    for ligne in lignes:
        
        largeur_ligne = draw.textlength(ligne, font=font)  
        x_centre_ligne = x + (largeur_max - largeur_ligne) // 2  
        draw.text((x_centre_ligne, y), ligne, font=font, fill=couleur)
        _, _, _, h = draw.textbbox((0, 0), ligne, font=font)
        y += h + espacement



def box_blur(image, rayon=3):
    pixels = image.load()
    largeur, hauteur = image.size
    resultat = Image.new("RGB", (largeur, hauteur))
    pixels_resultat = resultat.load()

    for y in range(hauteur):
        for x in range(largeur):
            total_r = total_g = total_b = 0
            compteur = 0
            for dy in range(-rayon, rayon + 1):
                for dx in range(-rayon, rayon + 1):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < largeur and 0 <= ny < hauteur:
                        r, g, b = pixels[nx, ny] 
                        total_r += r
                        total_g += g
                        total_b += b
                        compteur += 1
            pixels_resultat[x, y] = (
                total_r // compteur,
                total_g // compteur,
                total_b // compteur
            )
    return resultat



def creer_page_garde(chemin_logo):
    largeur, hauteur =  1880, 2000   

    page = Image.new("RGB", (largeur, hauteur), "white")
    draw = ImageDraw.Draw(page)

    try:
        font_titre = ImageFont.truetype("arial.ttf", 80)
        font_soustitre = ImageFont.truetype("arial.ttf", 50)
    except:
        font_titre = font_soustitre = ImageFont.load_default()

    logo = Image.open(chemin_logo).convert("RGBA")
    largeur_max = 1000
    ratio = largeur_max / logo.width
    nouvelle_largeur = int(logo.width * ratio)
    nouvelle_hauteur = int(logo.height * ratio)
    logo = logo.resize((nouvelle_largeur, nouvelle_hauteur), Image.LANCZOS)
    position_x_logo = (largeur - logo.width) // 2
    position_y_logo = hauteur // 3 - logo.height // 2
    page.paste(logo, (position_x_logo, position_y_logo), logo)
    
    couleur = (0, 51, 153)
    titre = "Bachelor 1 _ SUPINFO Paris _ 2025-2026"
    sous_titre = "Année académique 2025-2026 _ Campus de Paris"

    w = draw.textlength(titre, font=font_titre)
    draw.text(((largeur - w) // 2, position_y_logo + logo.height + 150), titre, fill=couleur, font=font_titre)

    w2 = draw.textlength(sous_titre, font=font_soustitre)
    draw.text(((largeur - w2) // 2, hauteur - 300), sous_titre, fill=couleur, font=font_soustitre)

    page.save("page_garde.png")
    
    page.show()
    print(" Page d'ouverture SUPINFO crée")
    return page


def page_sup_classe(pages, chemin_image):
    try:
        img = Image.open(chemin_image).convert("RGB")

        
        
        largeur, hauteur  = 2430, 1320
 
        page = Image.new("RGB", (largeur, hauteur), "white")

        
        ratio = max(largeur / img.width, hauteur / img.height)
        nouvelle_taille = (int(img.width * ratio), int(img.height * ratio))
        img = img.resize(nouvelle_taille, Image.BICUBIC)

        
        x = (largeur - img.width) // 2
        y = (hauteur - img.height) // 2
        page.paste(img, (x, y))

        
        page.save("photoClasse.png")

        
        pages.append(page)

        
        page.show()
        print(" Photo de classe SUPINFO crée")

    except Exception as e:
        print(f"Erreur : {e}")
         
 
def creer_pages_yearbook(images, dictionnaire_citations):
    
    print("Creation des images en cours :")
    
    
    choix = input(" Entre 1 pour Portrait ou nimporte quel nbr réel pour Paysage : ").strip()


    if choix == "1":
       orientation = "portrait"
       largeur, hauteur = 1880, 2000
       largeur_img, hauteur_img = 320, 384
       espacement = 220
       départ_x, départ_y = 70, 60
       colonnes, rangées = 3, 3
       bordure = 10
       marge_texte = 20

       largeur_yn = colonnes * largeur_img + (colonnes - 1) * espacement
       hauteur_yn = rangées * (hauteur_img + marge_texte + 40) + (rangées - 1) * espacement
       départ_x = (largeur - largeur_yn) // 2
       départ_y = (hauteur - hauteur_yn) // 2
       
    
    
    else:
       orientation = "paysage"
       largeur, hauteur = 2430, 1320
       largeur_img, hauteur_img = 256, 384        
       espacement = 180         
       départ_x, départ_y = 70, 60     
       colonnes, rangées = 5, 2            
       bordure = 8                   
       marge_texte = 12
                         
       largeur_yn = colonnes * largeur_img + (colonnes - 1) * espacement
       hauteur_yn = rangées * (hauteur_img + marge_texte + 40) + (rangées - 1) * espacement  


       départ_x = (largeur - largeur_yn) // 2
       départ_y = (hauteur - hauteur_yn) // 2

                           
    try:
        font = ImageFont.truetype("StoryScript-Regular.ttf", 23)
    except:
        font = ImageFont.load_default()
        print("yo")

    étudiants_par_page = colonnes * rangées
    nombre_pages = math.ceil(len(images) / étudiants_par_page)
    pages = []

    for numéro_page in range(nombre_pages):
        page = Image.new("RGB", (largeur, hauteur), "white")
        draw = ImageDraw.Draw(page)
    
        début = numéro_page * étudiants_par_page
        fin = min(début + étudiants_par_page, len(images))

        for i in range(début, fin):
            colonne = (i- début) % colonnes
            rangé = (i-début) // colonnes
            x = départ_x + colonne * (largeur_img +espacement)
            y = départ_y + rangé * (hauteur_img + espacement)

            try:
                img = Image.open(images[i]).resize((largeur_img, hauteur_img))
            except:
                print(f" Image introuvable : {images[i]}")
                continue

            identifiant_image = os.path.splitext(os.path.basename(images[i]))[0]
            informations = eleves.get(identifiant_image)

            if informations:
                floutage = informations.get("floutage", False)
                délégué = informations.get("delegue", 0)
            else:
                floutage = False
                délégué = 0
            
            
            if floutage:
                img = box_blur(img, rayon=4)
          

            couleur_bordure = "black" if délégué > 0 else "black"
            cadre_noir_image = ImageOps.expand(img, border=bordure, fill=couleur_bordure)

            page.paste(cadre_noir_image, (x, y))

            if informations:
                rôle = informations.get("delegue", 0)
                if rôle == 2:  
                 try:
                     icone_médaillon = Image.open("output/images/medaille-dor.png").convert("RGBA")
                     icone_médaillon = icone_médaillon.resize((60, 60))
                     page.paste(icone_médaillon, (x + largeur_img - 30, y - 30), icone_médaillon)
                 except Exception as e:
                     print(f" Erreur or  : {e}")

                elif rôle == 1:  
                    try:
                        icone_médaillon = Image.open("output/images/medaille-dargent.png").convert("RGBA")
                        icone_médaillon = icone_médaillon.resize((60, 60))
                        page.paste(icone_médaillon, (x + largeur_img - 30, y - 30), icone_médaillon)
                    except Exception as e:
                        print(f" Erreur argent : {e}")

            if informations:
                nom_complet = f"{informations['prenom']} {informations['nom']}"
            else:
                nom_complet = "(Nom inconnu)"
            
            largeur_nom = draw.textlength(nom_complet, font=font)
            position_x_centrée = x + (largeur_img - largeur_nom) // 2
            draw.text((position_x_centrée, y + hauteur_img + marge_texte), nom_complet, fill="black", font=font)

            citation = dictionnaire_citations.get(identifiant_image, "(erreurr)")
            ecrire_texte_multiligne(draw, citation, (x, y + hauteur_img + marge_texte + 40), font, largeur_img)

        fichier = f"yearbook_page_{numéro_page+1}.png"
        page.save(fichier)
        pages.append(page)
        print(f"Page enregistré : {fichier}")
  
    return pages


if __name__ == "__main__":
    creer_page_garde("ressources/SUPINFO_LOGO_QUADRI.png")
    pages = []
    page_sup_classe(pages, "output/images/photoClasse.png")

    
    dictionnaire_citations = {}
    for identifiant_élève, chemin in citations_files.items():
        with open(f"{chemin}", "r", encoding="utf-8") as f:
            dictionnaire_citations[identifiant_élève] = f.read().strip()
 





a = creer_pages_yearbook(images_paths, dictionnaire_citations)


for i in range(1, 4):
    img = Image.open(f"yearbook_page_{i}.png")
    mode_noirblanc = img.convert("L")
    mode_noirblanc.save(f"yearbook{i}.jpeg")



   
    
    
def sauvegarder_pdf(pages, nom_pdf="yearbook_final.pdf"):
    try:
        ensemble_pages = []

       
        ensemble_pages.append(Image.open("page_garde.png").convert("RGB"))
        ensemble_pages.append(Image.open("photoClasse.png").convert("RGB"))

     
        for i in range(1, 4):
            ensemble_pages.append(Image.open(f"yearbook_page_{i}.png").convert("RGB"))

     
        for i in range(1, 4):
            ensemble_pages.append(Image.open(f"yearbook{i}.jpeg").convert("RGB"))

        
        ensemble_pages[0].save(
            nom_pdf,
            "PDF",
            save_all=True,
            append_images=ensemble_pages[1:],
            resolution=100.0
        )

        print(f"Yearbook généré  : {nom_pdf}")

    except Exception as yan:
        print(f" Erreur  : {yan}")

    



img1 = Image.open("yearbook_page_1.png")
mode_noirblanc = img1.convert("L")
mode_noirblanc.save("yearbook1.jpeg")
img1 = Image.open("yearbook_page_2.png")
mode_noirblanc = img1.convert("L")
mode_noirblanc.save("yearbook2.jpeg")

img1 = Image.open("yearbook_page_3.png")
mode_noirblanc = img1.convert("L")
mode_noirblanc.save("yearbook3.jpeg")
    
sauvegarder_pdf(pages, "yearbook_final.pdf")