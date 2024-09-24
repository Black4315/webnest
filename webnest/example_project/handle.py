import os

def main():
    """handle and run your application task """
    try:
        from webnest.handling import execute_from_args
    except ImportError as e:
        raise ImportError(
            "Faild to import webnest. Are you sure it's installed "
            "in your environment ? did you activate your "
            "environment ?"
        ) from e
     
    execute_from_args()


if __name__ == '__main__':
    main()
