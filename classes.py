import configparser
import os


class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, start, end):
        self.id = None
        self.start = start
        self.end = end
        self.isSelected = False

        if start.y == end.y:
            if (start.y == 20) or (start.y == 344):
                self.isSelected = True
        elif start.x == end.x:
            if (start.x == 20) or (start.x == 344):
                self.isSelected = True

    def get_id(self):
        return self.id

    def set_id(self, line_id):
        self.id = line_id

    def print(self):
        return print('[', self.start.x, ', ', self.start.y, '], [', self.end.x, ', ', self.end.y, '], id=', self.id,
                     ', isSelected = ', self.isSelected)


class Square:
    def __init__(self, top, right, bottom, left):
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left

    def contains_line(self, line):
        return (line == self.top or line == self.right or
                line == self.bottom or line == self.left)

    def is_all_selected(self):
        return self.top.isSelected and self.right.isSelected and self.bottom.isSelected and self.left.isSelected

    def print(self):
        self.top.print()
        self.right.print()
        self.bottom.print()
        self.left.print()
        print('-----')


class Player:
    def __init__(self, color):
        self.color = color
        self.num_cells = 0

    @classmethod
    def squares_owned(cls, players):
        return sum(player.num_cells for player in players)


class Config:
    filename = 'config.ini'
    @staticmethod
    def get(section, variable, _type=None):
        if os.path.isfile(Config.filename):
            config = configparser.ConfigParser()
            config.read(Config.filename)
            try:
                if _type == 'int':
                    res = config.getint(section, variable)
                else:
                    res = config.get(section, variable)
            except configparser.Error:
                res = ''
            return res
        else:
            return None

    @staticmethod
    def set(section, name, value):
        config = configparser.ConfigParser()
        config.read(Config.filename)
        if config.has_section(section) is False:
            config.add_section(section)
        config.set(section, name, str(value))
        with open(Config.filename, 'w') as configfile:
            config.write(configfile)