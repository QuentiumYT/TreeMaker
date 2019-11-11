import os, sys, urllib.request
from tkinter import *
from tkinter.messagebox import *

__version__ = 5
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
        try:urllib.request.urlretrieve("http://quentium.fr/+++PythonDL/{}.ico".format(__filename__), __iconpath__)
        except:pass

if connection == True:
    try:script_version = int(urllib.request.urlopen("http://quentium.fr/programs/index.php").read().decode().split(__filename__ + "<!-- Version: ")[1].split(" --></h2>")[0])
    except:script_version = __version__
    if script_version > __version__:
        if os.path.exists(__iconpath__):popup = Tk(); popup.attributes("-topmost", 1); popup.iconbitmap(__iconpath__); popup.withdraw()
        ask_update = askquestion(__filename__ + " V" + str(script_version), "Une mise à jour à été trouvée, souhaitez vous la télécharger puis l'éxécuter ?", icon="question")
        if ask_update == "yes":
            try:os.rename(__basename__, __filename__ + "-old.exe")
            except:os.remove(__filename__ + "-old.exe"); os.rename(__basename__, __filename__ + "-old.exe")
            if "-32" in str(__basename__):urllib.request.urlretrieve("http://quentium.fr/download.php?file={}-32.exe".format(__filename__), __filename__ + ".exe")
            else:urllib.request.urlretrieve("http://quentium.fr/download.php?file={}.exe".format(__filename__), __filename__ + ".exe")
            showwarning(__filename__, "Le programme va redémarrer pour fonctionner sous la nouvelle version.", icon="warning")
            os.system("start " + __filename__ + ".exe"); os._exit(1)

__filename__ = __filename__ + " V" + str(__version__)

from tkinter.ttk import *
from tkinter.filedialog import *
from tkinter import *

tree_done = ""
FILES = False

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
    if FILES and files:
        file_prefix = prefix + ("|" if dirs else " ") + "   "
        for name in files:
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
        yield count, count - length, value

def start_tree():
    global FILES, dirs
    if check_var.get() == 0:
        FILES = False
    elif check_var.get() == 1:
        FILES = True
    directory = askdirectory()
    if directory:
        if not directory == "":
            file = open("Tree.txt", "w", encoding="utf-8")
            tree(directory)
            file.write(tree_done[:-1])
            file.close()
            showinfo(__filename__, "Votre structure a été générée avec succès.")

            win_crypt = Tk()
            win_crypt.configure(bg = "lightgray")
            if os.path.exists(__iconpath__):
                win_crypt.iconbitmap(__iconpath__)
            """
            win_crypt.state("zoomed")
            win_crypt.title(__filename__)
            canvas = Canvas(win_crypt, height=1030, background="white")
            canvas.pack(fill=BOTH)

            canvas_id = canvas.create_text(10, -10, font="impact 15", anchor="nw")
            canvas.insert(canvas_id, 5000, "uiy")
            win_crypt.mainloop()
            """
        treemaker.destroy()
        os._exit(0)
    else:
        showwarning(__filename__, "Erreur : Aucun dossier n'a été sélectionné !")

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
check_var = IntVar()
Checkbutton(treemaker, text="Fichiers inclus ?", variable=check_var, font="impact 20", bg="lightgray", activebackground="lightgray").pack(pady=50)
Button(treemaker, text="Générer une structure", command=start_tree, relief=GROOVE, width=25, font="impact 20", fg="black").pack(pady=20)
treemaker.mainloop()
