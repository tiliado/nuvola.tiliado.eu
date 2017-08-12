if __name__ == "__main__":
    import sys
    from nuvola_index.main import main

    # noinspection PyBroadException
    try:
        code = main(sys.argv)
    except Exception as e:
        import traceback
        print("Unexpected failure:", file=sys.stderr)
        traceback.print_exc()
        code = 2
    sys.exit(code)
