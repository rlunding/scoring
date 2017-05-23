set term png
set output 'plots/push_04.png'
set ylabel 'Occurrence [#]' rotate by 90
set xlabel 'Seconds [s]'
set title 'Stress test. Push with 0.4 second delay'
set xrange [0:20]
set key right top
plot '04sec/04_sec_push_at_44_diff_distribution_gnuplot.dat' using 1:2 with lines notitle