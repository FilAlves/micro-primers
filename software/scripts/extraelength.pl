#!/usr/local/bin/perl
####Programa para obtener la longitud de cada una de las secuencias de un fichero fasta;
if (!$ARGV[0]){
	print "introduce name of fasta file: ";
	$name=<STDIN>;
	chomp $name;
}else{
	$name=$ARGV[0];
	chomp $name;
}

		open (codigos,"$name") || die "Error: problem opening fasta file\n";
		open (results,">.temp/length_calc_out.fasta");
	$length=0;
	while (<codigos>){
			chomp $_;
			if ($_=~/^\>/){
				$length=length($seq);
				print results "$id\t$length\n";
				$seq="";
				#if ($length > 150){
				#	print results ">$id\n$seq\n";
				#}else{
				#	next;
				#}
				($a1,$id)=split(/\>/,$_);
			}else{

				$seq.=$_;
				}
		}
	$length=length($seq);
print results "$id\t$length\n";
