def Strongest_Extension(class_name, extensions):
    strongest = extensions[0]
    max_strength = sum(1 for c in strongest if c.isupper()) - sum(1 for c in strongest if c.islower())
    for ext in extensions[1:]:
        strength = sum(1 for c in ext if c.isupper()) - sum(1 for c in ext if c.islower())
        if strength > max_strength:
            max_strength = strength
            strongest = ext
    return f"{class_name}.{strongest}"
