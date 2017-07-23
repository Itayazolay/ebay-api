from lxml import objectify

EM = objectify.ElementMaker(annotate=False)


def dict2xml(root: objectify.Element, data: dict):
    for key, value in data.items():
        if isinstance(value, dict):
            sub_root = getattr(EM, key)()
            element = dict2xml(sub_root, value)
            root.append(element)
        elif isinstance(value, list):
            """
            {"a": ["b","c","d"]} => <a>b</a> <a>c</a> <a>d</a>
            {"a": [{"b":1}, {"b": 2}] } => <a><b>1</b></a> <a><b>2</b></a>
            """
            sub_root = getattr(EM, key)
            for val in value:
                if isinstance(val, dict):
                    element = dict2xml(sub_root(), val)
                else:
                    element = sub_root(val)
                root.append(element)
        else:
            element = getattr(EM, key)(value)
            root.append(element)
    return root


def xml2dict(root: objectify.Element):
    data = {}
    namespace = root.nsmap.get(None, "")
    clean_tag = lambda tag: tag.replace("{%s}" % namespace, "")

    for element in root.getchildren():
        # Figure out type
        if not hasattr(element, "pyval"):  # A root element
            sub_data = xml2dict(element)
            name, val = clean_tag(element.tag), sub_data
        else:
            name, val = clean_tag(element.tag), element.pyval
        # Add the value to the data dict
        if name in data:
            # If it's already in data, append or make a list out of it.
            if isinstance(data[name], list):
                data[name].append(val)
            else:
                data[name] = [data[name], val]
        else:
            # Just a regular value.
            data[name] = val
    return data
