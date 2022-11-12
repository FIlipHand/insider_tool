import os


def get_project_root():
    """
    Get Current Solutions Directory
    Returns
    -------
    str
        Application Path
    """
    return os.getcwd().split('src')[0]
