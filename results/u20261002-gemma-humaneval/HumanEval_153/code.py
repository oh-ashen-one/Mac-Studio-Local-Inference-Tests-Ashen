def Strongest_Extension(class_name, extensions):
    """You will be given the name of a class (a string) and a list of extensions.
    The extensions are to be used to load additional classes to the class. The
    strength of the extension is as follows: Let CAP be the number of the uppercase
    letters in the extension's name, and let SM be the number of lowercase letters 
    in the extension's name, the strength is given by the fraction CAP - SM. 
    You should find the strongest extension and return a string in this 
    format: ClassName.StrongestExtensionName.
    If there are two or more extensions with the same strength, you should
    choose the one that comes first in the list.
    """
    def get_strength(ext):
        cap = sum(1 for char in ext if char.isupper())
        sm = sum(1 for char in ext if char.islower())
        return cap - sm

    strongest_ext = extensions[0]
    max_strength = get_strength(extensions[0])

    for i in range(1, len(extensions)):
        current_strength = get_strength(extensions[i])
        if current_strength > max_strength:
            max_strength = current_strength
            strongest_ext = extensions[i]

    return f"{class_name}.{strongest_ext}"
