import os
def gen_doc(header, utfil):
    with open('write.tex', 'w') as texfile:
        texfile.write('\\documentclass[10pt]{report}\n')
        texfile.write('\\usepackage[a4paper, total={7in, 8in}]{geometry}\n')
        texfile.write('\\usepackage{{booktabs}}\n')
        texfile.write('\\usepackage{fancyhdr}\n')
        texfile.write('\\newlength\\mylen\n')
        texfile.write('\\settowidth{\\mylen}{\\bfseries Pagamenti \\ \\}\n')
        texfile.write('\n')
        texfile.write('\\begin{document}\n')
        texfile.write('\\pagestyle{fancy}\n')
        texfile.write('\\fancyhead{} % clear all header fields\n')
        texfile.write('\\fancyhead[RO,LE]{\\textbf{'+header+'}}\n')
        texfile.write('\n')

        a = 0
        for fil in os.listdir('tables'):
            if fil.endswith('.tex'):
                a+=1
        for i in range(a):
            texfile.write('\\bigskip\\noindent\\parbox{\\mylen}{}\n')
            texfile.write('\\input{{tables/a_'+str(i)+'.tex}} \\\\\n')

        texfile.write('\\end{document} ')

    os.system('xelatex --interaction=batchmode write.tex test.pdf')
    os.system(f'cp write.pdf {utfil}')

    os.system('rm tables/*')

#gen_doc('Hall of Fame', 'pdfs/hof.pdf')
#gen_doc('2010-2023', 'pdfs/post2010.pdf')
gen_doc('1980-2023', 'pdfs/alle.pdf')