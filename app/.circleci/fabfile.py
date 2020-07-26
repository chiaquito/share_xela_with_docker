from fabric.api import env, run, cd, task, sudo
import os.path


#host = 'share_xela.ga'
HOST = '153.126.194.171'
PULL_DIR = '/home/chiaki/test_dir/'
APP_PATH = PULL_DIR + "app"

env.hosts = [HOST]
env.use_ssh_config = False
env.user = 'chiaki'
env.port = '21345'

env.key_filename = '~/.ssh/id_rsa'
#env.key_filename = '~/.ssh/circle_ci'



def test():
    #run('python -V')
    run("python3 -c 'import sys;print(sys.version)'")



class DeployHandler(object):

    def make_app_dir(self):
        with cd(env.pull_dir):
            run("MYDIR='/home/chiaki/test_dir'")
            if exists('/home/chiaki/tet_dir'):
                print("存在する")
            else:
                print("存在しない")


    #gitで指定するリポジトリからデータを取得する。
    def pull(self):
        with cd(PULL_DIR):
            #run("git remote -v")
            #run("git remote add origin chiaki@github.com:chiaki1990/share_xela_with_docker")
            run("git pull origin master")
            #run("git clone https://github.com/chiaki1990/share_xela_with_docker.git")


    def install_dependencies(self):
        with cd(APP_PATH):
            run("python3 -m pip install -r requirements.txt")


    def makemigrations(self):
        with cd(APP_PATH):
            run("python3 manage.py makemigrations --settings=config.settings.prod_settings")

    def migrate(self):
        with cd(APP_PATH):
            run("python3 manage.py migrate --settings=config.settings.prod_settings")

    def collectstatic(self):
        with cd(APP_PATH):
            run("python3 manage.py collectstatic --no-input --settings=config.settings.prod_settings")


    def command_ls(self):
        with cd(APP_PATH):
            pass

    def kill_process(self):
        with cd(APP_PATH):
            run("pkill gunicorn") 

    def restart(self):
        with cd(APP_PATH):
            run("gunicorn --daemon --bind 127.0.0.1:8000 --env DJANGO_SETTINGS_MODULE=config.settings.prod_settings config.wsgi:application")
        





@task
def deploy():
    dh = DeployHandler()
    #dh.make_app_dir()
    #dh.command_ls()
    dh.pull()
    dh.install_dependencies()
    dh.makemigrations()
    dh.migrate()
    dh.collectstatic()
    dh.kill_process()
    dh.restart()