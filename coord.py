class Coord:
    def __init__(self, *argv):
        len_argv = len(argv)
        if len_argv == 1:
            self.x = argv[0][0]
            self.y = argv[0][1]
        elif len_argv == 2:
            self.x = argv[0]
            self.y = argv[1]
        else:
            raise Exception('Invalid number of arguments for Coord constructor')

    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        else:
            raise Exception('Invalid key for get Coord')

    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        else:
            raise Exception('Invalid key for set Coord')