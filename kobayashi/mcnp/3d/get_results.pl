#!/usr/bin/perl

# collect tallies for Kobayashi benchmarks

$OUT = "results.txt";

@problems = (
		 "prob1_abs", "prob1_sct", 
		 "prob2_abs", "prob2_sct", 
		 "prob3_abs", "prob3_sct"
            ); 
bench_results();

open(OUT,">$OUT");

foreach $case (@problems) {

  $mctal   = $case . ".m";

  if( ! -s $mctal ) { next; }

  print  "...collect results for case= $case\n";

  open(MCTAL,"<$mctal") || die("***** can't open mctal file: $mctal\n");

  $_ = <MCTAL>;     # line 1 - info
  $_ = <MCTAL>;     # line 2 - title
    chomp;
    $title = $_;

  $_ = <MCTAL>;     # line 3 - ntal, npert?
    m/^\s*ntal\s+(\d+)/;
    $ntal = $1;
 
  while( $_ = <MCTAL> ) {

    if( /^\s*tally\s+(\d+)/ ) {
      $num = $1;
    }
    elsif( /^\s*vals\s+/ ) {
      $_ = <MCTAL>;
        m/^\s*([\d.E+-]+)\s+([\d.E+-]+)/;
        $ave = $1;
        $err = $2;

        $mcnp_ave{ "f$num" } = $ave;
        $mcnp_err{ "f$num" } = $err;
    }
  }
  close(MCTAL);
}


foreach $case (sort(keys(%cases))) {

  $tal = $cases{$case}{detector_set}{A}[0];
  if( ! $mcnp_ave{$tal} ) { next; }


  print   OUT  "\n$cases{$case}{title}\n\n";

  printf  OUT  "\t\t\t x, y, z\tReference\tRel-Err\t\tMCNP-result\tRel-err \t  C/E\n";

  foreach $det (sort(keys(%{$cases{$case}{detector_set}}))) {

    print  OUT  "\tDetector Set $det\n";

    foreach $tal ( @{$cases{$case}{detector_set}{$det}} ) {

      $x = $bench{$tal}{xyz}[0];
      $y = $bench{$tal}{xyz}[1];
      $z = $bench{$tal}{xyz}[2];

      $r = $bench{$tal}{flux}[0];
      $e = $bench{$tal}{flux}[1];

      $m = $mcnp_ave{$tal};
      $f = $mcnp_err{$tal};

      $ce = $m / $r;

      printf  OUT  "\t\t%5s\t%2d,%2d,%2d\t%-12.5e\t%6.4f\t\t%-12.5e\t%6.4f\t\t%6.2f\n",
                 $tal,$x,$y,$z,$r,$e,$m,$f,$ce;
    }
  }
}
if( -s $OUT ) {
  print "\n...results saved in file= $OUT\n\n";
  close(OUT);
}
exit;



