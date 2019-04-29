# Add new languages to this list:

LANGS = esp

# New languages should have three files in the lang/ directory:
# - lang/xxx_original.txt: the list of words, by frequency
# - lang/xxx_banned.txt: a list of words to exclude from the diceware
#   (articles, prepositions, proper names...)
# - lang/xxx_symbols.txt: a list of non ASCII characters to replace
#
# And one Python module in the diceware.filter package.
#
# See the example lang/esp_*.txt and src/diceware/filter/esp.py files.

# ---
# Do not modify from here
# ---

LANG_FILES = $(addprefix lang/,$(addsuffix .txt,$(LANGS)))

.SECONDARY: $(LANG_FILES)

.PHONY: all
all: esp

%: lang/%.txt
	@cd src && python -m diceware ../$<

lang/%.txt:
	cd src && python -m diceware.filter.$(basename $(notdir $@)) \
		../$(@:%.txt=%_original.txt) \
		../$(@:%.txt=%_banned.txt) \
		../$(@:%.txt=%_symbols.txt) > ../$@

clean:
	@rm -f $(LANG_FILES)
