#!/usr/bin/perl

use HTML::WikiConverter;

$xml = "";
while (<STDIN>) {
  s/^[ ,\t]*//;
  $xml .= $_
}

my $wc = new HTML::WikiConverter( dialect => 'MoinMoin' );
print $wc->html2wiki( $xml );
