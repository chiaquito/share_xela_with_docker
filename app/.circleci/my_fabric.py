#構築済みのサーバーに対してgithubからpullを実行するコードを書く.


やることはconfigファイルの中でデプロイ部分を完成させる
そのあとはcircleciに秘密の鍵を登録する
そしてfabricの使い方を調べて書く。
一応どんな感じなのか調べる。
cinfigファイルのworlflowsについて書き方を調べておきたい。。。



#環境変数をfabricで登録してみる



#!/usr/bin/python2

from fabric.api import env, run, cd, task

debug = False

"""
Fabric deploy script

This is a Fabric (python 2.7) deployment script to be used by CircleCI to
deploy this project automatically to either production or staging.
"""

if debug:
    import paramiko
    paramiko.common.logging.basicConfig(level=paramiko.common.DEBUG)

env.venv_name = 'django-circleci-example'
env.path = '~/django-circleci-example'
env.user = 'admin'
env.gateway = 'timmyomahony.com:30000'


@task
def production():
    env.branch = 'master'
    env.hosts = ['timmyomahony.com:30000', ]


@task
def staging():
    env.branch = 'develop'
    env.hosts = ['timmyomahony.com:30000', ]


@task
def venv(cmd):
    run('workon {0} && {1}'.format(env.venv_name, cmd))


@task
def deploy():
    with cd(env.path):
        run('git pull origin {0}'.format(env.branch))
        venv('pip install -r requirements.txt')
        venv('python3 manage.py migrate')
        venv('python3 manage.py collectstatic --noinput')
        run('supervisorctl reread')
        run('supervisorctl update')
        run('supervisorctl restart django-circleci-example')