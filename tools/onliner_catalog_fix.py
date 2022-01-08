from tools.onliner_catalog import catalog


def fix_cat(cat):
    result = {}
    for key, val in cat.items():

        fix_key = ' '.join(key.split())

        if type(val) == dict:
            val = fix_cat(val)

        result[fix_key] = val

    return result


print(fix_cat(catalog))