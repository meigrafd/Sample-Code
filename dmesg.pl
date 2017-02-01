#!/usr/bin/perl

use strict;
use warnings;

my @dmesg_new = ();
my $dmesg = "/bin/dmesg";
my @dmesg_old = `$dmesg`;
my $now = time();
my $uptime = `cat /proc/uptime | cut -d"." -f1`;
my $t_now = $now - $uptime;

foreach my $line ( @dmesg_old )
{
	chomp( $line );
	if( $line =~ m/\[\s*(\d+)\.(\d+)\](.*)/i )
	{
		# now - uptime + sekunden
		my $t_time = scalar localtime( $t_now + $1 );
		push( @dmesg_new , "[ $t_time ] $3" );
	}
}

print join( "\n", @dmesg_new );
print "\n";

