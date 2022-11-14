def printingAlternate(mainList, variables):
    '''

    Args:
        mainList: list to be printed
        variables: list of variables to be used for printing
    '''
    temp = ''

    for string in mainList:
        count = -1
        for i in string:
            count += 1
            if i == '0':
                temp += variables[0][count]
                temp += "'"
            elif i == "1":
                temp += variables[0][count]
        temp += " + "
    tempLen = len(temp)
    print(temp[:tempLen - 3])
    print("\b\b\b \n")

def printing(mainList, char):
    '''Prints a boolean function with variables as a,b,c..

    Args:
        mainList: A list of lists. Each list should be a string of the form '1's and '0's representing a term of the funtion.
        char: It is the character with which two terms are seperated. e.g- '+' or ','
    '''

    for string in mainList:
        count = -1
        for i in string:
            count += 1
            if i == '0':
                print(chr(ord('a') + count) + "'", end="")
            elif i == "1":
                print(chr(ord('a') + count), end="")
        print("  " + char + "  ", end="")
    print("\b\b\b \n")

def printGroups(min_terms_dictionary):
    '''

    Args:
        min_terms_dictionary: dictionary of the categorized minterms by count of 1's

    '''
    print('\n\n')
    print('Group No. \t Binary of Minterms \t Minterms' )
    print('='*50)

    for i in min_terms_dictionary:
        if not i:
            continue
        print('\t' + str(i) + ':\n')
        for j in min_terms_dictionary[i]:

            print('\t\t\t\t\t', j[0], '\t\t\t', j[1])
        print('-'*50)

def categorize(min_terms, variables):
    '''
    Categorises minterms on the basis of number of '1's

    Args:
        min_terms: A list of min terms. Each item is a binary number string e.g-"1001".
        variables: The number of variables in the function

    Returns:
        min_terms_categorized: A dictionary with number of '1's as keys and a list of minterms as values with the same number of '1's as the key.
    '''
    min_terms_categorised = {}

    for i in range(variables + 1):
        min_terms_categorised[i] = []

    for i in min_terms:
        min_terms_categorised[i.count("1")].append([i, [int(i, 2)]]) # Creates a dictionary with the number of 1's
        # Ex { 0: 0000, 1: 0001}

    printGroups(min_terms_categorised)

    return min_terms_categorised

def check(element1, element2):
    '''Checks if the two terms differ by only one place.

    Args:
        element1: A list with first element a string of "1"s and "0"s and "-"s
        element2: A list with first element a string of "1"s and "0"s and "-"s

    Returns:
        False - is terms differ by more than 1
        A string of "1"s and "0"s and "-"s otherwise.
    '''
    count = 0
    combined = []
    for i in range(len(element1[0])):
        combined.append(element1[0][i])
        if element2[0][i] != element1[0][i]:
            combined[i] = '-'
            count += 1
    if count > 1:
        return False
    else:
        return ["".join(combined), element1[1] + element2[1]] # Returns prime implicant and their corresponding deciimals


def getPrimeImplicants(terms, number, prime_implicants):
    '''

    Args:
        terms: dictionary of counted 1's per implicant
        number: number of implicants in the term
        prime_implicants: temporary list

    Returns:
        list of prime implicants

    '''
    new_terms = {}
    recursion = 0
    used_terms = []

    for i in range(number):
        new_terms[i] = []
    for i in range(number):
        for element1 in terms[i]:
            flag = 0
            for element2 in terms[i + 1]: # Compares the group of implicants to the next group
                combined = check(element1, element2)
                if combined: # Indicates that there is a combination of minterms
                    recursion = 1
                    flag = 1
                    new_terms[i].append(combined)
                    if element1[0] not in used_terms:
                        used_terms.append(element1[0])
                    if element2[0] not in used_terms:
                        used_terms.append(element2[0])

            if flag == 0: # If element has no combinations, put in prime implicants
                if element1[0] not in used_terms and element1[0] not in [x[0] for x in prime_implicants]:
                    prime_implicants.append(element1)

    for i in terms[number]: # If element with most 1's has no combinations, put in prime implicants
        if i[0] not in used_terms and i[0] not in [x[0] for x in prime_implicants]:
            prime_implicants.append(i)

    if not recursion: # If there are no more combinations
        return
    else:
        getPrimeImplicants(new_terms, number - 1, prime_implicants)


def getEssential(table, essential_implicants):
    '''

    Args:
        table: dictionary of prime implicants
        essential_implicants: list of essential prime implicants


    Returns:
        list of essential prime implicants

    '''

    for i in [x for x in table if len(table[x]) == 1]:
        if table[i][0] not in essential_implicants:
            essential_implicants.append(table[i][0])
        del table[i] # Empties table