sub bench_results {
  #
  # from kobayashi report, 2000.
  #
%cases = ( 
	 prob1_abs  => { 
		title => "problem 1 - 3d, voids+absorbers",
		detector_set => {
		A => [	f1105, f1115, f1125, f1135, f1145,
			f1155, f1165, f1175, f1185, f1195 ],
		B => [	f1205, f1215, f1225, f1235, f1245,
			f1255, f1265, f1275, f1285, f1295 ],
		C => [	f1305, f1315, f1325, f1335, f1345,
			f1355, f1365, f1375, f1385, f1395 ] } },
	 prob1_sct  => { 
		title => "problem 1 - 3d, voids+abs+scat",
		detector_set => {
		A => [	f1405, f1415, f1425, f1435, f1445,
			f1455, f1465, f1475, f1485, f1495 ],
		B => [	f1505, f1515, f1525, f1535, f1545,
			f1555, f1565, f1575, f1585, f1595 ],
		C => [	f1605, f1615, f1625, f1635, f1645,
			f1655, f1665, f1675, f1685, f1695 ] } },
	 prob2_abs  => { 
		title => "problem 2 - 3d, voids+absorbers",
		detector_set => {
		A => [	f2105, f2115, f2125, f2135, f2145,
			f2155, f2165, f2175, f2185, f2195 ],
		B => [	f2205, f2215, f2225, f2235, f2245, f2255 ] } },
	 prob2_sct  => { 
		title => "problem 2 - 3d, voids+abs+scat",
		detector_set => {
		A => [	f2305, f2315, f2325, f2335, f2345,
			f2355, f2365, f2375, f2385, f2395 ],
		B => [	f2405, f2415, f2425, f2435, f2445, f2455 ] } },
	 prob3_abs  => { 
		title => "problem 3 - 3d, voids+absorbers",
		detector_set => {
		A => [	f3105, f3115, f3125, f3135, f3145,
			f3155, f3165, f3175, f3185, f3195 ],
		B => [	f3205, f3215, f3225, f3235, f3245, f3255 ],
		C => [	f3305, f3315, f3325, f3335, f3345, f3355 ] } },
	 prob3_sct  => { 
		title => "problem 3 - 3d, voids+abs+scat",
		detector_set => {
		A => [	f3405, f3415, f3425, f3435, f3445,
			f3455, f3465, f3475, f3485, f3495 ],
		B => [	f3505, f3515, f3525, f3535, f3545, f3555 ],
		C => [	f3605, f3615, f3625, f3635, f3645, f3655 ] } }
         );
%bench = (
  #  title => "problem1 - void, detector set A :: x,y,z,flux-exact",
  f1105 => {  xyz => [   5,5,5 ], flux => [ 5.95659E+00, 0.0 ]  },
  f1115 => {  xyz => [  5,15,5 ], flux => [ 1.37185E+00, 0.0]  },
  f1125 => {  xyz => [  5,25,5 ], flux => [ 5.00871E-01, 0.0]  },
  f1135 => {  xyz => [  5,35,5 ], flux => [ 2.52429E-01, 0.0]  },
  f1145 => {  xyz => [  5,45,5 ], flux => [ 1.50260E-01, 0.0]  },
  f1155 => {  xyz => [  5,55,5 ], flux => [ 5.95286E-02, 0.0]  },
  f1165 => {  xyz => [  5,65,5 ], flux => [ 1.53283E-02, 0.0 ]  },
  f1175 => {  xyz => [  5,75,5 ], flux => [ 4.17689E-03, 0.0 ]  },
  f1185 => {  xyz => [  5,85,5 ], flux => [ 1.18533E-03, 0.0 ]  },
  f1195 => {  xyz => [  5,95,5 ], flux => [ 3.46846E-04, 0.0 ]  },
  
  #  title => "problem1 - void, Detector set B :: x,y,z,flux-exact" 
  f1205 => {  xyz => [     5,5,5 ], flux => [ 5.95659E+00, 0.0 ]  },
  f1215 => {  xyz => [  15,15,15 ], flux => [ 4.70754E-01, 0.0 ]  },
  f1225 => {  xyz => [  25,25,25 ], flux => [ 1.69968E-01, 0.0 ]  },
  f1235 => {  xyz => [  35,35,35 ], flux => [ 8.68334E-02, 0.0 ]  },
  f1245 => {  xyz => [  45,45,45 ], flux => [ 5.25132E-02, 0.0 ]  },
  f1255 => {  xyz => [  55,55,55 ], flux => [ 1.33378E-02, 0.0 ]  },
  f1265 => {  xyz => [  65,65,65 ], flux => [ 1.45867E-03, 0.0 ]  },
  f1275 => {  xyz => [  75,75,75 ], flux => [ 1.75364E-04, 0.0 ]  },
  f1285 => {  xyz => [  85,85,85 ], flux => [ 2.24607E-05, 0.0 ]  },
  f1295 => {  xyz => [  95,95,95 ], flux => [ 3.01032E-06, 0.0 ]  },
  
  #  title => "problem1 - void, Detector set C :: x,y,z,flux-exact" 
  f1305 => {  xyz => [   5,55,5 ], flux => [ 5.95286E-02, 0.0 ]  },
  f1315 => {  xyz => [  15,55,5 ], flux => [ 5.50247E-02, 0.0 ]  },
  f1325 => {  xyz => [  25,55,5 ], flux => [ 4.80754E-02, 0.0 ]  },
  f1335 => {  xyz => [  35,55,5 ], flux => [ 3.96765E-02, 0.0 ]  },
  f1345 => {  xyz => [  45,55,5 ], flux => [ 3.16366E-02, 0.0 ]  },
  f1355 => {  xyz => [  55,55,5 ], flux => [ 2.35303E-02, 0.0 ]  },
  f1365 => {  xyz => [  65,55,5 ], flux => [ 5.83721E-03, 0.0 ]  },
  f1375 => {  xyz => [  75,55,5 ], flux => [ 1.56731E-03, 0.0 ]  },
  f1385 => {  xyz => [  85,55,5 ], flux => [ 4.53113E-04, 0.0 ]  },
  f1395 => {  xyz => [  95,55,5 ], flux => [ 1.37079E-04, 0.0 ]  },
  
  #  title => "problem2 - void, detector set A :: x,y,z,flux-exact" 
  f2105 => {  xyz => [   5,5,5 ], flux => [ 5.95659E+00, 0.0 ]  },
  f2115 => {  xyz => [  5,15,5 ], flux => [ 1.37185E+00, 0.0 ]  },
  f2125 => {  xyz => [  5,25,5 ], flux => [ 5.00871E-01, 0.0 ]  },
  f2135 => {  xyz => [  5,35,5 ], flux => [ 2.52429E-01, 0.0 ]  },
  f2145 => {  xyz => [  5,45,5 ], flux => [ 1.50260E-01, 0.0 ]  },
  f2155 => {  xyz => [  5,55,5 ], flux => [ 9.91726E-02, 0.0 ]  },
  f2165 => {  xyz => [  5,65,5 ], flux => [ 7.01791E-02, 0.0 ]  },
  f2175 => {  xyz => [  5,75,5 ], flux => [ 5.22062E-02, 0.0 ]  },
  f2185 => {  xyz => [  5,86,5 ], flux => [ 4.03188E-02, 0.0 ]  },
  f2195 => {  xyz => [  5,95,5 ], flux => [ 3.20574E-02, 0.0 ]  },
  
  #  title => "problem2 - void, detector set B :: x,y,z,flux-exact" 
  f2205 => {  xyz => [   5,95,5 ], flux => [ 3.20574E-02, 0.0 ]  },
  f2215 => {  xyz => [  15,95,5 ], flux => [ 1.70541E-03, 0.0 ]  },
  f2225 => {  xyz => [  25,95,5 ], flux => [ 1.40557E-04, 0.0 ]  },
  f2235 => {  xyz => [  35,95,5 ], flux => [ 3.27058E-05, 0.0 ]  },
  f2245 => {  xyz => [  45,95,5 ], flux => [ 1.08505E-05, 0.0 ]  },
  f2255 => {  xyz => [  55,95,5 ], flux => [ 4.14132E-06, 0.0 ]  },
  
  #  title => "problem3 - void, detector set A :: x,y,z,flux-exact",
  f3105 => {  xyz => [   5,5,5 ], flux => [ 5.95659E+00, 0.0 ]  },
  f3115 => {  xyz => [  5,15,5 ], flux => [ 1.37185E+00, 0.0 ]  },
  f3125 => {  xyz => [  5,25,5 ], flux => [ 5.00871E-01, 0.0 ]  },
  f3135 => {  xyz => [  5,35,5 ], flux => [ 2.52429E-01, 0.0 ]  },
  f3145 => {  xyz => [  5,45,5 ], flux => [ 1.50260E-01, 0.0 ]  },
  f3155 => {  xyz => [  5,55,5 ], flux => [ 9.91726E-02, 0.0 ]  },
  f3165 => {  xyz => [  5,65,5 ], flux => [ 4.22623E-02, 0.0 ]  },
  f3175 => {  xyz => [  5,75,5 ], flux => [ 1.14703E-02, 0.0 ]  },
  f3185 => {  xyz => [  5,85,5 ], flux => [ 3.24662E-03, 0.0 ]  },
  f3195 => {  xyz => [  5,95,5 ], flux => [ 9.48324E-04, 0.0 ]  },
  
  #  title => "problem3 - void, detector set B :: x,y,z,flux-exact",
  f3205 => {  xyz => [   5,55,5 ], flux => [ 9.91726E-02, 0.0 ]  },
  f3215 => {  xyz => [  15,55,5 ], flux => [ 2.45041E-02, 0.0 ]  },
  f3225 => {  xyz => [  25,55,5 ], flux => [ 4.54477E-03, 0.0 ]  },
  f3235 => {  xyz => [  35,55,5 ], flux => [ 1.42960E-03, 0.0 ]  },
  f3245 => {  xyz => [  45,55,5 ], flux => [ 2.64846E-04, 0.0 ]  },
  f3255 => {  xyz => [  55,55,5 ], flux => [ 9.14210E-05, 0.0 ]  },
  
  #  title => "problem3 - void, detector set C :: x,y,z,flux-exact",
  f3305 => {  xyz => [   5,95,35 ], flux => [ 3.27058E-05, 0.0 ]  },
  f3315 => {  xyz => [  15,95,35 ], flux => [ 2.68415E-05, 0.0 ]  },
  f3325 => {  xyz => [  25,95,35 ], flux => [ 1.70019E-05, 0.0 ]  },
  f3335 => {  xyz => [  35,95,35 ], flux => [ 3.37981E-05, 0.0 ]  },
  f3345 => {  xyz => [  45,95,35 ], flux => [ 6.04893E-06, 0.0 ]  },
  f3355 => {  xyz => [  55,95,35 ], flux => [ 3.36460E-06, 0.0 ]  },
  
  #  title => "problem1 - void + scatter, detector set A :: x,y,z,flux-mvp,re-mvp",
  f1405 => {  xyz => [    5,5,5 ], flux => [ 8.29260E+00, 0.00021 ]  },
  f1415 => {  xyz => [   5,15,5 ], flux => [ 1.87028E+00, 0.00005 ]  },
  f1425 => {  xyz => [   5,25,5 ], flux => [ 7.13986E-01, 0.00003 ]  },
  f1435 => {  xyz => [   5,35,5 ], flux => [ 3.84685E-01, 0.00004 ]  },
  f1445 => {  xyz => [   5,45,5 ], flux => [ 2.53984E-01, 0.00006 ]  },
  f1455 => {  xyz => [   5,55,5 ], flux => [ 1.37220E-01, 0.00073 ]  },
  f1465 => {  xyz => [   5,65,5 ], flux => [ 4.65913E-02, 0.00117 ]  },
  f1475 => {  xyz => [   5,75,5 ], flux => [ 1.58766E-02, 0.00197 ]  },
  f1485 => {  xyz => [   5,85,5 ], flux => [ 5.47036E-03, 0.00343 ]  },
  f1495 => {  xyz => [   5,95,5 ], flux => [ 1.85082E-03, 0.00619 ]  },
  
  #  title => "problem1 - void + scatter, detector set B :: x,y,z,flux-mvp,re-mvp",
  f1505 => {  xyz => [      5,5,5 ], flux => [  8.29260E+00, 0.00021 ]  },
  f1515 => {  xyz => [   15,15,15 ], flux => [  6.63233E-01, 0.00004 ]  },
  f1525 => {  xyz => [   25,25,25 ], flux => [  2.68828E-01, 0.00003 ]  },
  f1535 => {  xyz => [   35,35,35 ], flux => [  1.56683E-01, 0.00005 ]  },
  f1545 => {  xyz => [   45,45,45 ], flux => [  1.04405E-01, 0.00011 ]  },
  f1555 => {  xyz => [   55,55,55 ], flux => [  3.02145E-02, 0.00061 ]  },
  f1565 => {  xyz => [   65,65,65 ], flux => [  4.06555E-03, 0.00074 ]  },
  f1575 => {  xyz => [   75,75,75 ], flux => [  5.86124E-04, 0.00116 ]  },
  f1585 => {  xyz => [   85,85,85 ], flux => [  8.66059E-05, 0.00198 ]  },
  f1595 => {  xyz => [   95,95,95 ], flux => [  1.12892E-05, 0.00383 ]  },
  
  #  title => "problem1 - void + scatter, detector set C :: x,y,z,flux-mvp,re-mvp",
  f1605 => {  xyz => [    5,55,5 ], flux => [ 1.37220E-01, 0.00073 ]  },
  f1615 => {  xyz => [   15,55,5 ], flux => [ 1.27890E-01, 0.00076 ]  },
  f1625 => {  xyz => [   25,55,5 ], flux => [ 1.13582E-01, 0.00080 ]  },
  f1635 => {  xyz => [   35,55,5 ], flux => [ 9.59578E-02, 0.00088 ]  },
  f1645 => {  xyz => [   45,55,5 ], flux => [ 7.82701E-02, 0.00094 ]  },
  f1655 => {  xyz => [   55,55,5 ], flux => [ 5.67030E-02, 0.00111 ]  },
  f1665 => {  xyz => [   65,55,5 ], flux => [ 1.88631E-02, 0.00189 ]  },
  f1675 => {  xyz => [   75,55,5 ], flux => [ 6.46624E-03, 0.00314 ]  },
  f1685 => {  xyz => [   85,55,5 ], flux => [ 2.28099E-03, 0.00529 ]  },
  f1695 => {  xyz => [   95,55,5 ], flux => [ 7.93924E-04, 0.00890 ]  },
  
  #  title => "problem2 - void + scatter, detector set A :: x,y,z,flux-mvp,re-mvp",
  f2305 => {  xyz => [    5,5,5 ], flux => [ 8.61696E+00, 0.00063 ]  },
  f2315 => {  xyz => [   5,15,5 ], flux => [ 2.16123E+00, 0.00015 ]  },
  f2325 => {  xyz => [   5,25,5 ], flux => [ 8.93437E-01, 0.00011 ]  },
  f2335 => {  xyz => [   5,35,5 ], flux => [ 4.77452E-01, 0.00012 ]  },
  f2345 => {  xyz => [   5,45,5 ], flux => [ 2.88719E-01, 0.00013 ]  },
  f2355 => {  xyz => [   5,55,5 ], flux => [ 1.88959E-01, 0.00014 ]  },
  f2365 => {  xyz => [   5,65,5 ], flux => [ 1.31026E-01, 0.00016 ]  },
  f2375 => {  xyz => [   5,75,5 ], flux => [ 9.49890E-02, 0.00017 ]  },
  f2385 => {  xyz => [   5,85,5 ], flux => [ 7.12403E-02, 0.00019 ]  },
  f2395 => {  xyz => [   5,95,5 ], flux => [ 5.44807E-02, 0.00019 ]  },
  
  #  title => "problem2 - void + scatter, detector set B :: x,y,z,flux-mvp,re-mvp",
  f2405 => {  xyz => [    5,95,5 ], flux => [ 5.44807E-02, 0.00019 ]  },
  f2415 => {  xyz => [   15,95,5 ], flux => [ 6.58233E-03, 0.00244 ]  },
  f2425 => {  xyz => [   25,95,5 ], flux => [ 1.28002E-03, 0.00336 ]  },
  f2435 => {  xyz => [   35,95,5 ], flux => [ 4.13414E-04, 0.00363 ]  },
  f2445 => {  xyz => [   45,95,5 ], flux => [ 1.55548E-04, 0.00454 ]  },
  f2455 => {  xyz => [   55,95,5 ], flux => [ 6.02771E-05, 0.00599 ]  },
  
  #  title => "problem3 - void + scatter, detector set A :: x,y,z,flux-mvp,re-mvp",
  f3405 => {  xyz => [    5,5,5 ], flux => [ 8.61578E+00, 0.00044 ]  },
  f3415 => {  xyz => [   5,15,5 ], flux => [ 2.16130E+00, 0.00010 ]  },
  f3425 => {  xyz => [   5,25,5 ], flux => [ 8.93784E-01, 0.00008 ]  },
  f3435 => {  xyz => [   5,35,5 ], flux => [ 4.78052E-01, 0.00008 ]  },
  f3445 => {  xyz => [   5,45,5 ], flux => [ 2.89424E-01, 0.00009 ]  },
  f3455 => {  xyz => [   5,55,5 ], flux => [ 1.92698E-01, 0.00010 ]  },
  f3465 => {  xyz => [   5,65,5 ], flux => [ 1.04982E-01, 0.00077 ]  },
  f3475 => {  xyz => [   5,75,5 ], flux => [ 3.37544E-02, 0.00107 ]  },
  f3485 => {  xyz => [   5,85,5 ], flux => [ 1.08158E-02, 0.00163 ]  },
  f3495 => {  xyz => [   5,95,5 ], flux => [ 3.39632E-03, 0.00275 ]  },
  
  #  title => "problem3 - void + scatter, detector set B :: x,y,z,flux-mvp,re-mvp",
  f3505 => {  xyz => [    5,55,5 ], flux => [ 1.92698E-01, 0.00010 ]  },
  f3515 => {  xyz => [   15,55,5 ], flux => [ 6.72147E-02, 0.00019 ]  },
  f3525 => {  xyz => [   25,55,5 ], flux => [ 2.21799E-02, 0.00028 ]  },
  f3535 => {  xyz => [   35,55,5 ], flux => [ 9.90646E-03, 0.00033 ]  },
  f3545 => {  xyz => [   45,55,5 ], flux => [ 3.39066E-03, 0.00195 ]  },
  f3555 => {  xyz => [   55,55,5 ], flux => [ 1.05629E-03, 0.00327 ]  },
  
  #  title => "problem3 - void + scatter, detector set C :: x,y,z,flux-mvp,re-mvp",
  f3605 => {  xyz => [   5,95,35 ], flux => [ 3.44804E-04, 0.00793 ]  },
  f3615 => {  xyz => [  15,95,35 ], flux => [ 2.91825E-04, 0.00659 ]  },
  f3625 => {  xyz => [  25,95,35 ], flux => [ 2.05793E-04, 0.00529 ]  },
  f3635 => {  xyz => [  35,95,35 ], flux => [ 2.62086E-04, 0.00075 ]  },
  f3645 => {  xyz => [  45,95,35 ], flux => [ 1.05367E-04, 0.00402 ]  },
  f3655 => {  xyz => [  55,95,35 ], flux => [ 4.44962E-05, 0.00440 ]  }
);

}
  # @tallies = sort(keys(%bench));
  # 
  # foreach $key (@tallies)   {
  #   $x   = $bench{$key}{xyz}[0];
  #   $y   = $bench{$key}->{xyz}[1];
  #   $z   = $bench{$key}->{xyz}[2];
  #   $ave = $bench{$key}->{flux}[0];
  #   $re  = $bench{$key}->{flux}[1];
  #   print " $key:\tx=$x,\ty=$y,\tz=$z\tflux=$ave\tre=$re\n";
  #}


