set term png
set output 'plots/push.png'
set ylabel 'Occurrence' rotate by 90
set xlabel 'Seconds [S]'
set title 'Push'
set key right top
set xrange [0:30]
plot 'push_test_diff_distribution_gnuplot.dat' using 1:2 with lines notitle