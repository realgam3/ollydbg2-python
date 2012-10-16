#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    import_ida_symbols.py - A script to import the IDA symbols (.map file) in OllyDbg2
#    Copyright (C) 2012 Axel "0vercl0k" Souchet - http://www.twitter.com/0vercl0k
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

def get_name_address_symbols(f):
    """
    Create a list of dictionnaries storing an absolute address and the symbol name:
    [{
        'name' : 'sub_bla',
        'addr' : 1337
    }, ..]

    Here is the how a .MAP file generated by IDA looks like:
    [...]
     Address         Publics by Value

     0001:00000000       sub_401000
     0001:00000010       sub_401010
     0001:0000002A       loc_40102A
     0001:00000040       sub_401040
     0001:00000090       loc_401090
     [...]
     """
    # we need to retrieve the PE sections of the binary, in order to have the base of the different segments
    sections = GetPESections()

    # the state used to parse correctly the .map
    state = None
    symbols = []

    for line in f.readlines():
        line = line.strip()

        # we found the begining of the interesting part of the file
        if line.startswith('Address'):
            state = 'PreMarkerOK'
            continue

        # this is the empty line just after the begining of the intersting part
        if line == '' and state == 'PreMarkerOK':
            state = 'MarkerOK'
            continue
        
        # the end!
        if line == '' and state == 'MarkerOK':
            break
        
        if state == 'MarkerOK':
            # retrieve the full address (segment selector + RVA) and the name of the symbol
            full_addr, name = line.split('       ', 2)

            # extract the segment selector and the RVA
            segment_selector, addr = full_addr.split(':', 2)

            # compute the absolute address (base of the segment (retrieved in the PE sections) + RVA)
            absolute_addr = sections[int(segment_selector) - 1].base + int(addr, 16)

            # feed the symbols list
            symbols.append({
                'name' : name,
                'addr' : absolute_addr
            })

    return symbols

def main():
    mapfile_path = 'D:\\Codes\OllyDBG2-Python\samples\\import_ida_symbols.map'
    with open(mapfile_path, 'r') as f:
        # get a simple list with the absolute address & the name of our symbols
        pair_address_symbol = get_name_address_symbols(f)
        for symbol in pair_address_symbol:
            # yay, add them to ollydbg
            AddUserLabel(symbol['addr'], symbol['name'])

    return 1

if __name__ == '__main__':
    main()