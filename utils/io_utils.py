import os


allowed_extensions = {
    "image": ["jpg", "jpeg", "png"],
    "video": ["avi", "mp4"]
}


def get_file_extension(file):
    return file.split(".")[-1]

def is_allowed_extension(ext):
    '''
    Return type of file if it's in allowed extensions or None if it's not.

    :param ext: string
    :return: 'image', 'video' or None
    '''
    for key, value in allowed_extensions.items():
        if ext in value:
            return key
    else:
        return None

def check_path(path):
    '''
    Return list of types and paths to files with allowed media extensions (image, video).
    :param path: string
    :return: [['video', path_to_file],...]
    '''
    if not os.path.exists(path):
        raise InputError('Path not exists')

    if os.path.isdir(path):
        files = []
        # r=root, d=directories, f = files
        for r, d, f in os.walk(path):
            for file in f:
                extension = get_file_extension(file)
                extension_type = is_allowed_extension(extension)
                if extension_type:
                    files.append([extension_type, os.path.join(r, file)])
        if files:
            return files
        else:
            raise InputError('There are not allowed media files in the directory path.')
    elif os.path.isfile(path):
        extension = get_file_extension(path)
        extension_type = is_allowed_extension(extension)
        if extension_type:
            return [[extension_type, path]]
        else:
            raise InputError(f'File extension is not allowed: {extension}')


