Webster
=======

Webster is a self validating dict object for python.

It expands upon dict's capability by allowing you to pass in a validation 
dict object with either types or regular expression values.

Then you can use it for validation by using it as a condition or get
back a detailed error response.

  import Webster

  # create a schema
  schema = {'amount': '([+-]?\\d*\\.\\d+)(?![-+0-9\\.])',
            'credit_card': {
              'number': '((?:(?:\\d{4}[- ]){3}\\d{4}|\\d{16}))(?![\\d])',
              'expiration_date': '((?:(?:0[1-9])|(?:1[0-2]))\\/(?:\\d{2}))(?![\\d])'}
           }
  
  # create the object and pass the schema into the init
  im_a_dict = Webster(schema)
  
  #  add your values
  im_a_dict['amount'] = '1.00'
  im_a_dict['credit_card'] = {}
  im_a_dict['credit_card']['number'] = '4111111111111111'
  im_a_dict['credit_card']['expiration_date'] = '05/12'

  # lets see if we are valid or not
  print im_a_dict.is_valid()
