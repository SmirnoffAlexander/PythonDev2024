import cmd
import shlex

import cowsay


class CowSayShell(cmd.Cmd):
    intro = """Welcome to CowSay shell! Type help or ? to list commands.\n"""
    prompt = "(cowsay)"

    def shlex_parser(self, args):
        return shlex.split(args)

    def do_cowsay(self, args):
        """
        Parameters are listed with their
        corresponding options in the cowsay command. Returns the resulting cowsay
        string

        :param message: The message to be displayed. Required param.
        :param cow: -f – the available cows can be found by calling list_cows
        :param eyes: -e or eye_string
        :param tongue: -T or tongue_string
        """
        splitted_args = self.shlex_parser(args)
        kwargs = {
            "message": splitted_args[0],
            "cow": "default",
            "eyes": cowsay.Option.eyes,
            "tongue": cowsay.Option.tongue,
        }

        n_args = len(splitted_args)
        if n_args > 1 and n_args % 2:
            for key, param in zip(splitted_args[1::2], splitted_args[2::2]):
                if key == "-f":
                    kwargs["cow"] = param
                elif key == "-e":
                    kwargs["eyes"] = param
                elif key == "-T":
                    kwargs["tongue"] = param
                else:
                    print(f"No such key {key}!")
        elif not n_args % 2:
            print(
                "Number of keys don't match number of params! Default params are used!"
            )

        print(cowsay.cowsay(**kwargs))

    def do_list_cows(self, args):
        """Lists all cow file names"""
        splitted_args = self.shlex_parser(args)
        print(cowsay.list_cows(*splitted_args))

    def do_make_bubble(self, args):
        """
        Wraps text is wrap_text is true, then pads text and sets inside a bubble.
        This is the text that appears above the cows
        """
        splitted_args = self.shlex_parser(args)
        print(cowsay.make_bubble(*splitted_args))

    def do_cowthink(self, args):
        """
        Parameters are listed with their
        corresponding options in the cowthink command. Returns the resulting cowsay
        string

        :param message: The message to be displayed. Required param.
        :param cow: -f – the available cows can be found by calling list_cows
        :param eyes: -e or eye_string
        :param tongue: -T or tongue_string
        """
        splitted_args = self.shlex_parser(args)
        kwargs = {
            "message": splitted_args[0],
            "cow": "default",
            "eyes": cowsay.Option.eyes,
            "tongue": cowsay.Option.tongue,
        }

        n_args = len(splitted_args)
        if n_args > 1 and n_args % 2:
            for key, param in zip(splitted_args[1::2], splitted_args[2::2]):
                if key == "-f":
                    kwargs["cow"] = param
                elif key == "-e":
                    kwargs["eyes"] = param
                elif key == "-T":
                    kwargs["tongue"] = param
                else:
                    print(f"No such key {key}!")
        elif not n_args % 2:
            print(
                "Number of keys don't match number of params! Default params are used!"
            )

        print(cowsay.cowthink(**kwargs))

    def do_bye(self, arg):
        """Stop interaction with cow!"""
        print("Thank you for using CowSay")
        return True


if __name__ == "__main__":
    CowSayShell().cmdloop()
