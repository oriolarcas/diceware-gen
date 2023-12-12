'''
Copyright (C) 2019 Oriol Arcas

This file is part of DicewareGen.

DicewareGen is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

DicewareGen is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with DicewareGen.  If not, see <https://www.gnu.org/licenses/>.
'''

import re

from diceware.generator import DicewareGenerator

class SpanishGenerator(DicewareGenerator):
    def __init__(self):
        super().__init__(
            phrase_size=4,
            words_file=self._replace_file_in_path(__file__, "words.txt"),
            symbols=self._read_json(self._replace_file_in_path(__file__, "symbols.json")),
            banned_path=self._replace_file_in_path(__file__, "banned.txt")
        )

    def read_words(self):
        spaces = re.compile(r'\s+')
        with open(self.words_file, "r", encoding="iso-8859-15") as f:
            for l in f.readlines():
                spl = spaces.split(l.strip())
                if len(spl) != 4:
                    continue
                yield spl[1]

if __name__ == '__main__':
    SpanishGenerator().gen_diceware_list()
