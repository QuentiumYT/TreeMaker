import sys, os, re, ctypes, argparse, colorama

cli = False if ":\\" in sys.argv[0] else True

colorama.init()
parser = argparse.ArgumentParser(prog="PROG", prefix_chars="-+")

parser.add_argument("-f", "--files", help="active la recherche des fichiers dans l'arborescence", action="store_true")
parser.add_argument("-d", "--dir", metavar="directory", help="séléctionne le dossier ou l'arborescence doit être crée")
parser.add_argument("-i", "--ignore", metavar="ignore", help="ignore des dossiers / fichiers (separés par un espace ou virgule)", nargs="+")
parser.add_argument("-g", "--gui", help="active l'interface du programme", action="store_false")

args = parser.parse_args()

tree_done = ""
ignore_files = []

if not args.files:
    check_files = False
    print("Les fichiers ne sont pas pris en compte dans l'arborescence.")
    print(colorama.Fore.YELLOW + "(Si vous les souhaitez, ajoutez l'argument '-f')" + colorama.Fore.RESET)
else:
    check_files = True
    print("Les fichiers sont pris en compte dans l'arborescence.")

if not args.dir:
    directory = os.getcwd()
    print("Aucuns dossier n'a été séléctionné, le dossier actuel à été choisis.")
    print(colorama.Fore.YELLOW + "(Si vous souhaitez spécifier un dossier, ajoutez l'argument '-d \"nom_dossier\"')" + colorama.Fore.RESET)
else:
    directory = args.dir
    if not os.path.exists(directory):
        print(colorama.Fore.RED + "Le dossier {directory} n'existe pas ou n'a pas été trouvé, le dossier actuel à été choisis." + colorama.Fore.RESET)
        directory = os.getcwd()
    else:
        print("Le dossier " + args.dir + " à été choisis.")

if args.ignore:
    if os.path.exists(".gitignore"):
        ask_gitignore = input("Un fichier .gitignore à été trouvé, voulez vous l'utiliser ? (O/N) : ")
        if not "n" in ask_gitignore.lower():
            git_file = open(".gitignore", "r").readlines()
            ignore_files += [x.strip() for x in git_file if not x.startswith("#") and x != "\n"]
    ignore_files += re.findall("[.|\w+].?\w+/?\w+/?|\w+/", "".join(args.ignore))
    print("Les dossiers / fichiers '" + ', '.join(ignore_files) + "' vont être ignorés.")

if cli:
    cli = args.gui
else:
    # I have to enable and hide the console to be able to print to stdout when CLI is used
    if sys.platform.lower().startswith("win"):
        if getattr(sys, "frozen", False):
            whnd = ctypes.windll.kernel32.GetConsoleWindow()
            ctypes.windll.user32.ShowWindow(whnd, 0)
    import urllib.request
    from tkinter import *
    from tkinter.messagebox import *

    __version__ = 8
    __filename__ = "TreeMaker"
    __basename__ = os.path.basename(sys.argv[0])
    __savepath__ = os.path.join(os.environ["APPDATA"], "QuentiumPrograms")
    __iconpath__ = __savepath__ + "/{}.ico".format(__filename__)

    try:urllib.request.urlopen("https://www.google.fr/", timeout=1); connection = True
    except:connection = False
    if not os.path.exists(__iconpath__):
        try:os.mkdir(__savepath__)
        except:pass
        if connection == True:
            try:urllib.request.urlretrieve("https://quentium.fr/+++PythonDL/{}.ico".format(__filename__), __iconpath__)
            except:pass

    if connection == True:
        try:script_version = int(urllib.request.urlopen("https://quentium.fr/programs/index.php").read().decode().split(__filename__ + "<!-- Version: ")[1].split(" --></h2>")[0])
        except:script_version = __version__
        if script_version > __version__:
            if os.path.exists(__iconpath__):popup = Tk(); popup.attributes("-topmost", 1); popup.iconbitmap(__iconpath__); popup.withdraw()
            ask_update = askquestion(__filename__ + " V" + str(script_version), "Une mise à jour à été trouvée, souhaitez vous la télécharger puis l'éxécuter ?", icon="question")
            if ask_update == "yes":
                try:os.rename(__basename__, __filename__ + "-old.exe")
                except:os.remove(__filename__ + "-old.exe"); os.rename(__basename__, __filename__ + "-old.exe")
                if "-32" in str(__basename__):urllib.request.urlretrieve("https://quentium.fr/download.php?file={}-32.exe".format(__filename__), __filename__ + ".exe")
                else:urllib.request.urlretrieve("https://quentium.fr/download.php?file={}.exe".format(__filename__), __filename__ + ".exe")
                showwarning(__filename__, "Le programme va redémarrer pour fonctionner sous la nouvelle version.", icon="warning")
                os.system("start " + __filename__ + ".exe"); os._exit(1)

    __filename__ = __filename__ + " V" + str(__version__)

    from tkinter.ttk import *
    from tkinter.filedialog import *
    from tkinter import *

def is_ignored(thing):
    return any([x for x in ignore_files if x == thing])

def tree(path):
    global tree_done, dirs
    path = os.path.abspath(path)
    dirs, files = listdir(path)[:2]
    tree_done += path + "\n"
    walk(path, dirs, files)
    if not dirs:
        tree_done += "Aucuns sous dossiers existants !" + "\n"

