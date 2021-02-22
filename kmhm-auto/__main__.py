from config.arg_parser import arg_parser
from version import __version__

if __name__ == '__main__':
    args = arg_parser.get_args()
    if args.console:
        print('Starting kmhm_auto in console mode. Version %s' % __version__)
        import kmhm_console
        kmhm_console.main(simple_mode=args.simple_mode)
    else:
        print('GUI mode is under development.')