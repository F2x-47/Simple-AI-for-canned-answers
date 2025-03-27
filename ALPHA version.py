import random
import platform
import os
from termcolor import colored

def get_file_path():
    system = platform.system() 
    if system == "Windows": # Windows
        return r"File path"
        print(colored("Operating system : Windows.", 'yellow'))
    elif system == "Darwin":  # macOS
        return "File path"
        print(colored("Operating sustem : MacOS.", 'yellow'))
    else:  # Linux or others
        return "File path"
        print(colored("Operating system : Linux ou autres.", 'yellow'))

def setup():
    file_path = get_file_path()

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.readlines()
            print("Reading data from the file.")

        if len(content) < 5:
            raise ValueError("The data.txt file does not contain enough lines.")
            print(colored("The file does not contain enough lines.", 'yellow'))

    except (FileNotFoundError, ValueError):
        print(colored(f"The file {file_path} is missing or incorrectly formatted. Creating a new file...", 'yellow'))
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as file:
            file.writelines(["-1\n", "{}\n", "{}\n", "{}\n", "{}\n"])
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.readlines()

    rep = int(content[0].strip())
    dico = eval(content[1].strip())
    question = eval(content[2].strip())
    for i in question:
        question[i] = question[i].split(" ")
    synonyme = eval(content[3].strip())
    blacklist = eval(content[4].strip())
    blackwords = ["and", "but", "or", "neither", "because", "that", "?", "!", ".", "of", "so", ";", ":", "", " "]

    return None, blacklist, dico, rep, question, synonyme, blackwords

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
    return False

def liste(inter):
    reponse = inter.replace("-", " ").replace(",", " ").replace(".", " ").split()
    return " ".join(reponse), reponse

def first(dico, rep, question, reponse):
    print(colored("Hum... I don't know this question.", 'magenta'))
    question[0] = reponse
    dico[0] = input(colored("What should I answer? ", 'magenta'))
    return 0, dico, 0, question

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

def chose(dico, rep, choix):
    choisivaleur = max(choix.values(), default=0)
    if choisivaleur > 0:
        pertinente = [i for i in choix if choix[i] == choisivaleur]
        nombre = random.choice(pertinente)
        return False, nombre, dico, rep, dico[nombre]
    return True, None, dico, rep, None

def check(verif, back, reponse1, blacklist, nombre, dico, rep, question, reponse):
    check = input(colored("Did I answer correctly? (yes/no): ", 'magenta')).strip().lower()
    if check == "no":
        if back in blacklist:
            if reponse1 in blacklist[back]:
                blacklist[back][reponse1].append(nombre)
            else:
                blacklist[back][reponse1] = [nombre]
        else:
            blacklist[back] = {reponse1: [nombre]}
        rep += 1
        question[rep] = reponse
        dico[rep] = input(colored("What should I answer? ", 'magenta'))
        back = rep
    else:
        back = nombre
    return back, blacklist, dico, rep, question

def ask(back, dico, rep, question, reponse):
    rep += 1
    question[rep] = reponse
    dico[rep] = input(colored("I don't know this question. What should I answer? ", 'magenta'))
    back = rep
    return back, dico, rep, question

def main():
    back, blacklist, dico, rep, question, synonyme, blackwords = setup()
    print(colored("Ask me a question, or answer 'exit' to leave.", 'red'))
    execute = True
    while execute:
        inter = input(colored("You : ", 'blue')).strip()
        
        if inter.lower() == "exit":
            print(colored("Goodbye!", 'green'))
            print(colored("Closing the application.", 'yellow'))
            execute = close(blacklist, dico, rep, question, synonyme)
        else:
            try:
                result = eval(inter)
                if isinstance(result, (int, float)): 
                    print(colored(f"AI : {result}", 'green'))
                    continue 
            except:
                pass 

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
