MAKELEVEL =system('echo $MAKELEVEL')
command_tex="\
cat _TMP_.tex | sed 's/\\\\documentclass\\[10pt\\]{article}/\\\\documentclass\[10pt,a4paper,dvipdfmx\]{jarticle}/g' \
              | sed 's/\\\\usepackage.*{preview}//g' \
              | sed 's/\\\\PreviewEnvironment.*//g' \
              | sed 's/\\\\setlength.*//g' \
              | sed 's/\\\\begin{document}/\\\\usepackage{amsfonts,amssymb}\\\\usepackage{bm}\\\\usepackage{txfonts}\\\\usepackage{braket}\\\\begin{document}/g' > _TMP__.tex &&\
( platex -halt-on-error -kanji=utf8 -kanji-internal=utf8 _TMP__.tex > /dev/null ||\
  platex -halt-on-error -kanji=utf8 -kanji-internal=utf8 _TMP__.tex ) &&\
( dvipdfmx -f yugoth.map -d 5 -z 9 -V 5 _TMP__.dvi -q ||\
  dvipdfmx -f yugoth.map -d 5 -z 9 -V 5 _TMP__.dvi ) &&\
( pdfcrop _TMP__.pdf _TMP_.pdf > /dev/null ||\
  pdfcrop _TMP__.pdf _TMP_.pdf ) ;\
rm -f _TMP_.tex _TMP__.tex _TMP__.dvi _TMP__.pdf _TMP__.aux _TMP__.log missfont.log"

###############################################################################
#set terminal tikz latex standalone color dashlength 0.5 size 10,5.5
set terminal tikz latex standalone color dashlength 0.5 size 9,5

###############################################################################
set colors default
#set colors classic
#set colors podo

###############################################################################
unset mouse
set grid
set obj 9999 rect from graph 0, graph 0 to graph 1, graph 1 fc rgb "#f0f0f0" behind

###############################################################################
set key outside #inside
set key right #center #right #left
set key top #bottom
set key above
set key Left #Right
set key horizontal
set key reverse #noreverse
set key noinvert #invert #
set key samplen 2
set key spacing 1
set key width +1
set key height 0
#set key box lw 0
set key opaque
set key maxcols auto
set key maxrows auto

###############################################################################
set terminal tikz latex standalone color dashlength 0.5 size 9,5

filename="result.pdf"
set output "_TMP_.tex"

########
set title 'Number of shots = 4096,\ \ \ $\sum_{\psi} p(\psi) = 1$'
set xlabel 'Measured qubits, $\ket{\psi} = \ket{\mathrm{c_{Alice} c_{Bob} c_1 c_0}}$'
set ylabel 'Measured probabilities, $p(\psi)$'
# set ytics 20
set mytics 2
set xtics scale 0
set boxwidth 0.5 relative
set style fill solid border lc "black"

########
p \
[][0:0.14] \
"result.ssv" u 0:2:xtic(1) lc "purple" w boxes t "", \

########
set output
system( sprintf("rm -f %s", filename) )
system( command_tex ); if( system("if [ ! -f _TMP_.pdf ]; then echo 1; fi") ){ exit error "gnuplot stopped with error." }
system( sprintf("mv _TMP_.pdf %s", filename) ); print( sprintf("%s is generated.", filename) )
#if(MAKELEVEL eq ""){ system( sprintf("okular %s &", filename) ) }
