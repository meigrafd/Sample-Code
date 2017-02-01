#!/bin/bash -e
#
#   Version: 0.1
#   Creator: meigrafd
#   Copyright (C) 2013 by meiraspi@gmail.com published under the MIT License
#
# Edit to /etc/crontab:
# 28 4 * * * root if test -x /usr/local/sbin/aptcron; then /usr/local/sbin/aptcron; else true; fi
#
# Install sendemail: apt-get install sendemail libnet-ssleay-perl libio-socket-ssl-perl
# Edit /usr/bin/sendEmail and change
#    if (! IO::Socket::SSL->start_SSL($SERVER, SSL_version => 'SSLv23:!SSLv2')) {
# to
#    if (! IO::Socket::SSL->start_SSL($SERVER, SSL_version => 'TLSv1')) {
#
# required system cmd's:
# sendEmail apt grep cat cut sort sed touch mktemp wc basename
#

### CONFIG - START

SMTP_FROM='pi@gmail.com'
SMTP_TO='target@email.com'
SMTP_SERVER='pop.gmail.com'
SMTP_PORT=587
SMTP_LOGIN='xxx@gmail.com'
SMTP_PASS='passwd'
SMTPTLS=1
SUBJECT="apt cron $(date)"

### CONFIG - END


# -------------------------------------------------------------- #
# >>> >> >  DO NOT MESS WiTH ANYTHiNG BELOW THiS LiNE!  < << <<< #
# -------------------------------------------------------------- #


tmpfile=$(mktemp -t aptcron.XXXXXXXXXX)

# update the package lists
apt-get -qq update > ${tmpfile} 2>&1

# get the list of packages which are pending an upgrade
PKGNAMES=$(apt-get -q -y --ignore-hold --allow-unauthenticated -s upgrade | grep ^Inst | cut -d" " -f2 | sort)
NUM_PACKAGES=$(echo $PKGNAMES | wc -w)

if [ -n "$PKGNAMES" ]; then
    echo "$(basename $0) has detected $NUM_PACKAGES packages need upgrading for: $(hostname)" >> ${tmpfile}
    echo "The following packages are currently pending an upgrade:" >> ${tmpfile}
    echo "" >> ${tmpfile}
	for PKG in $PKGNAMES ; do
        VER=$(LC_ALL=C apt-cache policy $PKG | grep Candidate: | cut -f4 -d" ")
        VERFILE=$(echo "$VER" | sed -e "s/:/%3a/g")
        echo -e "\t"$PKG $VER >> ${tmpfile}
    done
    echo "" >> ${tmpfile}
    # send email..
    if [ -n "$SMTPTLS" ] && [ $SMTPTLS == 1 ]; then
        sendEmail -f $SMTP_FROM -t $SMTP_TO -u $SUBJECT -m $(cat ${tmpfile}) -o tls=yes -s "$SMTP_SERVER:$SMTP_PORT" -xu "$SMTP_LOGIN" -xp "$SMTP_PASS"
    else
        sendEmail -f $SMTP_FROM -t $SMTP_TO -u $SUBJECT -m $(cat ${tmpfile}) -s "$SMTP_SERVER:$SMTP_PORT" -xu "$SMTP_LOGIN" -xp "$SMTP_PASS"
    fi
    # do the upgrade downloads
    apt-get --ignore-hold -qq -d --allow-unauthenticated --force-yes upgrade > /dev/null
fi

rm -f ${tmpfile}
exit 0

#EOF