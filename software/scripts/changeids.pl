#!/usr/local/bin/perl

if (!$ARGV[0]){
        print "introduce name of fasta file: ";
        $name=<STDIN>;
        chomp $name;
}else{
        $name=$ARGV[0];
        chomp $name;
}
($id,$ext)=split(/\./,$name);
                open (codigos,"$name") || die "Error: problem opening fasta file\n";
                open (results,">.temp/ids_out.fasta");


                $count=0;
                while (<codigos>){
                        chomp $_;
                        if ($_=~/^\>/){
				($kk,$resto)=split(/\>/,$_);
                                $count++;
                                print results ">$count"."_$resto\n";
                        }else{
                                print results "$_\n";
                                }
                }
