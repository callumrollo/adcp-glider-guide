SOURCE_DOCS := $(wildcard *.md)

EXPORTED_DOCS=\
 $(SOURCE_DOCS:.md=.pdf) \
 $(SOURCE_DOCS:.md=.html)

RM=/bin/rm

PANDOC=/usr/bin/pandoc


%.pdf : %.md
	$(PANDOC) -o $@ $<
	
%.html : %.md
	$(PANDOC) -o $@ $<

.PHONY: all clean

all : $(EXPORTED_DOCS)

clean:
	- $(RM) $(EXPORTED_DOCS)
