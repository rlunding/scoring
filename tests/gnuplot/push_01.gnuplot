set term png
set output 'plots/push_01.png'
set ylabel 'Occurrence [#]' rotate by 90
set xlabel 'Seconds [s]'
set title 'Stress test. Push with 1 second delay'
set xrange [0:15]
set key right top
plot '01sec/01_sec_push_at_44_diff_distribution_gnuplot.dat' using 1:2 with lines notitle