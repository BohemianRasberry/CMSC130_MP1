'''
Reference: https://github.com/int-main/Quine-McCluskey
Authors:
    Danielle Azarraga
    Stefani Gutierrez
'''

class Quine:
    def __init__(self, min_terms, dont_cares):
        '''
        Initializes the whole class
        Args:
            self: required argument for initializaition
            min_terms: list of minterms
            dont_cares: list of don't cares
        '''
        self.__mt = min_terms
        self.__dc = dont_cares
        self.__md = min_terms + dont_cares

    def toRefine(self, my_list, dc_list): # Shaves of don't cares
        '''
        Refines the list of prime implicants
        Args:
            self: necessary argument for a class
            my_list: list of merged terms
            dc_list: list of don't cares given by the user
        Return:
            result: list of items found in my_list but not in dc_list
        '''
        result = []
        for i in my_list:
            if int(i) not in dc_list:
                result.append(i)
        return result

    def identifyEPI(self, dict): # Non repeating -> check chart
        '''
        Identify all the prime implicants that are non repeating
        Args:
            self: necessary argument for a class
            dict: dictionary of minterms and their corresponding binary terms
        Return:
            result: All non repeating items in x
        '''
        result = []
        for i in dict:
            if len(dict[i]) == 1:
                result.append(dict[i][0]) if dict[i][0] not in result else None
        return result

    def identifyVAR(self, listEPI): # Unicode
        '''
        Prints the function using normal variables
        Args:
            self: necessary argument for a class
            listEPI: terms from the list of essential prime implicants
        Return:
            var_list: list of needed variables for function
        '''
        var_list = []
        for i in range(len(listEPI)):
            if listEPI[i] == '0':
                var_list.append(chr(i + 97) + "'")
            elif listEPI[i] == '1':
                var_list.append(chr(i + 97))
        return var_list

    def identify_newVAR(self, listPI, variables): # Not Unicode
        '''
        Prints the function based on the user's variables
        Args:
            self: necessary argument for a class
            listPI: terms from the list of essential prime implicants
            variables: list of variables given by the user
        Return:
            var_list: list of needed variables for function
        '''
        var_list = []
        for i in range(len(listPI)):
            if listPI[i] == '0':
                var_list.append(variables[i] + "'")
            elif listPI[i] == '1':
                var_list.append(variables[i])
        return var_list


    def toFlatten(self, dict): # For unmarked_list
        '''
        Puts contents of dictionary temp in a list
        Args:
            self: necessary argument for a class
            dict: dictionary of minterms
        Return:
             flattened_items: list of contents of dictionary x
        '''
        flattened_items = []
        for i in dict:
            flattened_items.extend(dict[i])
        return flattened_items

    def findMinterms(self, elementsPI): # ex. [1, 2]
        '''
        Finds the minterms with that should be grouped together
        Args:
            self: necessary argument for a class
            elementsPI: elements of set all_pi
        Return:
            List of grouped minterms
        '''
        gaps = elementsPI.count('-')
        if gaps == 0:
            return [str(int(elementsPI, 2))]
        x = [bin(i)[2:].zfill(gaps) for i in range(pow(2, gaps))]
        temp = []
        for i in range(pow(2, gaps)):
            temp2, index = elementsPI[:], -1
            for j in x[0]:
                if index != -1:
                    index = index + temp2[index + 1:].find('-') + 1
                else:
                    index = temp2[index + 1:].find('-')
                temp2 = temp2[:index] + j + temp2[index + 1:]
            temp.append(str(int(temp2, 2)))
            x.pop(0)
        return temp

    def toCompare(self, grpA, grpB): # Per character comparison
        '''
        Compares if the binary terms differ by one bit
        Args:
            self: necessary argument for a class
            grpA: minterm in binary from the first group
            grpB: minterm in binary from the next group (to be compared to)
        Return:
            Boolean: True or False
            mismatch_index: the index of where the two minterms have differed
        '''
        mismatch_index = 0
        c = 0
        for i in range(len(grpA)):
            if grpA[i] != grpB[i]:
                mismatch_index = i
                c += 1
                if c > 1:
                    return False, None
        return True, mismatch_index

    def deleteTerms(self, _chart, termsBinary): # deletes based on keys
        '''
        Deletes elements from the chart that are essential prime implicants
        Args:
            self: necessary argument for a class
            _chart: dictionary of prime implicants
            termsBinary: list of essential prime implicants in binary
        '''
        for i in termsBinary:
            for j in self.findMinterms(i):
                try:
                    del _chart[j]
                except KeyError:
                    pass

    def primaryGRP(self, md, size): # dictionary
        '''
        Creates a dictionary for minters + don't cares
        Args:
            self: necessary argument for a class
            md: list of minterms and don't cares
            size: size of largest binary
        '''
        groups = {}
        for minterm in md:
            try:
                groups[bin(minterm).count('1')].append(
                    bin(minterm)[2:].zfill(size))
            except KeyError:
                groups[bin(minterm).count('1')] = [
                    bin(minterm)[2:].zfill(size)]
        return groups

    def toPrint(self, groups): # Prints table dictionary
        '''
        Prints group to a chart
        Args:
            self: necessary argument for a class
            groups: dictionary of minterms + don't cares
        '''
        print("\n\n\n\nGROUP #\t\tMINTERMS\t\tBINARY\n%s" %
            ('=' * 50))
        for i in sorted(groups.keys()):
            print("%5d:" % i)  # Prints group number
            for j in groups[i]:
                # Prints minterms and its binary representation
                print("\t\t\t\t%-15s%s" %
                      (','.join(self.findMinterms(j)), j))
            print('-' * 50)

    def toReplace(self, temp, groups, m, marked, should_stop): # yeah alam mo na yan lolololol
        '''
        Replaces the similar numbers with "-"
        Args:
            self: necessary argument for a class
            temp: dictionary of minterms + don't cares
            groups: empty dictionary
            m: index to be used for dictionary
            marked: set of
            should_stop: boolean of whether should stop
        Return:
            groups: dictionary containing processed minterms
            m: index to be used for dictionary
            marked: set
            should_stop: boolean of whether should stop
        '''
        lists = sorted(list(temp.keys())) # List of ordered keys of the temp dictionary
        for i in range(len(lists) - 1):
            for j in temp[lists[i]]:  # Loop which iterates through current group elements
                for k in temp[lists[i + 1]]:  # Loop which iterates through next group elements
                    res = self.toCompare(j, k)  # Compare the minterms [Boolean, index]
                    if res[0]:  # If the minterms differ by 1 bit only
                        try:
                            # Put a '-' in the changing bit and add it to corresponding group
                            groups[m].append(j[:res[1]] + '-' + j[res[1] + 1:]) if j[:res[1]] + '-' + j[res[1] + 1:] not in groups[m] else None
                        except KeyError:
                            # If the group doesn't exist, create the group at first and then put a '-' in the changing bit and add it to the newly created group
                            groups[m] = [j[:res[1]] + '-' + j[res[1] + 1:]]
                        should_stop = False
                        marked.add(j)  # Mark element j
                        marked.add(k)  # Mark element k
            m += 1

        return groups, m, marked, should_stop

    def getVariables(self, varLen): # user variable
        '''
        Gets variables of user's choice
        Args:
            self: necessary argument for a class
            varLen: size of largest binary number
        Return:
            variables: list of variables
        '''
        variables = []
        print('Enter the variables you want to use: (Press enter for every new variable)')
        for i in range(varLen):
            print('Variable ' + str(i + 1) + ': ')
            temp = input().lower()
            variables.append(temp)
        return variables

    def main(self): # ano kaya to ʕ•́ᴥ•̀ʔっ
        '''
        Starting point of the whole program
        '''
        self.__mt.sort() # Sorts the list of minters
        self.__md.sort() # Sorts the list of minters + don't cares
        size = len(bin(self.__md[-1])) - 2 # Length of the largest binary
        all_pi = set()

        # Primary grouping starts
        groups = self.primaryGRP(self.__md, size) # Creates a dictionary for md
        # Primary grouping ends

        # Primary group printing starts
        self.toPrint(groups)
        # Primary group printing ends

        # Process for creating tables and finding prime implicants starts
        while True:
            temp = groups.copy()
            groups, m, marked, should_stop = {}, 0, set(), True
            groups, m, marked, should_stop = self.toReplace(
                temp, groups, m, marked, should_stop)

            local_unmarked = set(self.toFlatten(temp)).difference(
                marked)  # Unmarked elements of each table
            all_pi = all_pi.union(local_unmarked) # Adding Prime Implicants to global list
            print("\nPrime Implicants without marks:", None if len(local_unmarked) == 0 else ', '.join(local_unmarked))  # Printing Prime Implicants of current table
            if should_stop:  # If the minterms cannot be combined further
                print("\n\nAll Prime Implicants: ", None if len(all_pi) == 0 else ', '.join(all_pi))  # Print all prime implicants
                break
            # Printing of all the next groups starts
            self.toPrint(groups)
            # Printing of all the next groups ends
        # Process for creating tables and finding prime implicants ends

        # Printing and processing of Prime Implicant chart starts
        size = len(str(min_terms[-1]))  # The number of digits of the largest minterm
        chart = {}
        print('\n\n\nPRIME IMPLICANT TABLE\n\n    MINTERMS    |%s\n%s' % (
            ' '.join((' ' * (size - len(str(i)))) + str(i) for i in min_terms), '=' * (len(min_terms) * (size + 1) + 16)))
        for i in all_pi:
            merged_terms, y = self.findMinterms(i), 0
            print("%-16s|" % ','.join(merged_terms), end='')
            for j in self.toRefine(merged_terms, self.__dc):
                # The position where we should put 'X'
                x = min_terms.index(int(j)) * (size + 1)
                print(' ' * abs(x - y) + ' ' * (size - 1) + 'X', end='')
                y = x + size
                try:
                    # Add minterm in chart
                    chart[j].append(i) if i not in chart[j] else None
                except KeyError:
                    chart[j] = [i]
            print('\n' + '-' * (len(min_terms) * (size + 1) + 16))
        # Printing and processing of Prime Implicant chart ends

        EPI = self.identifyEPI(chart)  # Finding essential prime implicants
        print("\nEssential Prime Implicants: " +
              ', '.join(str(i) for i in EPI))
        # Remove EPI related columns from chart
        self.deleteTerms(chart, EPI)


        choice = input('\n\n\nDo you want to use your own variables?. Type (y/n).\n')
        if choice[0].lower() == 'y':
            varLen = len(EPI[0])
            variables = self.getVariables(varLen) # User gets to choose their own variable
            final_result = [self.identify_newVAR(i, variables) for i in EPI]
            print('\n\nSolution: F = ' + ' + '.join(''.join(i)
                                                    for i in final_result))
        else:
            final_result = [self.identifyVAR(i) for i in EPI]  # Final result with only EPIs
            print('\n\nSolution: F = ' + ' + '.join(''.join(i) for i in final_result))


if __name__ == "__main__":

    print('\n')
    print('\t\tWELCOME TO QUINE-MCCLUSKEY PROGRAM!')
    while True:
        min_terms = [int(i) for i in input("\nEnter the minterms: ").strip().split()]
        dont_cares = [int(i) for i in input("Enter the don't cares: ").strip().split()]

        Quine(min_terms, dont_cares).main()
        check = input("Do you want to quit? (Y/N) ")
        print(check)
        if check[0].lower() == 'y':
            break

    input("\nPress enter to exit...")