#!/usr/bin/python
import os
import sys
import crypt
a = raw_input("Enter No. Of user :") 
def createuser (useradd1,passwd1):
	epass = crypt.crypt(passwd1,"22")
        return os.system(" useradd -p"+epass+ "-s" +"/bin/bash"+"-d"+"/home/"+useradd1+"-m"+"-c \"\"" +useradd1)


def sambaserver(user1):	
	f = raw_input ("Enter Directory name:")
	net = raw_input("Enter Network :")
	sb = raw_input("Enter you samba share name :")
	os.system('sudo apt-get install samba samba-common-bin -y')
	os.system("mkdir %s"%f )
	os.system("chcon -t samba_share_t %s "%f)
	os.system('echo [%s] >> /etc/samba/smb.conf'%sb)
	os.system('echo comment = public >> /etc/samba/smb.conf')
	os.system('echo path = %s >> /etc/samba/smb.conf'%f)
	os.system('echo public = yes >> /etc/samba/smb.conf')
	os.system('echo browsable = yes >> /etc/samba/smb.conf')
	os.system("echo valid users = %s >> /etc/samba/smb.conf"%user1)
	os.system("echo host allow = %s >> /etc/samba/smb.conf"%net)
	
	os.system("smbpasswd -a %s"%user1)
	os.system('sudo service samba restart')

for x in range(a)
	useradd = raw_input("Enter User name :")
        passwd = raw_input("Enter password :")
	createuser(useradd,passwd)
sambaserver(useradd)
