SHELL := /bin/bash

MAIN=answer_sheet
TEXSRC=$(wildcard *.tex)
DIR_BUILD=build
OPT= --interaction=nonstopmode

all: $(DIR_BUILD)/$(MAIN).pdf

$(DIR_BUILD)/$(MAIN).pdf: $(TEXSRC)
	latexmk -pdf -pvc -pdflatex="pdflatex $(OPT)" $(MAIN) -auxdir=$(DIR_BUILD) -outdir=$(DIR_BUILD)

clean:
	rm -f $(MAIN).{log,aux,bcf,fdb_latexmk,fls,lof,lot,run.xml,synctex.gz,toc,upa,upd,ubp,bbl,blg}

.PHONY: clean all