import custom_types as pmrtp
 
class BasicConfigurator():
    
    dictionary = {}
    valid_entries = {}

    convert = True
    
    def __init__(self, dictionary={}, convert=True):

        self.dictionary = dictionary
        self.convert = convert

        self.check()

    def check(self):
        
        #check keys
        valid_keys = self.valid_entries.keys()
        for key in self.dictionary:
            if key not in valid_keys:
                raise KeyError()
        del valid_keys

        #check values
        valid_types = self.valid_entries.values()
        #checks if the dictionary values are types
        for tp in valid_types:
            if not isinstance(tp, type)  :
                raise SyntaxError(f"{tp} must be a type")
        del valid_types

        #checks if the values in the dictionary have the same type of the type in valid_types
        for key in self.dictionary:
            dict_val = self.dictionary[key]
            vtype = self.valid_entries[key]

            if not isinstance(dict_val, vtype):
                
                if not self.convert:
                    raise ValueError(f"{dict_val} must be of type {vtype}")
                else:
                    try:
                        self.dictionary[key] = vtype(dict_val)
                    except TypeError:
                        raise ValueError(f"It wasn't possible to convert {dict_val} to {vtype}")

        return 0 #no problems

    def is_valid(self, key, value):
        return key in self.valid_entries \
                and \
                isinstance(value, self.valid_entries[key])


    def __setitem__(self, key, value):
        if key in self.valid_entries:
            #automatically tries to convert the value in a valid value
            vtype = self.valid_entries[key]
            try:
                self.dictionary[key] = vtype(value)
            except TypeError:
                raise ValueError(f"It wasn't possible to convert {value} into {vtype}")

        else:
            raise KeyError(f"'{key}' is not a valid key in the dictionary")

    def __getitem__(self, key):
        return self.dictionary[key]

    def get(self, key, missing=None):
        value = self.dictionary.get(key, missing)
        return value
    
    def __call__(self):
        return self.dictionary

    def __str__(self):
        return str(self.dictionary)


class FileConfigurator(BasicConfigurator):
    valid_entries = dict(\
            name = str, \
            path = str, \
            is_header = bool, \
            precompile = bool, \
            tags = pmrtp.array, \
            )

    def __init__(self, dictionary={}, convert=True, index=-1):
        super().__init__(dictionary, convert)

