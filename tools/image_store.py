def get_path_image_store(filename, storage):
    file = filename.split('.')
    cat = 'dot'
    if len(file[0]) > 1:
        cat = file[0][1]
    return f'{storage}/{file[0][0]}/{cat}/{filename}'

