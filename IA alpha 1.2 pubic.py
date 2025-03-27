import random
import platform
import os
from termcolor import colored

# Fonction pour détecter le système d'exploitation et définir l'emplacement du fichier
def get_file_path():
    system = platform.system()  # Détecte le système d'exploitation
    if system == "Windows": # Windows
        return r"Chemin du fichier"
        print(colored("Systeme d'exploitation : Windows.", 'yellow'))
    elif system == "Darwin":  # macOS
        return "Chemin du fichier"
        print(colored("Systeme d'exploitation : MacOS.", 'yellow'))
    else:  # Linux ou autres
        return "Chemin du fichier"
        print(colored("Systeme d'exploitation : Linux ou autres.", 'yellow'))

# Fonction d'ouverture des données
def setup():
    file_path = get_file_path()

    try:
        # Lecture des données depuis le fichier
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.readlines()
            print("Lecture des données du fichier.")

        # Vérifie que le fichier contient le bon nombre de lignes
        if len(content) < 5:
            raise ValueError("Le fichier data.txt ne contient pas suffisamment de lignes.")
            print(colored("Le fichier ne contient pas suffisament de ligne.", 'yellow'))

    except (FileNotFoundError, ValueError):
        # Création du fichier s'il n'existe pas encore ou est mal formaté
        print(colored(f"Le fichier {file_path} est manquant ou mal formaté. Création d'un nouveau fichier...", 'yellow'))
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as file:
            file.writelines(["-1\n", "{}\n", "{}\n", "{}\n", "{}\n"])
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.readlines()

    # Chargement des données du fichier
    rep = int(content[0].strip())
    dico = eval(content[1].strip())
    question = eval(content[2].strip())
    for i in question:
        question[i] = question[i].split(" ")
    synonyme = eval(content[3].strip())
    blacklist = eval(content[4].strip())
    blackwords = ["et", "mais", "ou", "or", "ni", "car", "que", "?", "!", ".", "de", "donc", ";", ":", "", " "]

    return None, blacklist, dico, rep, question, synonyme, blackwords

# Fonction de sauvegarde des nouveaux mots
def close(blacklist, dico, rep, question, synonyme):
    file_path = get_file_path()
    for i in question:
        question[i] = " ".join(question[i])
    with open(file_path, "w", encoding="utf-8") as file:
        file.writelines(
            [
                str(rep) + "\n",
                str(dico) + "\n",
                str(question) + "\n",
                str(synonyme) + "\n",
                str(blacklist) + "\n",
            ]
        )
    return False  # Termine la boucle principale

# Fonction transforme la phrase en liste de mots
def liste(inter):
    reponse = inter.replace("-", " ").replace(",", " ").replace(".", " ").split()
    return " ".join(reponse), reponse

# Fonction si c'est la première fois
def first(dico, rep, question, reponse):
    print(colored("Hum... je ne connais pas encore cette question.", 'magenta'))
    question[0] = reponse
    dico[0] = input(colored("Que dois-je répondre ? ", 'magenta'))
    return 0, dico, 0, question

# Fonction scan toutes les phrases et établit leur pertinence
def scan(back, reponse1, blacklist, rep, question, synonyme, blackwords, reponse):
    choix = {}
    for i in range(rep + 1):
        choix[i] = 0
        for b in reponse:
            if b not in blackwords and b in question[i]:
                choix[i] += 2
            elif b in synonyme:
                for syn in synonyme[b]:
                    if syn in question[i]:
                        choix[i] += 1
    return choix

# Fonction choisit une phrase
def chose(dico, rep, choix):
    choisivaleur = max(choix.values(), default=0)
    if choisivaleur > 0:
        pertinente = [i for i in choix if choix[i] == choisivaleur]
        nombre = random.choice(pertinente)
        return False, nombre, dico, rep, dico[nombre]
    return True, None, dico, rep, None

