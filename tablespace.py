import os
import sys


class TabReplace(object):
    """docstring for TabReplace"""
    def __init__(self, path=None):
        self.file_filter = ('.js', '.html', '.css')
        assert os.path.exists(path)
        self.dir_name = path
        self._dir_name = path

    @classmethod
    def replace(cls, file_path):
        with open(file_path, 'rw') as fg:
            data = fg.read().replace('\t', '    ')
            fg.write(data)

    def progress(self, path):
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
                        self.progress(file_path)

    def run(self):
        if self.dir_name:
            self.progress(self.dir_name)
            return None

        raise ValueError('dirname is invalid')


def fetch_command(act_command, dir_name=None):
    if not act_command == 'run':
        return

    if dir_name:
        tr = TabReplace()
        tr.dir_name = dir_name
    else:
        tr = TabReplace()
        tr.dir_name = os.path.dirname(os.path.abspath(__file__))
    tr.run()
    return


def main_help_text():
    usage = [
        'Available act_command:',
        '',
        'run:',
        'if --dir=None or anyless means run it from current dir. else dir=dirname means run it from dirname',
        '',
        'help'
    ]
    return '\n'.join(usage)


def execute_from_command_line(command=None):
    try:
        act_command = command[1]
    except IndexError:
        act_command = 'help'

    commands_list = ['help', 'run']
    if not act_command == 'help' and act_command in commands_list:
        try:
            dir_command = command[2]
            dir_name = dir_command.replace('--dir=', '')
        except IndexError:
            dir_name = None
        fetch_command(act_command, dir_name=dir_name)
    else:
        sys.stdout.write(main_help_text())


if __name__ == '__main__':
    execute_from_command_line(command=sys.argv)
