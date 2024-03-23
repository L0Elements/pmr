#this file include all the tokens interpreted by the program
#it will be used to understand which parts of the program are executed



#the main dictionary, to be imported during comprehension
tokens = {\
        'new': 0, \
        'add': 1, \
        'rm': 2, 'remove': 2, \
        'list': 3, \

        'build': None, \
        'package': None, \
        'build-profile': None, \
        'config': None, \
        'module': None, \
        'mod': None, \
}






if __name__ == '__main__':
    print(tokens)
