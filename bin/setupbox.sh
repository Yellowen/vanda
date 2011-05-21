#! /bin/sh

# this script should run with root user.

adduser --system --no-create-home debbox
addgroup --system debbox
adduser debbox debbox
mkdir /var/log/debbox -p
mkdir /var/lib/debbox -p
mkdir /var/lib/debbox/vpkg -p
touch /var/lib/debbox/vpkg/installed_apps
chown debbox.debbox /var/lib/debbox -R
chown debbox.debbox /var/log/debbox -R

