def Strongest_Extension(class_name, extensions):
    def calculate_strength(extension):
        cap = sum(1 for c in extension if c.isupper())
        sm = sum(1 for c in extension if c.islower())
        return cap - sm

    if not extensions:
        return f"{class_name}."

    strongest = extensions[0]
    max_strength = calculate_strength(strongest)

    for ext in extensions[1:]:
        strength = calculate_strength(ext)
        if strength > max_strength:
            max_strength = strength
            strongest = ext

    return f"{class_name}.{strongest}"
