# ========= Config =========
OUTDIR  := build
LATEXMK := latexmk
LATEXMK_OPTS := -pdf -silent -interaction=nonstopmode -outdir=$(OUTDIR)

# LaTeX buscará también en la carpeta padre (..), donde viven los .sty
export TEXINPUTS := .:..:$(TEXINPUTS)

VERSIONES := v1 v2 v3

# ========= Targets =========
.PHONY: all sin con clean distclean $(VERSIONES)

all: $(foreach v,$(VERSIONES),$(OUTDIR)/examen_departamental_$(v)_sin_sol.pdf \
                               $(OUTDIR)/examen_departamental_$(v)_con_sol.pdf)

# Por versión individual: make v1  make v2  make v3
v1: $(OUTDIR)/examen_departamental_v1_sin_sol.pdf $(OUTDIR)/examen_departamental_v1_con_sol.pdf
v2: $(OUTDIR)/examen_departamental_v2_sin_sol.pdf $(OUTDIR)/examen_departamental_v2_con_sol.pdf
v3: $(OUTDIR)/examen_departamental_v3_sin_sol.pdf $(OUTDIR)/examen_departamental_v3_con_sol.pdf

$(OUTDIR):
	mkdir -p $(OUTDIR)

# ---- Regla genérica: driver SIN soluciones ----
$(OUTDIR)/driver_%_sin.tex: examen_departamental_%.tex | $(OUTDIR)
	@printf "%s\n" \
	"\\PassOptionsToPackage{nosolucion}{macros_simple}" \
	"\\providecommand{\\versionEtiqueta}{Sin soluciones}" \
	"\\input{../examen_departamental_$*.tex}" > $@

# ---- Regla genérica: driver CON soluciones ----
$(OUTDIR)/driver_%_con.tex: examen_departamental_%.tex | $(OUTDIR)
	@printf "%s\n" \
	"\\PassOptionsToPackage{solucion}{macros_simple}" \
	"\\providecommand{\\versionEtiqueta}{Con soluciones}" \
	"\\input{../examen_departamental_$*.tex}" > $@

# ---- PDFs SIN soluciones ----
$(OUTDIR)/examen_departamental_%_sin_sol.pdf: $(OUTDIR)/driver_%_sin.tex examen_departamental_%.tex
	$(LATEXMK) $(LATEXMK_OPTS) -jobname=examen_departamental_$*_sin_sol \
	    $(OUTDIR)/driver_$*_sin.tex

# ---- PDFs CON soluciones ----
$(OUTDIR)/examen_departamental_%_con_sol.pdf: $(OUTDIR)/driver_%_con.tex examen_departamental_%.tex
	$(LATEXMK) $(LATEXMK_OPTS) -jobname=examen_departamental_$*_con_sol \
	    $(OUTDIR)/driver_$*_con.tex

clean:
	$(LATEXMK) -C -outdir=$(OUTDIR)
	rm -f $(OUTDIR)/driver_*.tex

distclean: clean
	rm -rf $(OUTDIR)
