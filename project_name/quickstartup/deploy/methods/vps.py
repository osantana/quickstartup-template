# coding: utf-8

from decouple import config
from fabric.context_managers import cd, settings
from fabric.contrib.files import append, sed
from fabric.operations import sudo, local
from fabric.state import env
from fabric.utils import abort

from ..helpers import get_key_from_file, gen_random_string
from .base import BaseDeployer


class VPSBaseDeployer(BaseDeployer):
    def _initialize_package_system(self):
        sudo("apt-get update", quiet=True)
        sudo("apt-get -q -y install aptitude")
        sudo("aptitude -q -y safe-upgrade")

    def _install_packages(self, pkglist):
        if isinstance(pkglist, basestring):
            pkglist = [pkglist]

        sudo("aptitude -q -y install {}".format(" ".join(pkglist)))

    def _restart_service(self, service):
        sudo("touch /tmp/restart-{}".format(service))

    def _save_etc(self, message):
        with cd("/etc"):
            sudo("git add -A")
            sudo("git commit -m '{}' || true".format(message))

    def _initialize_etc_versioning(self):
        with settings(warn_only=True):
            email = local("git config --get user.email", capture=True)
            name = local("git config --get user.name", capture=True)

        if not email:
            email = "deployer@quickstartup.us"

        if not name:
            name = "Quickstartup Deployer"

        self._install_packages("git-core")

        with cd("/etc"):
            sudo("git init -q")
            sudo("git config --global user.name '{}'".format(name))
            sudo("git config --global user.email '{}'".format(email))

        self._save_etc("Basic Configuration")

        sudo("chmod -R go-rwx /etc/.git")

    def _setup_host(self, ip, hostname, locales=""):
        # host
        sudo("echo '{}' > /etc/hostname".format(hostname))
        sudo("hostname -F /etc/hostname")
        append("/etc/hosts", "{} {}".format(ip, hostname), use_sudo=True)

        # locale
        sudo("locale-gen en_US.UTF-8 {}".format(locales))
        sudo("dpkg-reconfigure locales -f noninteractive")

        # clock
        sudo("ln -s -f /usr/share/zoneinfo/UTC /etc/localtime")
        self._install_packages("ntp")
        sudo("touch /tmp/restart-cron")

        # extra packages
        self._install_packages(["python-software-properties", "rsyslog", "htop", "iotop", "wget", "vim", "less",
                                "build-essential", "logrotate", "screen", "curl"])

        self._save_etc("Basic Host Setup")

    def _setup_security(self):
        self._install_packages(["ufw", "fail2ban"])

        # ssh
        sed("/etc/ssh/sshd_config", "^X11Forwarding yes$", "X11Forwarding no", use_sudo=True)
        sed("/etc/ssh/sshd_config", "^PermitRootLogin yes$", "PermitRootLogin no", use_sudo=True)
        append("/etc/ssh/sshd_config", "UseDNS no")
        self._restart_service("ssh")

        # firewall
        sudo("ufw logging on")
        sudo("ufw default deny")
        sudo("ufw allow ssh/tcp")
        sudo("ufw limit ssh/tcp")
        sudo("ufw allow http/tcp")
        sudo("ufw allow https/tcp")
        sudo("ufw --force enable")

        self._save_etc("Basic Security Settings enabled")

    def _add_user(self, username, password=None, sudoer=False):
        sudo("adduser --disabled-password --gecos '' '{}'".format(username))

        if password:
            sudo("echo '{}:{}' | chpasswd".format(username, password), quiet=True)

        if not sudoer:
            return

        append("/etc/sudoers.d/{}".format(username), "{} ALL=(ALL) NOPASSWD:ALL".format(username))
        sudo("chmod 0440 /etc/sudoers.d/{}".format(username))

    def _setup_user(self, username, pubkey, password=None):
        if not password:
            password = gen_random_string(10)
            sed("/etc/ssh/sshd_config", "^#PasswordAuthentication yes$", "PasswordAuthentication no", use_sudo=True)
            self._restart_service("ssh")

        self._install_packages("sudo")

        self._add_user(username, password, sudoer=True)

        # put his/her pubkey as authorized key
        sudo("mkdir -p /home/{}/.ssh".format(username))
        append("/home/{}/.ssh/authorized_keys".format(username), pubkey, use_sudo=True)
        sudo("chown -R '{username}':'{username}' /home/{username}/.ssh".format(username=username))
        sudo("chmod 0700 /home/{username}/.ssh".format(username=username))
        sudo("chmod 0600 /home/{username}/.ssh/*".format(username=username))

        # limit ssh access to this user
        append("/etc/ssh/sshd_config", "AllowUsers {}".format(username))

        self._save_etc("Finished user setup for {}".format(username))

    def _setup_environment(self):
        # postfix
        sudo("echo 'postfix postfix/main_mailer_type select Internet Site' | debconf-set-selections")
        sudo("echo 'postfix postfix/mailname string localhost' | debconf-set-selections")
        sudo("echo 'postfix postfix/destinations string localhost.localdomain, localhost' | debconf-set-selections")
        self._install_packages(["postfix", "bsd-mailx"])
        sudo("/usr/sbin/postconf -e 'inet_interfaces = loopback-only'")
        self._restart_service("postfix")

        # postgresql
        self._install_packages(["postgresql-9.3-postgis-2.1", "postgresql-9.3-postgis-scripts",
                                "postgresql-contrib-9.3", "postgresql-client-9.3",
                                "libpq-dev"])

        # redis
        self._install_packages(["redis-server", "redis-tools"])

        # nginx
        self._install_packages(["nginx-extras"])

        # python
        self._install_packages(["python", "python-dev", "python-setuptools"])
        sudo("easy_install pip")
        sudo("pip install -q -U setuptools")
        sudo("pip install -q -U pip")
        sudo("pip install -q -U virtualenv")
        sudo("pip install -q -U psycopg2")
        sudo("pip install -q -U redis")
        sudo("pip install -q -U uwsgi")

        self._save_etc("Support Services installed.")

    def _setup_finalize(self):
        # execute all requested service restart
        sudo("for s in $(ls /tmp/restart-* | cut -d- -f2-); do "
             "  service \"${s}\" restart && rm -f \"/tmp/restart-${s}\"; "
             "done")

        sudo("touch /etc/setup-done")
        self._save_etc("Setup done.")

    def setup(self, hostname, server_ip, username, user_pubkey, extra_locales="", password=None):
        pubkey = get_key_from_file(user_pubkey)
        if not pubkey:
            abort("Cannot open public key file {}".format(user_pubkey))

        env.user = "root"
        env.host_string = server_ip

        self._initialize_package_system()
        self._initialize_etc_versioning()

        self._setup_host(server_ip, hostname, extra_locales)
        self._setup_security()
        self._setup_user(username, pubkey, password)
        self._setup_environment()
        self._setup_finalize()

    def deploy(self, **kwargs):
        print "ok"

