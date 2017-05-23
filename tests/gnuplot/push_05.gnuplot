set term png
set output 'plots/push_05.png'
set ylabel 'Occurrence [#]' rotate by 90
set xlabel 'Seconds [s]'
set title 'Stress test. Push with 0.5 second delay'
set xrange [0:15]
set key right top
plot '05sec/05_sec_push_at_44_diff_distribution_gnuplot.dat' using 1:2 with lines notitle