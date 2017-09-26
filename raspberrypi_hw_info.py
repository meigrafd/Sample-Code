#!/usr/bin/python3
#
# Get RaspberrPi Hardware Informations
# (c) 09.2017 by meigrafd
#
import re


# http://elinux.org/RPi_HardwareHistory#Which_Pi_have_I_got.3F
# https://github.com/WiringPi/WiringPi/blob/master/wiringPi/wiringPi.c#L807
# https://github.com/AndrewFromMelbourne/raspberry_pi_revision/blob/master/raspberry_pi_revision.c#L76


pi_model = {
    '0002': 'Released: Q1 2012; Model: 1 B; PCB Revision: 1.0; MEM: 256MB',
    '0003': 'Released: Q3 2012; Model: 1 B; PCB Revision: 1.0; MEM: 256MB; Maker: Egoman; Notes: ECN0001 (no fuses, D14 removed)',
    '0004': 'Released: Q3 2012; Model: 1 B: PCB Revision: 2.0; MEM: 256MB; Maker: Sony; Notes: Mounting holes',
    '0005': 'Released: Q4 2012; Model: 1 B; PCB Revision: 2.0; MEM: 256MB; Maker: Sony',
    '0006': 'Released: Q4 2012; Model: 1 B; PCB Revision: 2.0; MEM: 256MB; Maker: Qisda',
    '0007': 'Released: Q1 2013; Model: 1 A; PCB Revision: 2.0; MEM: 256MB; Maker: Egoman',
    '0008': 'Released: Q1 2013; Model: 1 A; PCB Revision: 2.0; MEM: 256MB; Maker: Sony',
    '0009': 'Released: Q1 2013; Model: 1 A; PCB Revision: 2.0; MEM: 256MB; Maker: Qisda',
    '000d': 'Released: Q4 2012; Model: 1 B; PCB Revision: 2.0; MEM: 512MB; Maker: Egoman',
    '000e': 'Released: Q4 2012; Model: 1 B; PCB Revision: 2.0; MEM: 512MB; Maker: Sony',
    '000f': 'Released: Q4 2012; Model: 1 B; PCB Revision: 2.0; MEM: 512MB; Maker: Qisda',
    '0010': 'Released: Q3 2014; Model: 1 B+; PCB Revision: 1.0; MEM: 512MB; Maker: Sony',
    '0011': 'Released: Q2 2014; Model: Compute Module 1; PCB Revision: 1.0; MEM: 512MB; Maker: Sony',
    '0012': 'Released: Q4 2014; Model: 1 A+; PCB Revision: 1.1; MEM: 256MB; Maker: Sony',
    '0013': 'Released: Q1 2015; Model: 1 B+; PCB Revision: 1.2; MEM: 512MB; Maker: ?',
    '0014': 'Released: Q2 2014; Model: Compute Module 1; PCB Revision: 1.0; MEM: 512MB; Maker: Embest, China',
    '0015': 'Released: ?; Model: 1 A+; PCB Revision: 1.1; MEM: 256MB / 512MB; Maker: Embest, China',
    'a01040': 'Released: ?; Model: 2 B; PCB Revision: 1.0; MEM: 1GB; Maker: Sony, UK',
    'a01041': 'Released: Q1 2015; Model: 2 B; PCB Revision: 1.1; MEM: 1GB; Maker: Sony, UK',
    'a21041': 'Released: Q1 2015; Model: 2 B; PCB Revision: 1.1; MEM: 1GB; Maker: Embest, China',
    'a22042': 'Released: Q3 2016; Model: 2 B; PCB Revision: 1.2; MEM: 1GB; Maker: Embest, China; Notes: with BCM2837',
    '900021': 'Released: Q3 2016; Model: 1 A+; PCB Revision: 1.1; MEM: 512MB; Maker: Sony, UK',
    '900032': 'Released: Q2 2016; Model: 1 B+; PCB Revision: 1.2; MEM: 512MB; Maker: Sony, UK',
    '900092': 'Released: Q4 2015; Model: Zero; PCB Revision: 1.2; MEM: 512MB; Maker: Sony, UK',
    '900093': 'Released: Q2 2016; Model: Zero; PCB Revision: 1.3; MEM: 512MB; Maker: Sony, UK',
    '920093': 'Released: Q4 2016; Model: Zero; PCB Revision: 1.3; MEM: 512MB; Maker: Embest, China',
    '9000c1': 'Released: Q1 2017; Model: ZeroW; PCB Revision: 1.1; MEM: 512MB; Maker: Sony, UK',
    'a02082': 'Released: Q1 2016; Model: 3 B; PCB Revision: 1.2; MEM: 1GB; Maker: Sony, UK',
    'a020a0': 'Released: Q1 2017; Model: Compute Module 3 (and CM3 Lite); PCB Revision: 1.0; MEM: 1GB; Maker: Sony, UK',
    'a22082': 'Released: Q1 2016; Model: 3 B; PCB Revision: 1.2; MEM: 1GB; Maker: Embest, China',
    'a32082': 'Released: Q4 2016; Model: 3 B; PCB Revision: 1.2; MEM: 1GB; Maker: Sony, Japan',
}


def get_cpuinfo():
    info=dict()
    try:
        fo = open('/proc/cpuinfo')
    except EnvironmentError as error:
        print('Error: {}'.format(error))
    else:
        for line in fo:
            name_value = [s.strip() for s in line.split(':', 1)]
            if len(name_value) != 2:
                continue
            name, value = name_value
            info[name] = value
        fo.close()
    return info


def main():
    warranty_void=False
    cpuinfo = get_cpuinfo()
    revision = cpuinfo['Revision']
    if re.search('[a-zA-Z]', revision):
        if revision[:1] == '3':
            warranty_void = True
            revision = revision[-(len(revision)-1):]
    else:
        # If longer than 4, we'll assume it's been overvolted
        warranty_void = len(revision) > 4
        if warranty_void:
            revision = revision[-4:]
    print( pi_model[revision] )


if __name__ == '__main__':
    main()


#EOF