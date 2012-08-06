"""
    ValidDict - The self validating dictionary object for python
    Copyright (C)2012  David F. Lenwell
    
    This library is free software; you can redistribute it and/or
    modify it under the terms of the GNU Library General Public
    License as published by the Free Software Foundation; either
    version 2 of the License, or (at your option) any later version.
    
    This library is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    Library General Public License for more details.
    
    You should have received a copy of the GNU Library General Public
    License along with this library; if not, write to the
    Free Software Foundation, Inc., 51 Franklin St, Fifth Floor,
    Boston, MA  02110-1301, USA.
    
    
    http://www.gnu.org/licenses/gpl-3.0.txt
    
"""
import re


class ValidDict(dict):
    """
        ValidDict extends dict
        
        It expands upon dict's capability by allowing you 
        to pass in a validation dict object with either types or 
        regular expression values. 
        
        Then you can use it for validation by using it as a condition or get 
        back a detailed error response. 
        
        import valid_dict

        # create a schema
        schema = { 'amount' : '([+-]?\\d*\\.\\d+)(?![-+0-9\\.])' ,
              'credit_card' : { 'number' : '((?:(?:\\d{4}[- ]){3}\\d{4}|\\d{16}))(?![\\d])' ,
                       'expiration_date' : '((?:(?:0[1-9])|(?:1[0-2]))\\/(?:\\d{2}))(?![\\d])' } }
        
        # create the object and pass the schema into the init 
        vd = valid_dict.ValidDict(schema)
        
        # build out your values 
        vd['amount'] = '1.00'
        vd['credit_card'] = {}
        vd['credit_card']['number'] = '4111111111111111'
        vd['credit_card']['expiration_date'] = '05/12'
        
        
        # lets see if we are valid or not 
        print vd.is_valid()
        
        
        
        
    """
    _error = {}
    _missing = []
    _invalid = []
    
    _schema = {}
    
    _is_valid = False
    
    def __init__(self, schema = {}, to_import = None):
        """
            __init__
            
            param:  schema
            param:  to_import 
            
            init function .. takes a schema and will eventually allow you to 
            import an outside dictionary 
            
        """
        self.schema = schema        
        
        if to_import:
            # if to import pass to import function (not built yet)
            pass    
    
    
    @property
    def invalid(self):
        """
            get for invalid list 
        """
        return self._invalid
    
    @property
    def missing(self):
        """
            get for missing list 
        """
        return self._missing
    
    @property
    def error(self):
        """ 
            get for _error object
        """
        self._error['missing'] = self._missing
        self._error['invalid'] = self._invalid
        
        return self._error
    
        
    
    # lets override some built in behavior
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError as e:
            raise AttributeError(e)

    def __setattr__(self, name, value):
        self[name] = value

    def __iter__(self):
        return iter(self.keys())

    def __repr__(self):
        return pprint.pformat(self)
    
    
    def _validate_value(self, _re, value):
        """
            validates the provided regex against the provided value
            
        """
        return re.compile(_re,re.IGNORECASE|re.DOTALL).search(value)
    
    
    def _validate_dict(self, _key, _to_validate):
        """
            internally called dict validation function. 
            
            This function will loop through the _to_validate param and validate 
            they keys and the fields. 
            
            If it encounters a missing key.. 
                it adds it to self._errors['missing_keys'] list
                
            If it encounters another dict .. it waits for it to be validated 
                it then validates the key against the regex 
                provided in the schema.
            
                If it encounters an invalid value it adds the key to the 
                    self._errors['missing_keys'] list
                
                
        """
        return_value = True
        
        for p in _key.iterkeys():
            if not _to_validate.has_key(p):
                self._error['missing'].append(p)
                return_value = False
                
            elif isinstance(_key[p], dict):
                if not isinstance(_to_validate[p], dict):
                    self._error['missing'].append(_key[p].keys())
                    return_value = False
                        
                elif not self._validate_dict(_key[p], _to_validate[p]):
                    return_value = False
            else: 
                """validate regex here """
                if self._validate_value(_key[p], _to_validate[p]):
                    self._error['invalid'].append(p)
                    return_value = False
                    
        return return_value
        
    
    def validation(self):
        """
            Calls for validation and outputs either a True or the error list. 
        
        """
        if self.is_valid():
            return True
        else:
            return self._error
    
    
    def is_valid(self):
        """
            main trigger for validation.. clears the error lists
        
        """
        #clear missing 
        while self._error['missing']: self._error['missing'].pop()
        while self._error['invalid']: self._error['invalid'].pop()
        
        # kick off the validation loop on my self 
        if self._validate_dict(self.schema, self):         
            return True
        else:
            print 'missing keys: ', str(self._error)      
            return False
        
  