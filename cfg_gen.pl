use strict;
use warnings;
use Cwd;

my $config_file_content = <<'END_CONFIG';
# AUTO GENERATED FILE
# DO NOT TOUCH THIS FILE IF YOU DON'T KNOW WHAT YOU'RE DOING

[DEFAULT]
LOGS_PATH = 
PIPER_DATA_PATH = 
TEMP_PATH = 

END_CONFIG

my $config_file_path = 'kreacher.cfg';

# change the value of LOGS_PATH
$config_file_content =~ s/LOGS_PATH = .*/LOGS_PATH = $ENV{'PWD'}\/logs/;

# change the value of PIPER_DATA_PATH
$config_file_content =~ s/PIPER_DATA_PATH = .*/PIPER_DATA_PATH = $ENV{'PWD'}\/container\/piper/;

# change the value of TEMP_PATH
$config_file_content =~ s/TEMP_PATH = .*/TEMP_PATH = $ENV{'PWD'}\/temp/;

open(my $fh, '>', $config_file_path) or die "Could not open file $config_file_path: $!";
print $fh $config_file_content;
close $fh;

print "Configuration file created at $config_file_path\n";