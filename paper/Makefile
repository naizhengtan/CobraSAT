SHELL := /bin/bash
WORK := $(shell basename `pwd`)
MAIN = $(WORK).ltx

BASE := $(basename $(MAIN))
SRCEXT := $(patsubst $(BASE).%,%,$(MAIN))
BIBFILES := $(wildcard *.bib)
STYLINK := $(notdir $(wildcard *.sty))
STYFILES := $(sort $(STYLINK) $(wildcard *.sty))
TEXFILES := $(sort $(MAIN) $(wildcard *.tex) $(STYFILES))

LATEX = pdflatex
BIBTEX = bibtex -min-crossrefs=1000
PS2PDF = ps2pdf

all: $(BASE).pdf

%.pdf: %.eps
	perl -ne 'exit 1 unless /\n/' $< \
		|| perl -p -i -e 's/\r/\n/g' $<
	epstopdf --outfile=$@ $<

$(BASE).pdf: %.pdf: %.$(SRCEXT) $(TEXFILES) $(BIBFILES)
	$(eval LTXINPUT := "$(EXTDEF)$(EDITDEF)\input{$<}")
	latexmk -pdf $(MAIN)

%.pdf: %.ltx
	latexmk -pdf $<

clean:
		rm -f $(BASE).ps $(BASE).pdf
		rm -f *.dvi *.aux *.log *.bbl *.blg *.lof *.lot *.toc *.bak *.out .images $(WORK).fdb_latexmk $(WORK).fls
		for i in $(IMAGES); do $(MAKE) -C $$i clean; done
