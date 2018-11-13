#!/usr/local/bin/perl

if ((!$ARGV[0]) && (!$ARGV[1])){
     print "Please introduce the file with list of IDs (can include more tab info): ";
    $lista=<STDIN>;
    chomp $lista;
print "Introduce the name of your reference file: ";
    $ref=<STDIN>;
    chomp $ref;
}else{
    $lista=$ARGV[0];
    chomp $lista;
    $ref=$ARGV[1];
    chomp $ref;
}
open (codigos,"$ref") || die "Error: problem opening $ref\n";
while (<codigos>){
    chomp $_;
  ($identificador,@info)=split(/\t/,$_);
   $lineacompleta= join("\t",@info);
    $gen{$identificador}=$lineacompleta;
    $count++;
}
close (codigos);

open (fichero,"$lista") || die "Error: problem opening $name".".txt\n";
open (results,">.temp/cluster_info_out.txt");
while (<fichero>){
    chomp $_;
	($name,@resto)=split(/\,/,$_);
	($id,$rest)=split(/\_/,$name);
    if ($gen{$id}){
	$cuenta++;
	print results "$_\t$gen{$id}\n";
	}else{
	print results "$_\n";
	next;
   }
}


#    print "$count---$lineas---$cuenta\n";
    close (fichero);
    close (results);
