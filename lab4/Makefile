SHELL := /bin/bash

MAIN=answer_sheet
TEXSRC=$(wildcard *.tex)
BIBSRC=$(wildcard *.bib)
DIR_BUILD=build
OPT= --interaction=nonstopmode

all: $(DIR_BUILD)/$(MAIN).pdf

$(DIR_BUILD)/$(MAIN).pdf: $(TEXSRC) $(BIBSRC)
	latexmk -pdf -pvc -pdflatex="texfot pdflatex $(OPT)" $(MAIN) -auxdir=$(DIR_BUILD) -outdir=$(DIR_BUILD)

clean:
	rm -f $(DIR_BUILD)/*

.PHONY: clean all