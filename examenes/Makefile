# ========= Config =========
TEXMAIN := examen_2_v1.tex
OUTDIR  := build
PDF_SIN := examen_sin_sol
PDF_CON := examen_con_sol

LATEXMK := latexmk
LATEXMK_OPTS := -pdf -silent -interaction=nonstopmode -outdir=$(OUTDIR)

# LaTeX buscará también en la carpeta padre (..), donde vive macros.sty
export TEXINPUTS := .:..:$(TEXINPUTS)

# ========= Rules =========
.PHONY: all sin con clean distclean

all: sin con

sin: $(OUTDIR)/$(PDF_SIN).pdf
con: $(OUTDIR)/$(PDF_CON).pdf

$(OUTDIR):
	mkdir -p $(OUTDIR)

# ... (lo demás igual que ya tienes) ...

# Driver SIN soluciones
$(OUTDIR)/driver_sin.tex: $(TEXMAIN) | $(OUTDIR)
	@printf "%s\n" \
	"\\PassOptionsToPackage{nosolucion}{macros_simple}" \
	"\\providecommand{\\versionEtiqueta}{Sin soluciones}" \
	"\\input{../$(TEXMAIN)}" > $(OUTDIR)/driver_sin.tex

# Driver CON soluciones
$(OUTDIR)/driver_con.tex: $(TEXMAIN) | $(OUTDIR)
	@printf "%s\n" \
	"\\PassOptionsToPackage{solucion}{macros_simple}" \
	"\\providecommand{\\versionEtiqueta}{Con soluciones}" \
	"\\input{../$(TEXMAIN)}" > $(OUTDIR)/driver_con.tex

$(OUTDIR)/$(PDF_SIN).pdf: $(OUTDIR)/driver_sin.tex $(TEXMAIN)
	$(LATEXMK) $(LATEXMK_OPTS) -jobname=$(PDF_SIN) $(OUTDIR)/driver_sin.tex

$(OUTDIR)/$(PDF_CON).pdf: $(OUTDIR)/driver_con.tex $(TEXMAIN)
	$(LATEXMK) $(LATEXMK_OPTS) -jobname=$(PDF_CON) $(OUTDIR)/driver_con.tex

clean:
	$(LATEXMK) -C -outdir=$(OUTDIR)
	rm -f $(OUTDIR)/driver_*.tex   # <-- importante

distclean: clean
	rm -rf $(OUTDIR)