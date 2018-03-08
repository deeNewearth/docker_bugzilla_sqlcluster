#!/usr/bin/perl -w
use strict;
use warnings;

use DBI;
print("starting init db\n");
#print("pwd is $ENV{'MYSQL_ROOT_PASSWORD'}");

my $dbh;

for (my $i=0; $i <= 9 && !$dbh; $i++) {
   $dbh  = DBI->connect("DBI:mysql:host=$ENV{'MYSQL_HOST'}",$ENV{'MYSQL_USER'},$ENV{'MYSQL_ROOT_PASSWORD'});
   if(!$dbh){
		print("Failed to connect will try again, try : $i\n");
		sleep(5);
   }
}



print "creating database $ENV{'MYSQL_DB'}";
$dbh->do("create database $ENV{'MYSQL_DB'}") or die "Cannot create database \n ";
print "created database\n";