def getAllSelected(POS, temp, allSelected, index):
    '''
    Args:
        POS: list of all remaining values in table
        temp: list
        allSelected: list
        index:

    Returns:
        allSelected with the contents of POS

    '''
    if index == len(POS):
        temp1 = temp + []
        allSelected.append(temp1)
        return
    else:
        for i in POS[index]:
            if i not in temp:
                temp.append(i)
                getAllSelected(POS, temp, allSelected, index + 1)
                temp.remove(i)
            else:
                getAllSelected(POS, temp, allSelected, index + 1)


def tabulationMethod(table, selected_implicants):
    '''

    Args:
        table: list of prime implicants
        selected_implicants:


    Returns:

    '''
    temp = []
    POS = []
    allSelected = []

    for i in table:
        POS.append(table[i])

    getAllSelected(POS, temp, allSelected, 0)

    for i in allSelected:
        if len(i) == min([len(x) for x in allSelected]):
            if i not in selected_implicants:
                selected_implicants.append(i)


def getcount(mainList):
    '''

    Args:
        mainList:b


    Returns:

    '''
    count = 0
    for string in [x[0] for x in mainList]:
        for i in string:
            if i == '0' or i == '1':
                count += 1

    return count


def getminimal(selected_implicants): # Test to see if we can remove
    '''

    Args:
        selected_implicants: current list of minimal implicants


    Returns:
        reduces number of implicants in selected_implicants

    '''
    minimal_implicants = []
    minimum = 999999
    for i in selected_implicants:
        if getcount(i) < minimum:
            minimum = getcount(i)

    for i in selected_implicants:
        if getcount(i) == minimum:
            minimal_implicants.append(i)

    return minimal_implicants


def minimalize(prime_implicants, min_terms_categorised):
    '''

    Args:
        prime_implicants: list of prime implicants
        min_terms_categorised: dictionary of elements based on the count of 1's

    Returns:

    '''

    selected_implicants = [] # list
    table = {} # dictionary
    essential_implicants = [] # list of essential prime implicants
    for i, j in min_terms_categorised.items():
        for k in j:
            table[k[1][0]] = []


    for i in prime_implicants:
        for j in i[1]:
            table[j].append(i)

    getEssential(table, essential_implicants) # essential_implicants is full with essential prime implicants

    for i in essential_implicants: # Empties table of essential prime implicants similar to that if inside essential_implicants
        for j in i[1]:
            if j in [x for x in table]:
                del table[j]


    tabulationMethod(table, selected_implicants)
    minimal_implicants = getminimal(selected_implicants)

    return essential_implicants, minimal_implicants

def printImplicants(prime_implicants):
    '''

    Args:
          prime_implicants: list of combined implicants
    '''
    prime_terms_categorised = {}

    for i in range(len(prime_implicants)):
        prime_terms_categorised[i] = []

    index = 0

    for i in prime_implicants:
        temp = 0
        for j in i[0]:
            if j == '1':
                temp += 1
        prime_terms_categorised[temp].append(prime_implicants[index])  # Creates a dictionary with the number of 1's
        index += 1

    printGroups(prime_terms_categorised)

def tabulation(variables, min_terms):
    prime_implicants = []
    functions = [] # List of possible outcomes in binary

    min_terms = [bin(int(x))[2:].zfill(variables) for x in min_terms] # Produces list of minterms in binary
    min_terms_categorised = categorize(min_terms, variables) # Takes a dictionary with the number of 1's

    getPrimeImplicants(min_terms_categorised, variables, prime_implicants) # Return prime_implicants
    printImplicants(prime_implicants)
    essential_implicants, selected_implicants = minimalize(prime_implicants, min_terms_categorised) # Return essential prime implicants

    for i in selected_implicants:
        functions.append(essential_implicants + i)

    printImplicants(essential_implicants)

    prime_implicants = [x[0] for x in prime_implicants]
    essential_implicants = [x[0] for x in essential_implicants]


    for i in range(len(functions)):
        functions[i] = [x[0] for x in functions[i]]

    return prime_implicants, essential_implicants, functions


def main():
    variables = int(input("Enter the number of variables:\n")) # Number of variables to be used
    min_terms = [int(x) for x in input("Enter the minterms (space seperated) :\n").split()] # List of minterms

    prime_implicants, essential_implicants, functions = tabulation(variables, min_terms)

    printOption = input('\n\nDo you want to use your own variables?\n')

    if printOption[0].lower() == 'y':
        variables = [input("\nEnter the variables (space seperated) :\n").split()]
        print("\nThe prime implicants are:")
        printingAlternate(prime_implicants, variables)

        print("\nThe essential implicants are:")
        printingAlternate(essential_implicants, variables)

        print("\nThe possible functions are:")
        for i in functions:
            printingAlternate(i, variables)

    else:
        print("\nThe prime implicants are:")
        printing(prime_implicants, '+')

        print("\nThe essential implicants are:")
        printing(essential_implicants, '+')

        print("\nThe possible functions are:")
        for i in functions:
            printing(i, '+')


if __name__ == "__main__":
    main()