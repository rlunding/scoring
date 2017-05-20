set term png
set output 'plots/push_04.png'
set ylabel 'Occurrence' rotate by 90
set xlabel 'Seconds [S]'
set title '4 second Push. Peer 4'
set xrange [0:20]
set key right top
plot '04sec/04_sec_push_at_44_diff_distribution_gnuplot.dat' using 1:2 with lines notitle