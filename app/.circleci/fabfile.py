from fabric.api import env, run, cd, task, sudo
import os.path
import os


#host = 'share_xela.ga'
HOST = '153.126.194.171'
PULL_DIR = '/home/chiaki/sharexela_src/'
APP_PATH = PULL_DIR

env.hosts = [HOST]
env.use_ssh_config = False
env.user = 'chiaki'
env.port = '21345'
env.key_filename = '~/.ssh/id_rsa'
GUNICORN_CONF = APP_PATH + "/.circleci/" + "gunicorn_conf.py"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.prod_settings")




def test():
    """
    fab testが実行できるかのテスト
    バージョンが表示されなければfabric自体が起動できていない。
    """
    run("python3 -c 'import sys;print(sys.version)'")





class DeployHandler(object):

    def make_app_dir(self):
        """
        デプロイ先のディレクトリが存在するか確認する。
        存在しなければディレクトリを作成する。
        """
        with cd(PULL_DIR):
            run("MYDIR='/home/chiaki/sharexela_src'")
            if exists('/home/chiaki/tet_dir'):
                print("存在する")
            else:
                print("存在しない")
                run("mkdir /home/chiaki/sharexela_src")


    def pull(self):
        """
        githubの指定するリポジトリからソースコードを取得する。
        """
        with cd(PULL_DIR):
            #run("git remote -v")
            run("git pull origin master")


    def install_dependencies(self):
        """
        デプロイに必要になるライブラリをインストールする
        """
        with cd(APP_PATH):
            run("python3 -m pip install -r requirements.txt")


    def makemigrations(self):
        """
        makemigrationsの実行
        """
        with cd(APP_PATH):
            run("python3 manage.py makemigrations --settings=config.settings.prod_settings")

    def migrate(self):
        """
        migrateの実行
        """
        with cd(APP_PATH):
            run("python3 manage.py migrate --settings=config.settings.prod_settings")

    def collectstatic(self):
        """
        staticfileの収集
        """
        with cd(APP_PATH):
            run("python3 manage.py collectstatic --no-input --settings=config.settings.prod_settings")



    def kill_process(self):
        """
        gunicornのプロセスをkillする
        gunicorn実行時にオプションとしてpidfileを追加しないと、プロセスを切るときにエラーが生じる.
        """
        with cd(APP_PATH):
            run('kill -HUP `cat .circleci/gunicorn.pid`', warn_only=True)


    def restart(self):
        """
        アプリケーションの起動
        """
        with cd(APP_PATH):
            #run("gunicorn --daemon --bind 127.0.0.1:8000 --env DJANGO_SETTINGS_MODULE=config.settings.prod_settings config.wsgi:application")
            run("gunicorn --daemon --env DJANGO_SETTINGS_MODULE=config.settings.prod_settings config.wsgi:application -c {}".format(GUNICORN_CONF), pty=False)


    def restart_with_supervisor(self):
        with cd(APP_PATH):                
            run('supervisorctl reread')
            run('supervisorctl update')
            run('supervisorctl restart sharexela')



@task
def deploy():
    dh = DeployHandler()
    dh.pull()
    dh.install_dependencies()
    dh.makemigrations()
    dh.migrate()
    dh.collectstatic()
    dh.kill_process()
    dh.restart()
    dh.restart_with_supervisor()