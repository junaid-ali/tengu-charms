#!/bin/bash

function apache_self_signed_ssl {
    a2enmod ssl
    mkdir /etc/apache2/ssl
    function echodo()
    {
        echo "${@}"
        (${@})
    }

    function yearmon()
    {
        date '+%Y%m%d'
    }

    function fqdn()
    {
        hostname --fqdn
    }

    C=BE
    ST=OV
    L=Ghent
    O=Tengu
    OU=Tengu
    HOST=${1:-`hostname`}
    DATE=`yearmon`
    CN=`fqdn`
    EMAIL="merlijn.sebrechts@gmail.com"

    csr="${HOST}.csr"
    key="${HOST}.key"
    cert="${HOST}.cert"

    # Create the certificate and key
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/apache2/ssl/apache.key -out /etc/apache2/ssl/apache.crt <<EOF
${C}
${ST}
${L}
${O}
${OU}
${CN}
$EMAIL
EOF
}


apt-get install -y python-pip redis-server libapache2-mod-wsgi apache2
pip install snappass
# load wsgi mod
a2enmod wsgi

# create site
cp templates/snappass-site.conf /etc/apache2/sites-available/snappass-site.conf
# enable site
ln -s /etc/apache2/sites-available/snappass-site.conf /etc/apache2/sites-enabled/snappass-site.conf
# create snappass script
mkdir /var/www/snappass/
cp templates/snappass.wsgi /var/www/snappass/snappass.wsgi


apache_self_signed_ssl

service apache2 restart

#cp templates/upstart.conf /etc/init/snappass.conf



#service snappass start
