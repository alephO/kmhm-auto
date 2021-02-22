from utils.micro_mock import MicroMock


class Args(object):
    def __init__(self):
        args_dict = {
            'console': True,
            'simple_mode': True,
        }
        self.args = MicroMock(iDict=args_dict)

    def get_args(self):
        return self.args


arg_parser = Args()
