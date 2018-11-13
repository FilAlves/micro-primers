#!/usr/local/bin/perl

if ((!$ARGV[0]) && (!$ARGV[1])){
     print "Please introduce the name of your primer3 output file: ";
    $output=<STDIN>;
    chomp $output;
print "Introduce the name of your selected reads with start and end included: ";
    $list=<STDIN>;
    chomp $list;
}else{
    $output=$ARGV[0];
    chomp $output;
    $list=$ARGV[1];
    chomp $list;
}
open (file, "$list")|| die "Error: problem opening $list\n";
while (<file>){
	chomp $_;
	($id,$motif,$start,$end)=split(/\t/,$_);
	$ref{$id}="$motif $start $end";
}
open (output, "$output") || die "Error: problem opening $output\n";
open (results, ">final_primers.txt");

while (<output>){
	chomp $_;
	if ($_=~/^SEQUENCE_ID=/){
		($aa,$identificador)=split(/\=/,$_);
		#print "$identificador-------\n";
	}elsif($_=~/^PRIMER_LEFT_(\d)_SEQUENCE/){
		$count=$1;
		#print "$count\n";
		($bb,$left)=split(/\=/,$_);
	}elsif($_=~/^PRIMER_RIGHT_(\d)_SEQUENCE/){
		($cc,$right)=split(/\=/,$_);
	}elsif($_=~/^PRIMER_LEFT_\d_TM=/){
		($dd,$temp_left)=split(/\=/,$_);
	}elsif($_=~/^PRIMER_RIGHT_\d_TM=/){
                ($dd,$temp_right)=split(/\=/,$_);
	}elsif($_=~/^PRIMER_LEFT_\d=(\d*),(\d*)/){
		$ini_left=$1;
		$len_left=$2;
		print "$ini_left++++$len_left\n";
	}elsif($_=~/^PRIMER_RIGHT_\d=(\d*),(\d*)/){
		$ini_right=$1;
                $len_right=$2;
		print "$ini_right++++$len_right\n";
	}elsif($_=~/^PRIMER_PAIR_\d_PRODUCT_SIZE=(\d*)/){
		$product=$1;

		($motif,$start,$end)=split(/\s/,$ref{$identificador});
		#print "$ref{$identificador}/////$motif//////$start/////$end\n";
		$good_left=$ini_left+$len_left;$good_right=$ini_right-$len_right;
		print "$good_left//$start//$good_right//$end\n";
		if (($good_left<$start) && ($good_right>$end)){
			if ($count==0){
				print results "$identificador\t$product\t$left\t$temp_left\t$right\t$temp_right\t$motif\tbest\n";
			}else{
				print results "$identificador\t$product\t$left\t$temp_left\t$right\t$temp_right\t$motif\n";
			}
		}else{
		next;
		}
	}
}
