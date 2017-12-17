'''
File: debug_lib.py
Title: Debugs Library
Description:

    Python 3+

    Requires a module to semantically follow a certain docstring style and
    function call style for the purpose of debugging
    Function definitions must contain descriptive docstrings with mandatory
    specifications. Some of these include listing the inputs, the function
    title and describing the output.

    Features of the library include:
    *******************************
    1) Module specific debug levels (5 descriptive debug levels)
    2) Debugging Module as an object
    3) Argument count verification
    4) Function name from docstring
    5) Process docstring using regex
    6) Exception Handling:
       a) Exception specific debug level
       b) Backtrace prints include arguments to functions

'''

import re

_CONST_debug_levels = {
    'Very Low':4,
    'Low':3,
    'Medium':2,
    'High':1,
    'Critical':0
    }

def get_debug_lev(debug_lev):
    """
    Title: Get Debug Level
    Input: Debug Level Name
    Output: Debug Level
    """
    if debug_lev not in _CONST_debug_levels.keys():
        return _CONST_debug_levels['Critical']
    else:
        return _CONST_debug_levels[debug_lev]


class debug_mod(object):
    '''
    Debug Module Class:
    Create an instance for each module to isolate debug levels to the module
    '''
    def __init__(self, module, module_debug_level, exception_case_debug_level):
        """
        Title: Init Function for Debug Module Instance
        Input 1: Module Name
        Input 2: Module's Debug Level
        Input 3: Exception Case Debug Level
        Output: None
        """
        self.module = module
        self.module_debug_level = module_debug_level
        self.exception_case_debug_level = exception_case_debug_level

    def change_module_debug_lev(self, new_mod_debug_lev):
        """
        Title: Change the Module's Debug Level
        Input 1: New Debug Level for module
        Output: None
        """
        self.module_debug_level = new_mod_debug_lev

    def get_match_from_docstring(self, function, regex_obj):
        """
        Title: Get the match from a function's docstring
        Input 1: Function
        Input 2: Regex object
        Output: The 1st string matching the regex
        """
        docstring = function.__doc__
        match_str = regex_obj.findall(docstring)[0]
        return match_str

    def get_title_from_docstring(self, fn_name):
        """
        Title: Get title from docstring
        Input: Function Name
        Output: Title from the Docstring of function
        """
        return 'Function: {0}'.format(self.get_match_from_docstring(fn_name,
                re.compile('Title: (.+)')))

    def get_num_inputs_to_fn_from_docstring(self, function):
        '''
        Title: Get Number of Inputs To Function From Docstring
        Input 1: Function
        Output: Number of Inputs From Docstring
        '''
        docstring = function.__doc__
        input_re = re.compile('Input .+:')
        return len(input_re.findall(docstring))

    def _dbg_fn_matrix_from_fn_title(self, fn_name):
        """
        Title: Debug Fn Matrix From Fn Title
        Input: Fn Name
        Output: {_get_title_from_docstring: [fn_name]}
        """
        return {self.get_title_from_docstring:[fn_name]}

    def print_debug_msg(self, function_matrix, message, debug_level):
        """
        Title: Print Debug Messages
        Input 1: Function Matrix - Functions executed to get the primary message
        Input 2: Secondary Message
        Input 3: Debug Level
        Output: None
        """
        if debug_level <= self.module_debug_level:
            debug_msg = ''
            for function, args in function_matrix.items():
                debug_msg += function(*args)
            message = message.replace('\n','\n\t')
            print('Module: {0}'.format(self.module))
            print('{0}\n\t{1}'.format(debug_msg, message))

    def print_debug_msg_lev_crit(self, function_matrix, message):
        """
        Title: Print Critical Debug Messages
        Input 1: Function Matrix
        Input 2: Secondary Message
        Output: None
        """
        self.print_debug_msg(function_matrix, message,
            get_debug_lev('Critical'))

    def DEBUG_CRITICAL(self, fn_name, message):
        """
        Title: Wrapper for Print Critical Messages
        Input 1: Function Name
        Input 2: Message
        Output: None
        """
        self.print_debug_msg_lev_crit(
            self._dbg_fn_matrix_from_fn_title(fn_name), message)

    def print_debug_msg_lev_high(self, function_matrix, message):
        """
        Title: Print Debug Level High Debug Messages
        Input 1: Function Matrix
        Input 2: Secondary Message
        Output: None
        """
        self.print_debug_msg(function_matrix, message, get_debug_lev('High'))

    def DEBUG_HIGH(self, fn_name, message):
        """
        Title: Wrapper for Print Debug Level High Messages
        Input 1: Function Name
        Input 2: Message
        Output: None
        """
        self.print_debug_msg_lev_high(
            self._dbg_fn_matrix_from_fn_title(fn_name), message)

    def print_debug_msg_lev_medium(self, function_matrix, message):
        """
        Title: Print Debug Level Medium Debug Messages
        Input 1: Function Matrix
        Input 2: Secondary Message
        Output: None
        """
        self.print_debug_msg(function_matrix, message, get_debug_lev('Medium'))

    def DEBUG_MEDIUM(self, fn_name, message):
        """
        Title: Wrapper for Print Debug Level Medium Messages
        Input 1: Function Name
        Input 2: Message
        Output: None
        """
        self.print_debug_msg_lev_medium(
            self._dbg_fn_matrix_from_fn_title(fn_name), message)

    def print_debug_msg_lev_low(self, function_matrix, message):
        """
        Title: Print Debug Level Low Debug Messages
        Input 1: Function Matrix
        Input 2: Secondary Message
        Output: None
        """
        self.print_debug_msg(function_matrix, message, get_debug_lev('Low'))

    def DEBUG_LOW(self, fn_name, message):
        """
        Title: Wrapper for Print Debug Level Low Messages
        Input 1: Function Name
        Input 2: Message
        Output: None
        """
        self.print_debug_msg_lev_low(
            self._dbg_fn_matrix_from_fn_title(fn_name), message)

    def print_debug_msg_lev_very_low(self, function_matrix, message):
        """
        Title: Print Debug Level Very Low Debug Messages
        Input 1: Function Matrix
        Input 2: Secondary Message
        Output: None
        """
        self.print_debug_msg(function_matrix, message,
            get_debug_lev('Very Low'))

    def DEBUG_VERY_LOW(self, fn_name, message):
        """
        Title: Wrapper for Print Debug Level Very Low Messages
        Input 1: Function Name
        Input 2: Message
        Output: None
        """
        self.print_debug_msg_lev_very_low(
            self._dbg_fn_matrix_from_fn_title(fn_name), message)

    def get_debug_function_from_debug_level(self, debug_level):
        '''
        Title: Get DEBUG Function From Debug Level
        Input: Debug Level
        Output: DEBUG Function according to the debug level
        '''
        if debug_level == get_debug_lev('Critical'):
            return self.DEBUG_CRITICAL
        elif debug_level == get_debug_lev('High'):
            return self.DEBUG_HIGH
        elif  debug_level == get_debug_lev('Medium'):
            return self.DEBUG_MEDIUM
        elif debug_level == get_debug_lev('Low'):
            return self.DEBUG_LOW
        elif debug_level == get_debug_lev('Very Low'):
            return self.DEBUG_VERY_LOW
        else:
            return self.DEBUG_CRITICAL

    def debug_decorator(self, func):
        '''
        Title: Debug Decorator
        Input: Function To Be Decorated
        Output: Error Propogating Function Wrapper Which Provides Context
        '''
        def func_wrapper(*args):
            try:
                expected_num_args = self.get_num_inputs_to_fn_from_docstring(
                        func)
                if len(args) is not expected_num_args:
                    raise Exception('Expected Number of Args: {0} Received: {1}'
                            .format(expected_num_args, len(args)))
                return func(*args)
            except Exception as e:
                self.get_debug_function_from_debug_level(
                        self.exception_case_debug_level)(func,
                                'Error Has Occurred. Context is:\n{0}'.
                                format(args))
                raise e
        func_wrapper.__doc__ = func.__doc__
        return func_wrapper


def main():
    '''
    Title: Debug Module Library
    Input: None
    Output: None
    '''
    pass

if __name__ == '__main__':
    main()
    debug_mod_dbg = debug_mod('Debug Module Library',
            get_debug_lev('Critical'), get_debug_lev('Critical'))
    dbg_msg = 'Debug Module Functional'
    debug_mod_dbg.DEBUG_CRITICAL(main, dbg_msg)
