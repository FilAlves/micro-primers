#!/usr/local/bin/perl
####Programa para obtener la longitud de cada una de las secuencias de un fichero fasta;
if ((!$ARGV[0]) && (!$ARGV[1])){
	print "introduce name of fasta file: ";
	$name=<STDIN>;
	chomp $name;
	print "introduce name of micros list (ID start end seq_length): ";
	$list=<STDIN>;
	chomp $list;
}else{
	$name=$ARGV[0];
	chomp $name;
	$list=$ARGV[1];
	chomp $list;
}

		open (fasta,"$name") || die "Error: problem opening fasta file\n";
		open (results,">.temp/split_out.fasta");

	while (<fasta>){
			chomp $_;
			if ($_=~/^\>/){
			($simbol,$ID)=split(/\>/,$_);
			}else{
				$seq=$_;
			$fasta{$ID}=$seq;
			}
		}
	open (table, "$list") || die "Error: problem opening table\n";

while (<table>){
	chomp $_;
	($identificador,$start,$end,$seq_length)=split(/\t/,$_);
	$length_fin=$seq_length-$end;
	$seq_ini=substr($fasta{$identificador},0,$start-1);
	$seq_fin=substr($fasta{$identificador},$end,$length_fin);

print results ">$identificador\n$seq_ini"."$seq_fin\n";

}
