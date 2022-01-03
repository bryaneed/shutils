import os
import sys


class TabReplace(object):
    """docstring for TabReplace"""
    def __init__(self, path=None):
        self.file_filter = ('.js', '.html', '.css')
        self._dir_name = path

    @property
    def dir_name(self):
        return self._dir_name

    @dir_name.setter
    def dir_name(self, path):
        if not os.path.exists(path):
            raise IOError('path is not valid.')
        self._dir_name = path

    @classmethod
    def replace(cls, file_path):
        with open(file_path, 'rw') as fg:
            data = fg.read().replace('\t', '    ')
            fg.write(data)

    def handle(self, path):
        if os.path.isfile(path):
            self.replace(path)
        else:
            for file in os.listdir(path):
                file_path = os.path.join(path, file)
                if os.path.exists(file_path):
                    if os.path.isfile(file_path):
                        head, ext = os.path.splitext(file_path)
                        if ext in self.file_filter:
                            self.replace(file_path)
                    else:
                        self.handle(file_path)

    def process_func(self):
        if self.dir_name:
            self.handle(self.dir_name)
            return None

        raise ValueError('dirname is invalid')


def fetch_command(subcommand, dir_name=None):
    if not subcommand == 'run':
        return

    if dir_name:
        tr = TabReplace()
        tr.dir_name = dir_name
    else:
        tr = TabReplace()
        tr.dir_name = os.path.dirname(os.path.abspath(__file__))
    tr.process_func()
    return


def main_help_text():
    usage = [
        'Available subcommand:',
        '',
        'run:',
        'if --dir=None or anyless means run it from current dir. else dir=dirname means run it from dirname',
        '',
        'help'
    ]
    return '\n'.join(usage)


def execute_from_command_line(command=None):
    try:
        subcommand = command[1]
    except IndexError:
        subcommand = 'help'

    commands_list = ['help', 'run']
    if not subcommand == 'help' and subcommand in commands_list:
        try:
            dirname_commands = command[2]
            dirname = dirname_commands.replace('--dir=', '')
        except IndexError:
            dirname = None
        fetch_command(subcommand, dir_name=dirname)
    else:
        sys.stdout.write(main_help_text())


if __name__ == '__main__':
    execute_from_command_line(command=sys.argv)
