use strict;
use warnings;
use Cwd;

my $config_file_content = <<'END_CONFIG';

# AUTO GENERATED FILE
# DO NOT TOUCH THIS FILE IF YOU DON'T KNOW WHAT YOU'RE DOING

[DEFAULT]
PIPER_MODELS_PATH = 
LOG_FILE_PATH = 

END_CONFIG

my $config_file_path = 'kreacher.cfg';

# change the value of PIPER_MODELS_PATH
$config_file_content =~ s/PIPER_MODELS_PATH = .*/PIPER_MODELS_PATH = $ENV{'PWD'}\/container\/piper\/models/;

# change the value of LOG_FILE_PATH
$config_file_content =~ s/LOG_FILE_PATH = .*/LOG_FILE_PATH = $ENV{'PWD'}\/logs\/kreacher.log/;

open(my $fh, '>', $config_file_path) or die "Could not open file $config_file_path: $!";
print $fh $config_file_content;
close $fh;

print "Configuration file created at $config_file_path\n";