#! /usr/bin/python

# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""This class implements a BASIC interpreter that
presents a prompt to the user. The user may input
program statements, list them and run the program.
The program may also be saved to disk and loaded
again.

"""

from basictoken import BASICToken as Token
from lexer import Lexer
from program import Program
from sys import stderr


def main():

    banner = (
        """
        PPPP   Y   Y  BBBB    AAA    SSSS    I     CCC
        P   P   Y Y   B   B  A   A  S        I    C
        P   P   Y Y   B   B  A   A  S        I    C
        PPPP     Y    BBBB   AAAAA  SSSS     I    C
        P        Y    B   B  A   A      S    I    C
        P        Y    B   B  A   A      S    I    C
        P        Y    BBBB   A   A  SSSS     I     CCC
        
READY.""")

    print(banner)

    lexer = Lexer()
    program = Program()

    ten = Token(0,Token.UNSIGNEDINT,'10')

    # Continuously accept user input and act on it until
    # the user enters 'EXIT'
    while True:

        stmt = input('')

        try:
            tokenlist = lexer.tokenize(stmt)

            # Execute commands directly, otherwise
            # add program statements to the stored
            # BASIC program

            if len(tokenlist) > 0:

                # Exit the interpreter
                if tokenlist[0].category == Token.EXIT:
                    break

                # Add a new program statement, beginning
                # a line number
                elif tokenlist[0].category == Token.UNSIGNEDINT\
                     and len(tokenlist) > 1:
                    #print(dir(tokenlist[0]))
                    #tokenlist[0].pretty_print()
                    program.add_stmt(tokenlist)

                # Delete a statement from the program
                elif tokenlist[0].category == Token.UNSIGNEDINT \
                        and len(tokenlist) == 1:
                    program.delete_statement(int(tokenlist[0].lexeme))

                # Execute the program
                elif tokenlist[0].category == Token.RUN:
                    try:
                        program.execute()

                    except KeyboardInterrupt:
                        print("Program terminated")
                    print("\nREADY.")

                # List the program
                elif tokenlist[0].category == Token.LIST:
                    if len(tokenlist) == 2:
                         program.list(int(tokenlist[1].lexeme),int(tokenlist[1].lexeme))
                    elif len(tokenlist) == 3:
                        # if we have 3 tokens, it might be LIST x y for a range
                        # or LIST -y or list x- for a start to y, or x to end
                        if tokenlist[1].lexeme == "-":
                            program.list(None, int(tokenlist[2].lexeme))
                        elif tokenlist[2].lexeme == "-":
                            program.list(int(tokenlist[1].lexeme), None)
                        else:
                            program.list(int(tokenlist[1].lexeme),int(tokenlist[2].lexeme))
                    elif len(tokenlist) == 4:
                        # if we have 4, assume LIST x-y or some other
                        # delimiter for a range
                        program.list(int(tokenlist[1].lexeme),int(tokenlist[3].lexeme))
                    else:
                        program.list()
                    print("\nREADY.")

                # Save the program to disk
                elif tokenlist[0].category == Token.SAVE:
                    program.save(tokenlist[1].lexeme)
                    print("Program written to file")
                    print("\nREADY.")

                # Load the program from disk
                elif tokenlist[0].category == Token.LOAD:
                    program.load(tokenlist[1].lexeme)
                    print("Program read from file")
                    print("\nREADY.")

                # Delete the program from memory
                elif tokenlist[0].category == Token.NEW:
                    program.delete()
                    print("\nREADY.")

                #elif len(tokenlist) > 0:
                #    

                # Unrecognised input
                # Execute single statement
                else:
                    tokenlist.insert(0,ten)
                    oneliner = Program()
                    oneliner.add_stmt(tokenlist)
                    try:
                        oneliner.execute()

                    except KeyboardInterrupt:
                        print("Program terminated")
                    #print("Unrecognised input", file=stderr)
                    #for token in tokenlist:
                    #    token.print_lexeme()
                    #print(flush=True)


                #else:
                #    print("Unrecognised input", file=stderr)
                #    for token in tokenlist:
                #        token.print_lexeme()
                #    print(flush=True)

        # Trap all exceptions so that interpreter
        # keeps running
        except Exception as e:
            print(e, file=stderr, flush=True)


if __name__ == "__main__":
    main()
