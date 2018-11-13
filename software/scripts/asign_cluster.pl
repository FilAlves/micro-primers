#!/usr/local/bin/perl

if (!$ARGV[0]){
        print "introduce name of cdhit cluster file: ";
        $name=<STDIN>;
        chomp $name;
}else{
        $name=$ARGV[0];
        chomp $name;
}
open (file,"$name") || die "Error: problem opening cluster file\n";
open (results, ">.temp/clusters_out.txt");

while (<file>){
	if ($_=~/^\>/){
	$real=$total+1;
	#@combo=();
	for ($i=0;$i<=$total;$i++){
                        print results "$info{$num}{$i}\t$real\n";

	}
        ($kk,$resto)=split(/\>/,$_);
	($cluster,$num)=split(/\s/,$resto);
	#print results "\t\t\t$real\n";
	}
	else{
	$total=0;
	($total,$len,$chicha)=split(/\s+/,$_);
	($todo,$demas)=split(/\-/,$chicha);
	($sign,$bien)=split(/\>/,$todo);
	($index,$aaa)=split(/\_/,$bien);
	$info{$num}{$total}="$index"."\t$num";
	#$kk{$num}{$library}="yes";
	#print results "$index"."_$library"."\t$num\n";
	}
}
for ($i=0;$i<=$total;$i++){

 print results "$info{$num}{$i}\t$real\n";
  #              }elsif(($kk{$num}{pool})&&(!$kk{$num}{sample6})){
   #                     print results "$info{$num}{$i}\t$real\t1\n";
    #            }elsif((!$kk{$num}{pool})&&($kk{$num}{sample6})){
     #                   print results "$info{$num}{$i}\t$real\t1\n";
      #          }

 }
close (results);
#open (new, "list.clusters.txt");
#open (results2, ">clusters_list.txt");
#	$a2="kk";
#	while(<new>){
#	chomp $_;
#	($a1,$a2,$a3)=split(/\t/,$_);
#	($ind,$name)=split(/\_/,$a1);
#		if(($info{$a2}{$a3}{pool})&&($info{$a2}{$a3}{sample6})){
#			$presence=2;
#		}elsif(($info{$a2}{$a3}{pool})&&(!$info{$a2}{$a3}{sample6})){
#			$presence=1;
#		}elsif((!$info{$a2}{$a3}{pool})&&($info{$a2}{$a3}{sample6})){
#			$presence=1;
#		}
	#if ($a2=$a2_prev){
	#	push (@comb,$name);
	#}else{
	#	$count=scalar(grep $_,@comb);
	#	@comb=();
	#	push (@comb,$name);
#		print results2 "$ind"."_$name\t$a2\t$a3\t$presence\n";
	#}else{
	#	$count=scalar(grep $_,@comb);
	#	@comb=();
	#	push (@comb,$name);
	#	print results2 "$complete{$indd
#}
