def pass_gen():
    import random, string # pylint: disable=import-outside-toplevel,multiple-imports
    return ''.join(random.choice(string.ascii_letters) for i in range(30))
