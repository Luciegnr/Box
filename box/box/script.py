import os.path, subprocess, urllib.request, tarfile,shutil, yaml, sys
from sys import argv

box = '/var/lib/box'
base = '/var/lib/box/base'
env = '/var/lib/box/env'
mongo = '/var/lib/box/env/mongodb'

dev = base + '/dev'
proc = base + '/proc/'
sys = base + '/sys/'

mdev = 'sudo mount --bind /dev ' + dev
mdev = mdev.split()

udev = 'sudo umount ' + dev
udev = udev.split()

mproc = 'sudo mount -t proc /proc ' + proc
mproc = mproc.split()

uproc = 'sudo umount ' + proc
uproc = uproc.split()

msys = 'sudo mount -t sysfs /sys ' + sys
msys = msys.split()

usys = 'sudo umount ' + sys
usys = usys.split()

modev = mongo + '/dev'
mosys = mongo + '/sys'
moproc = mongo + '/proc'

umproc = 'sudo umount ' + moproc
umproc = umproc.split()

umsys = 'sudo umount ' + mosys
umsys = umsys.split()

umdev = 'sudo umount ' + modev
umdev = umdev.split()


# On démonte les filesystem si ils sont sont déjà montés.
def unmount():
    if os.path.ismount(dev):
        cmd1 = subprocess.Popen(udev)

    if os.path.ismount(sys):
        cmd2 = subprocess.Popen(usys)

    if os.path.ismount(proc):
        cmd3 = subprocess.Popen(uproc)

    if os.path.ismount(modev):
        cmd3 = subprocess.Popen(umdev)

    if os.path.ismount(mosys):
        cmd3 = subprocess.Popen(umsys)

    if os.path.ismount(moproc):
        cmd3 = subprocess.Popen(umproc)


# On supprime les dossiers "env", "mongodb" "box" et "base" si ils sont déjà existant.
def delete_folder():
    if os.path.exists(mongo):
        shutil.rmtree(mongo)
        directory = "mongodb"
        parent = "/var/lib/env"
        path = os.path.join(parent, directory)

    if os.path.exists(env):
        shutil.rmtree(env)
        directory = "env"
        parent = "/var/lib/box"
        path = os.path.join(parent, directory)

    if os.path.exists(base):
        shutil.rmtree(base)
        directory = "base"
        parent = "/var/lib/box"
        path = os.path.join(parent, directory)

    if os.path.exists(box):
        shutil.rmtree(box)
        directory = "box"
        parent = "/var/lib"
        path = os.path.join(parent, directory)


# On crée ou recréer les dossiers env, mongodb, box et base
def create_folder():
    os.mkdir(box)
    os.mkdir(base)
    os.mkdir(env)
    os.mkdir(mongo)


# On télécharge l'archive de configuration et on l'extrait
def tar():
    path_tar = base
    os.chdir(path_tar)
    urllib.request.urlretrieve(
        'https://github.com/debuerreotype/docker-debian-artifacts/raw/3503997cf522377bc4e4967c7f0fcbcb18c69fc8/buster/slim/rootfs.tar.xz',
        'rootfs.tar.xz')
    with tarfile.open('rootfs.tar.xz') as f:
        f.extractall('.')
    os.remove(base + '/rootfs.tar.xz')


# On monte les filesystem proc, sys, et dev dans /var/lib/box/base
def mount_filesystem():
    dev_file = subprocess.Popen(mdev)
    sys_file = subprocess.Popen(msys)
    proc_file = subprocess.Popen(mproc)


# Nous repréparons l'environnement d'exécution pour notre application mongodb
def mogo():
    path_tar = "/var/lib/box/env/mongodb"
    os.chdir(path_tar)
    urllib.request.urlretrieve(
        'https://github.com/debuerreotype/docker-debian-artifacts/raw/3503997cf522377bc4e4967c7f0fcbcb18c69fc8/buster/slim/rootfs.tar.xz',
        'rootfs.tar.xz')
    with tarfile.open('rootfs.tar.xz') as f:
        f.extractall('.')
    os.remove('/var/lib/box/env/mongodb/rootfs.tar.xz')

    dev = 'mount --bind /dev ' + mongo + '/dev'
    dev = dev.split()
    dev_file = subprocess.Popen(dev)

    sys = 'mount -t sysfs /sys ' + mongo + '/sys'
    sys = sys.split()
    sys_file = subprocess.Popen(sys)

    proc = 'mount -t proc /proc ' + mongo + '/proc'
    proc = proc.split()
    proc_file = subprocess.Popen(proc)


# Nous faisons notre chroot afin de définir la nouvelle racine pour exécuter notre application.
def chroot():
    os.chroot('/var/lib/box/env/mongodb')
    os.chdir("/") 


# Nous analysons le fichier yml afin de récpérer les commandes d'installation de mongodb puis nous appellons chroot() pour faire ces commandes dans l'environnement isolé.
def install():
    with open("/home/box/UNI2/box/box/mongo.yml", "r") as ymlfile:
        yml = yaml.safe_load(ymlfile)
        key = yml["repositories"]

    for section in yml:
        name_env = yml["name"]
        repository_env = yml["repository"]
        requirement = yml["requirements"]
        run = yml["run"]

    for value in key:
        key = value["key"]
       
    chroot() 
    
    os.system('apt -y update')
    os.system('apt -y install dirmngr gnupg apt-transport-https software-properties-common ca-certificates curl wget')

    os.system('wget -qO - ' + key + ' | apt-key add -')
    os.system('echo ' + repository_env + ' >> /etc/apt/sources.list')
    os.system('apt -y update')

    os.system ('apt -y install ' + requirement)
    os.system('apt -y update')
    os.mkdir('data')
    os.mkdir('/data/db')


# Fonction permettant lancer notre application
def mongodb():
    chroot() 
    os.system('mongod')


# On appelle toutes nos fonctions dans le bon ordre dans une seule et même fonction en vérifiant le nombre d'argument passé ainsi que leur valeur avant d'exécuter les différentes fonctions.
def script():
    if len(argv) == 2:
        if argv[1] == 'init':
            unmount()
            delete_folder()
            create_folder()
            tar()
            mount_filesystem()
            mogo()

    if len(argv) == 3:
        if argv[1] == 'build' and argv[2] == 'mongo.yml': 
            install()

    if len(argv) == 3:
        if argv[1] == 'run' and argv[2] == 'mongodb':
            mongodb()
