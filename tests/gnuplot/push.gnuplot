set term png
set output 'plots/push.png'
set ylabel 'Occurrence [#]' rotate by 90
set xlabel 'Seconds [s]'
set title 'Push'
set key right top
set xrange [0:5]
plot 'push_test_diff_distribution_gnuplot.dat' using 1:2 with lines notitle