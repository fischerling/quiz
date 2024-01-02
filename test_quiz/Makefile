QUESTIONS:=$(wildcard *.tex)
PDFS:=$(QUESTIONS:.tex=.pdf)
PNGS:=$(QUESTIONS:.tex=.png)
JPGS:=$(QUESTIONS:.tex=.jpg)

.PHONY: all
all: $(PDFS) $(PNGS) $(JPGS)

.PHONY: clean
clean:
	rm -f $(PDFS) $(PNGS) $(JPGS)

%.pdf: %.tex
	rubber --pdf $< && \
	rubber --clean $<

%.jpg: %.pdf
	convert -density 600 -quality 100 $< -flatten -sharpen 0x1.0 $@

%.png: %.pdf
	convert -density 600 -quality 100 $< -flatten -sharpen 0x1.0 $@
