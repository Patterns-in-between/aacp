all: aacp.pdf aacp.html

clean:
	rm aacp.pdf aacp.html

aacp.html: aacp.md references.bib
	pandoc --template=pandoc/iclc.html --citeproc --number-sections aacp.md -o aacp.html

aacp.pdf: aacp.md references.bib pandoc/iclc.latex pandoc/iclc.sty
	pandoc --template=pandoc/iclc.latex --citeproc --number-sections aacp.md -o aacp.pdf

aacp.docx: aacp.md references.bib
	pandoc --citeproc --number-sections aacp.md -o aacp.docx

aacpx.pdf: aacp.md references.bib pandoc/iclc.latex pandoc/iclc.sty
	pandoc --template=pandoc/iclc.latex --citeproc --number-sections aacp.md --latex-engine=xelatex -o aacpx.pdf