# Fonction vérifie si la réponse est correcte
def check(verif, back, reponse1, blacklist, nombre, dico, rep, question, reponse):
    check = input(colored("J'ai bien répondu ? (oui/non) : ", 'magenta')).strip().lower()
    if check == "non":
        # Ajout à la blacklist si la réponse est incorrecte
        if back in blacklist:
            if reponse1 in blacklist[back]:
                blacklist[back][reponse1].append(nombre)
            else:
                blacklist[back][reponse1] = [nombre]
        else:
            blacklist[back] = {reponse1: [nombre]}
        # Demande une nouvelle réponse et l'ajoute
        rep += 1
        question[rep] = reponse
        dico[rep] = input(colored("Que dois-je répondre ? ", 'magenta'))
        back = rep
    elif check == "no":
        # Ajout à la blacklist si la réponse est incorrecte
        if back in blacklist:
            if reponse1 in blacklist[back]:
                blacklist[back][reponse1].append(nombre)
            else:
                blacklist[back][reponse1] = [nombre]
        else:
            blacklist[back] = {reponse1: [nombre]}
        # Demande une nouvelle réponse et l'ajoute
        rep += 1
        question[rep] = reponse
        dico[rep] = input(colored("Que dois-je répondre ? ", 'magenta'))
        back = rep
    elif check == "nn":
        # Ajout à la blacklist si la réponse est incorrecte
        if back in blacklist:
            if reponse1 in blacklist[back]:
                blacklist[back][reponse1].append(nombre)
            else:
                blacklist[back][reponse1] = [nombre]
        else:
            blacklist[back] = {reponse1: [nombre]}
        # Demande une nouvelle réponse et l'ajoute
        rep += 1
        question[rep] = reponse
        dico[rep] = input(colored("Que dois-je répondre ? ", 'magenta'))
        back = rep
    elif check == "n":
        # Ajout à la blacklist si la réponse est incorrecte
        if back in blacklist:
            if reponse1 in blacklist[back]:
                blacklist[back][reponse1].append(nombre)
            else:
                blacklist[back][reponse1] = [nombre]
        else:
            blacklist[back] = {reponse1: [nombre]}
        # Demande une nouvelle réponse et l'ajoute
        rep += 1
        question[rep] = reponse
        dico[rep] = input(colored("Que dois-je répondre ? ", 'magenta'))
        back = rep
    else:
        back = nombre
    return back, blacklist, dico, rep, question

# Fonction si rien n'a été trouvé
def ask(back, dico, rep, question, reponse):
    rep += 1
    question[rep] = reponse
    dico[rep] = input(colored("Je ne connais pas cette question. Que dois-je répondre ? ", 'magenta'))
    back = rep
    return back, dico, rep, question

# Fonction principale
def main():
    back, blacklist, dico, rep, question, synonyme, blackwords = setup()
    print(colored("Pose-moi une question, ou réponds 'exit' pour quitter.", 'red'))
    execute = True
    while execute:
        inter = input(colored("Vous : ", 'blue')).strip()
        
        if inter.lower() == "exit":
            print(colored("Au revoir !", 'green'))
            print(colored("Fermeture de l'application.", 'yellow'))
            execute = close(blacklist, dico, rep, question, synonyme)
        else:
            # Vérifier si l'entrée est un calcul mathématique
            try:
                # Si l'entrée est un calcul, on l'évalue et on renvoie la réponse
                result = eval(inter)
                if isinstance(result, (int, float)):  # Vérifie si le résultat est un nombre
                    print(colored(f"IA : {result}", 'green'))
                    continue  # Passe à la prochaine question sans chercher dans les questions existantes
            except:
                pass  # Si l'entrée n'est pas un calcul valide, passer au traitement suivant

            reponse1, reponse = liste(inter)
            if rep == -1:
                back, dico, rep, question = first(dico, rep, question, reponse)
            else:
                choix = scan(back, reponse1, blacklist, rep, question, synonyme, blackwords, reponse)
                verif, nombre, dico, rep, choisitexte = chose(dico, rep, choix)
                if not verif:
                    print(colored(f"IA : {choisitexte}", 'green'))
                    back, blacklist, dico, rep, question = check(verif, back, reponse1, blacklist, nombre, dico, rep, question, reponse)
                else:
                    back, dico, rep, question = ask(back, dico, rep, question, reponse)

if __name__ == "__main__":
    main()