def walk(root, dirs, files, prefix=""):
    global tree_done
    if check_files and files:
        file_prefix = prefix + ("|" if dirs else " ") + "   "
        for name in files:
            if not is_ignored(name):
                tree_done += file_prefix + name + "\n"
        tree_done += file_prefix + "\n"
    dir_prefix, walk_prefix = prefix + "+---", prefix + "|   "
    for pos, neg, name in enumerate2(dirs):
        if neg == -1:
            dir_prefix, walk_prefix = prefix + "\\---", prefix + "    "
        tree_done += dir_prefix + name + "\n"
        path = os.path.join(root, name)
        try:
            dirs, files = listdir(path)[:2]
        except:
            pass
        else:
            walk(path, dirs, files, walk_prefix)

def listdir(path):
    dirs, files, links = [], [], []
    for name in os.listdir(path):
        path_name = os.path.join(path, name)
        if os.path.isdir(path_name):
            dirs.append(name)
        elif os.path.isfile(path_name):
            files.append(name)
        elif os.path.islink(path_name):
            links.append(name)
    return dirs, files, links

def enumerate2(sequence):
    length = len(sequence)
    for count, value in enumerate(sequence):
        if is_ignored(value + "/"):
            continue
        yield count, count - length, value

def start_tree():
    global check_files, dirs, ignore_files
    if os.path.exists(".gitignore"):
        ask_use_git = askquestion(__filename__, "Un fichier .gitignore à été trouvé, voulez vous l'utiliser ?", icon="question")
        if ask_use_git == "yes":
            f = open(".gitignore", "r").readlines()
            ignore_files = [x.strip() for x in f if not x.startswith("#") and x != "\n"]
        else:
            ignore_files = []
    else:
        ask_use_git = askquestion(__filename__, "Voulez vous utiliser un ficher .gitignore pour ignorer vos fichiers dans votre structure ?", icon="question")
        if ask_use_git == "yes":
            f = askopenfile().readlines()
            ignore_files = [x.strip() for x in f if not x.startswith("#") and x != "\n"]
        else:
            ignore_files = []
    if entry_val.get() != entry_default:
        ignore_files += re.findall("[.|\w+].?\w+/?\w+/?|\w+/", entry_val.get())
    if check_var.get() == 0:
        check_files = False
    elif check_var.get() == 1:
        check_files = True
    directory = askdirectory()
    if directory:
        if not directory == "":
            tree(directory)
            file = open(directory + "/Tree.txt", "w", encoding="utf-8")
            file.write(tree_done[:-1])
            file.close()
            showinfo(__filename__, "Votre structure a été générée avec succès.")

            treemaker.destroy()

            treemaker_preview = Tk()
            treemaker_preview.configure(bg="lightgray")
            if os.path.exists(__iconpath__):
                treemaker_preview.iconbitmap(__iconpath__)

            treemaker_preview.state("zoomed")
            treemaker_preview.title(__filename__)

            S = Scrollbar(treemaker_preview)
            T = Text(treemaker_preview, undo=True, height=700, width=1000)
            S.pack(side=RIGHT, fill=Y)
            T.pack(side=LEFT, fill=Y)
            S.config(command=T.yview)
            T.config(yscrollcommand=S.set)
            T.insert(END, tree_done[:-1])
            treemaker_preview.mainloop()

        os._exit(0)
    else:
        showwarning(__filename__, "Erreur : Aucun dossier n'a été sélectionné !")

if cli:
    tree(directory)
    file = open(directory + "//Tree.txt", "w", encoding="utf-8")
    file.write(tree_done[:-1])
    file.close()
    os._exit(0)
else:
    treemaker = Tk()
    width = 750
    height = 500
    treemaker.update_idletasks()
    x = (treemaker.winfo_screenwidth() - width) // 2
    y = (treemaker.winfo_screenheight() - height) // 2
    treemaker.geometry("{}x{}+{}+{}".format(width , height, int(x), int(y)))
    treemaker.resizable(width=False, height=False)
    treemaker.configure(bg="lightgray")
    if os.path.exists(__iconpath__):
        treemaker.iconbitmap(__iconpath__)
    treemaker.title(__filename__)
    Label(treemaker, text="Bienvenue dans le programme de création", font="impact 30", fg="red", bg="lightgray").pack(pady=40)
    Label(treemaker, text="de structure de documents !", font="impact 30", fg="red", bg="lightgray").pack()
    check_var = IntVar(value=1)
    Checkbutton(treemaker, text="Fichiers inclus ?", variable=check_var, font="impact 20", bg="lightgray", activebackground="lightgray").pack(pady=20)
    entry_val = StringVar()
    entry_default = "Fichiers/dossiers à ignorer (ex: a.txt, .gitignore, fold/, .git/)"
    entry = Entry(treemaker, textvariable=entry_val, width=50, font="impact 15")
    entry.insert(0, entry_default)
    entry.pack(pady=20)
    def clear_entry(event, entry):
        if entry.get() == entry_default:
            entry.delete(0, END)
    entry.bind("<Button-1>", lambda event: clear_entry(event, entry))
    Button(treemaker, text="Générer une structure", command=start_tree, relief=GROOVE, width=25, font="impact 20", fg="black").pack(pady=20)
    treemaker.mainloop()
