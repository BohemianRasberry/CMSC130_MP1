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

    def __mul(self, x, y):
        '''
        Multiply 2 minterms
        Args:
            self: necessary argument for a class
            x: element
        Return: list of multiplied expressions
        '''
        result = []
        for i in x:
            if i + "'" in y or (len(i) == 2 and i[0] in y):
                return []
            else:
                result.append(i)
        for i in y:
            if i not in result:
                result.append(i)
        return result

    def __multiply(self, x, y):
        '''
        Multiply 2 expressions
        Args:
            self: necessary argument for a class
            x: first expression
            y: second expression
        Return:
            result: list of multiplied expressions
        '''
        result = []
        for i in x:
            for j in y:
                temp = self.__mul(i, j)
                result.append(temp) if len(temp) != 0 else None
        return result

    def __refine(self, my_list, dc_list):
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

    def __findEPI(self, x):
        '''
        Finds the prime implicants that are non repeating
        Args:
            self: necessary argument for a class
            x: dictionary of minterms and their corresponding binary terms
        Return:
            result: All non repeating items in x
        '''
        result = []
        for i in x:
            if len(x[i]) == 1:
                result.append(x[i][0]) if x[i][0] not in result else None
        return result

    def __find_variables(self, x):
        '''
        Prints the function using normal variables
        Args:
            self: necessary argument for a class
            x: terms from the list of essential prime implicants
        Return:
            var_list: list of needed variables for function
        '''
        var_list = []
        for i in range(len(x)):
            if x[i] == '0':
                var_list.append(chr(i + 65) + "'")
            elif x[i] == '1':
                var_list.append(chr(i + 65))
        return var_list

    def __find_new_variables(self, x, variables):
        '''
        Prints the function based on the user's variables
        Args:
            self: necessary argument for a class
            x: terms from the list of essential prime implicants
            variables: list of variables given by the user
        Return:
            var_list: list of needed variables for function
        '''
        var_list = []
        for i in range(len(x)):
            if x[i] == '0':
                var_list.append(variables[i] + "'")
            elif x[i] == '1':
                var_list.append(variables[i])
        return var_list


    def __flatten(self, x):
        '''
        Puts contents of dictionary temp in a list
        Args:
            self: necessary argument for a class
            x: dictionary of minterms
        Return:
             flattened_items: list of contents of dictionary x
        '''
        flattened_items = []
        for i in x:
            flattened_items.extend(x[i])
        return flattened_items

    def __find_terms(self, a):
        '''
        Finds the minterms with that should be grouped together
        Args:
            self: necessary argument for a class
            a: elements of set all_pi
        Return:
            List of grouped minterms
        '''
        gaps = a.count('-')
        if gaps == 0:
            return [str(int(a, 2))]
        x = [bin(i)[2:].zfill(gaps) for i in range(pow(2, gaps))]
        temp = []
        for i in range(pow(2, gaps)):
            temp2, index = a[:], -1
            for j in x[0]:
                if index != -1:
                    index = index + temp2[index + 1:].find('-') + 1
                else:
                    index = temp2[index + 1:].find('-')
                temp2 = temp2[:index] + j + temp2[index + 1:]
            temp.append(str(int(temp2, 2)))
            x.pop(0)
        return temp

    def __compare(self, a, b):
        '''
        Compares the if the binary terms differ by one bit
        Args:
            self: necessary argument for a class
            a: minterm in binary from the first group
            b: minterm in binary from the next group (to be compared to)
        Return:
            Boolean: True or False
            mismatch_index: the index of where the two minterms have differed
        '''
        mismatch_index = 0
        c = 0
        for i in range(len(a)):
            if a[i] != b[i]:
                mismatch_index = i
                c += 1
                if c > 1:
                    return False, None
        return True, mismatch_index

    def __remove_terms(self, _chart, terms):
        '''
        Deletes elements from the chart that are essential prime implicants
        Args:
            self: necessary argument for a class
            _chart: dictionary of prime implicants
            terms: list of essential prime implicants in binary

        '''
        for i in terms:
            for j in self.__find_terms(i):
                try:
                    del _chart[j]
                except KeyError:
                    pass

    def __group_primary(self, md, size):
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

    def __print_group(self, groups):
        '''
        Prints group to a chart
        Args:
            self: necessary argument for a class
            groups: dictionary of minterms + don't cares
        '''
        print("\n\n\n\nGroup No.\tMinterms\tBinary of Minterms\n%s" %
            ('=' * 50))
        for i in sorted(groups.keys()):
            print("%5d:" % i)  # Prints group number
            for j in groups[i]:
                # Prints minterms and its binary representation
                print("\t\t\t\t%-15s%s" %
                      (','.join(self.__find_terms(j)), j))
            print('-' * 50)

    def __replace(self, temp, groups, m, marked, should_stop):
        '''
        Replaces the similar numbers with "-"
        Args:
            self: necessary argument for a class
            temp: dictionary of minterms + don't cares
            groups: empty dictionary
            m: index to be used for dictionary
            marked: set
            should_stop: boolean of whether should stop
        Return:
            groups: dictionary containing processed minterms
            m: index to be used for dictionary
            marked: set
            should_stop: boolean of whether should stop

        '''
        l = sorted(list(temp.keys())) # List of ordered keys of the temp dictionary
        for i in range(len(l) - 1):
            for j in temp[l[i]]:  # Loop which iterates through current group elements
                for k in temp[l[i + 1]]:  # Loop which iterates through next group elements
                    res = self.__compare(j, k)  # Compare the minterms [Boolean, index]
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

    def __getVariables(self, varLen):
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
            temp = input().upper()
            variables.append(temp)
        return variables

    def main(self):
        '''
        Starting point of the whole program
        '''
        self.__mt.sort() # Sorts the list of minters
        self.__md.sort() # Sorts the list of minters + don't cares
        size = len(bin(self.__md[-1])) - 2 # Length of the largest binary
        all_pi = set()

        # Primary grouping starts
        groups = self.__group_primary(self.__md, size) # Creates a dictionary for md
        # Primary grouping ends

        # Primary group printing starts
        self.__print_group(groups)
        # Primary group printing ends

        # Process for creating tables and finding prime implicants starts
        while True:
            temp = groups.copy()
            groups, m, marked, should_stop = {}, 0, set(), True
            groups, m, marked, should_stop = self.__replace(
                temp, groups, m, marked, should_stop)

            local_unmarked = set(self.__flatten(temp)).difference(
                marked)  # Unmarked elements of each table
            all_pi = all_pi.union(local_unmarked) # Adding Prime Implicants to global list
            print("\nPrime Implicants without marks:", None if len(local_unmarked) == 0 else ', '.join(local_unmarked))  # Printing Prime Implicants of current table
            if should_stop:  # If the minterms cannot be combined further
                print("\n\nAll Prime Implicants: ", None if len(all_pi) == 0 else ', '.join(all_pi))  # Print all prime implicants
                break
            # Printing of all the next groups starts
            self.__print_group(groups)
            # Printing of all the next groups ends
        # Process for creating tables and finding prime implicants ends

        # Printing and processing of Prime Implicant chart starts
        size = len(str(min_terms[-1]))  # The number of digits of the largest minterm
        chart = {}
        print('\n\n\nPrime Implicants chart:\n\n    Minterms    |%s\n%s' % (
            ' '.join((' ' * (size - len(str(i)))) + str(i) for i in min_terms), '=' * (len(min_terms) * (size + 1) + 16)))
        for i in all_pi:
            merged_terms, y = self.__find_terms(i), 0
            print("%-16s|" % ','.join(merged_terms), end='')
            for j in self.__refine(merged_terms, self.__dc):
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

        EPI = self.__findEPI(chart)  # Finding essential prime implicants
        print("\nEssential Prime Implicants: " +
              ', '.join(str(i) for i in EPI))
        # Remove EPI related columns from chart
        self.__remove_terms(chart, EPI)


        choice = input('\n\n\nDo you want to use your own variables?\n')
        if choice[0].lower() == 'y':
            varLen = len(EPI[0])
            variables = self.__getVariables(varLen) # User gets to choose their own variable
            if len(chart) == 0:
                final_result = [self.__find_new_variables(i, variables) for i in EPI]
            else:  # Else follow Petrick's method for further simplification
                P = [[self.__find_new_variables(j, variables) for j in chart[i]] for i in chart]
                while len(P) > 1:  # Keep multiplying until we get the SOP form of P
                    P[1] = self.__multiply(P[0], P[1])
                    P.pop(0)
                # Choosing the term with minimum variables from P
                final_result = [min(P[0], key=len)]
                final_result.extend(self.__find_new_variables(i,variables)
                                    for i in EPI)  # Adding the EPIs to final solution
            print('\n\nSolution: F = ' + ' + '.join(''.join(i)
                                                    for i in final_result))
        else:
            if len(chart) == 0:  # If no minterms remain after removing EPI related columns
                final_result = [self.__find_variables(i)
                                for i in EPI]  # Final result with only EPIs
            else:  # Else follow Petrick's method for further simplification
                P = [[self.__find_variables(j) for j in chart[i]] for i in chart]
                while len(P) > 1:  # Keep multiplying until we get the SOP form of P
                    P[1] = self.__multiply(P[0], P[1])
                    P.pop(0)
                # Choosing the term with minimum variables from P
                final_result = [min(P[0], key=len)]
                final_result.extend(self.__find_variables(i)
                                    for i in EPI)  # Adding the EPIs to final solution
            print('\n\nSolution: F = ' + ' + '.join(''.join(i)
                                                    for i in final_result))


if __name__ == "__main__":
    while True:
        min_terms = [int(i) for i in input("Enter the minterms: ").strip().split()]
        dont_cares = []
        # dont_cares = [int(i) for i in input("Enter the don't cares: ").strip().split()]

        Quine(min_terms, dont_cares).main()
        check = input("Do you want to quit? (Y/N) ")
        print(check)
        if check[0].lower() == 'y':
            break

    input("\nPress enter to exit...")