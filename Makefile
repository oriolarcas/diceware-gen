
.PHONY: esp
esp: lang/esp.txt
	@cd src && python -m diceware ../lang/esp.txt

#%: lang/%.txt
#	@cd src && python -m diceware ../lang/esp.txt

%.txt: %_original.txt %_banned.txt %_symbols.txt
	@cd src && python -m diceware.filter.$(basename $(notdir $@)) $(addprefix ../,$^) > ../$@
