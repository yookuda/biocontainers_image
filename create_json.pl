#!/usr/bin/perl
use strict;
use warnings;
use utf8;
use Encode;
use JSON;

open IN, $ARGV[0] or die;
my $dir = '';
#my $data = { 'dir' => '', 'image' => '', 'commands' => [], 'shared_libraries' => [] };
my $data = undef;
while (<IN>) {
    chomp;
    if (/^DIR:(.*)$/) {
        $dir = $1;
    } elsif (/^IMAGE:(.*)$/) {
        my $image = $1;
        if ($data) {
            &output_data($data);
        }
        $data = { 'dir' => $dir, 'image' => $image, 'commands' => [], 'shared_libraries' => [] };
    } elsif (/^LIBRARY:(.*)$/) {
        my $library = $1;
        $library =~ s/^.*\/([^\/]+)$/$1/;
        push @{$data->{'shared_libraries'}}, $library;
    } elsif (/^COMMAND:(.*)$/) {
        push @{$data->{'commands'}}, $1;
    }
}
close IN;
&output_data($data);

sub output_data {
    my $data = $_[0];
    my $json = decode('utf-8', encode_json($data));
    print "$json\n\n";
}
