#!/usr/bin/env perl
use strict;
use warnings;

# Minimal genetic algorithm scaffold: population init and mutation demo
my $pop_size   = $ENV{GA_POP_SIZE}   // 20;
my $genome_len = $ENV{GA_GENOME_LEN} // 16;
my $mut_rate   = $ENV{GA_MUT_RATE}   // 0.05;

sub rand_genome {
    my ($len) = @_;
    my $g = '';
    for (1..$len) { $g .= int(rand(2)); }
    return $g;
}

sub mutate {
    my ($g, $rate) = @_;
    my @c = split('', $g);
    for my $i (0..$#c) {
        if (rand() < $rate) { $c[$i] = $c[$i] eq '0' ? '1' : '0'; }
    }
    return join('', @c);
}

my @pop = map { rand_genome($genome_len) } (1..$pop_size);
my @mut = map { mutate($_, $mut_rate) } @pop;

print "init:\n";
print join("\n", @pop), "\n";
print "\nafter-mutation:\n";
print join("\n", @mut), "\n";
