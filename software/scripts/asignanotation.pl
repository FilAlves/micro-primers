#!/usr/local/bin/perl
#Programa para la asignacion de anotaciones a una lista de identificadores en comun. Puede modificarse para usarse como un simple adicionador de columnas en matches por ID. 

if ((!$ARGV[0]) && (!$ARGV[1])){
     print "Introduzca el nombre del documento que contiene su lista de nombres: ";
    $lista=<STDIN>;
    chomp $lista;
print "Introduzca el nombre del documento que contiene la longitud de todas las secuencias: ";
    $ref=<STDIN>;
    chomp $ref;
}else{
    $lista=$ARGV[0];
    chomp $lista;
    $ref=$ARGV[1];
    chomp $ref;
}
open (codigos,"$ref") || die "Error: problem opening todas_anotaciones.txt\n";
while (<codigos>){
    chomp $_;
  ($identificador,$GO)=split(/\t/,$_);
  # $lineacompleta= join("\t",$GO,$interpro,$intact,$keywords,$pathway,$orthologo);
$gen{$identificador}=$GO;
    $count++;
# print "$gen{$identificador}\n";
}
close (codigos);

open (fichero,"$lista") || die "Error: problem opening $name".".txt\n";
open (results,">$lista"."_annotation.txt");
#print results "ID\tGO\tInterPro\tIntAct\tKeywords\tPathway\tOrthologous\n";
while (<fichero>){
    chomp $_;
	$id=$_;
    if ($gen{$id}){
	$cuenta++;
	print results "$id\t$gen{$id}\n";
	}else{
	next;
   }
}


#    print "$count---$lineas---$cuenta\n";
    close (fichero);
    close (results);
