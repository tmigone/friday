FROM pihole/pihole:4.3.1-4_armhf
LABEL author "Tomás Migone"
LABEL maintainer "tomasmigone@gmail.com"

# Fixes required to run on balenaOS
RUN sed -i '/$AUTHORIZED_HOSTNAMES = array(/ a "balena-devices.com",' /var/www/html/admin/scripts/pi-hole/php/auth.php
RUN echo "bind-interfaces" >> /etc/dnsmasq.conf