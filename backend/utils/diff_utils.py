def print_diff(diff_text: str):
    """
    Pretty print git diff output.
    """

    if not diff_text.strip():
        print("\nNo changes detected.\n")
        return

    print("\n=========== DIFF PREVIEW ===========\n")
    print(diff_text)
    print("\n====================================\n")
