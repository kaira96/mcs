
def is_form_fields_is_empty(form, key_startswith) -> bool:
    """
    If the values of the form fields are empty return False otherwise True
    """
    return all(value != '' for (key, value) in form.data.items() if key.startswith(key_startswith))
