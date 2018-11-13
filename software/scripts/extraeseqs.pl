#!/usr/local/bin/perl
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
		open (results,">.temp/pseudo_out.fasta");

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
	$identificador=$_;

print results "SEQUENCE_ID=$identificador\nSEQUENCE_TEMPLATE=$fasta{$identificador}\n=\n";

}
