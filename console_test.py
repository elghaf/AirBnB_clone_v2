#!/usr/bin/python3
""" Console Module """
import cmd
import sys
from models.base_model import BaseModel
from models.__init__ import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """ Contains the functionality for the HBNB console"""

    # determines prompt for interactive/non-interactive modes
    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''

    # Mapping of class names to corresponding classes
    available_classes = {
        'BaseModel': BaseModel, 'User': User, 'Place': Place,
        'State': State, 'City': City, 'Amenity': Amenity,
        'Review': Review
    }

    # List of supported dot commands
    supported_dot_commands = ['all', 'count', 'show', 'destroy', 'update']

    # Mapping of attribute types for casting during updates
    attribute_types = {
        'number_rooms': int, 'number_bathrooms': int,
        'max_guest': int, 'price_by_night': int,
        'latitude': float, 'longitude': float
    }

    def preloop(self):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def precmd(self, line):
        """Reformat command line for advanced command syntax."""
        _cmd = _cls = _id = _args = ''  # initialize line elements

        # scan for general formating - i.e '.', '(', ')'
        if not ('.' in line and '(' in line and ')' in line):
            return line

        try:  # parse line left to right
            pline = line[:]  # parsed line

            # isolate <class name>
            _cls = pline[:pline.find('.')]

            # isolate and validate <command>
            _cmd = pline[pline.find('.') + 1:pline.find('(')]
            if _cmd not in HBNBCommand.supported_dot_commands:
                raise Exception

            # if parentheses contain arguments, parse them
            pline = pline[pline.find('(') + 1:pline.find(')')]
            if pline:
                # partition args: (<id>, [<delim>], [<*args>])
                pline = pline.partition(', ')  # pline convert to tuple

                # isolate _id, stripping quotes
                _id = pline[0].replace('\"', '')
                # possible bug here:
                # empty quotes register as empty _id when replaced

                # if arguments exist beyond _id
                pline = pline[2].strip()  # pline is now str
                if pline:
                    # check for *args or **kwargs
                    if pline[0] == '{' and pline[-1] == '}' \
                            and type(eval(pline)) is dict:
                        _args = pline
                    else:
                        _args = pline.replace(',', '')
                        # _args = _args.replace('\"', '')
            line = ' '.join([_cmd, _cls, _id, _args])

        except Exception as mess:
            pass
        finally:
            return line

    def postcmd(self, stop, line):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def do_quit(self, command):
        """ Method to exit the HBNB console"""
        exit()

    def help_quit(self):
        """ Prints the help documentation for quit  """
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        """ Handles EOF to exit program """
        print()
        exit()

    def help_EOF(self):
        """ Prints the help documentation for EOF """
        print("Exits the program without formatting\n")

    def emptyline(self):
        """ Overrides the emptyline method of CMD """
        pass

    def do_create(self, args):
        """ Create an object of any class"""
        try:
            if not args:
                raise SyntaxError()
            arg_list = args.split(" ")
            kwargs = {}
            for arg in arg_list[1:]:
                arg_splitted = arg.split("=")
                arg_splitted[1] = eval(arg_splitted[1])
                if type(arg_splitted[1]) is str:
                    arg_splitted[1] = arg_splitted[1].replace("_", " ").replace('"', '\\"')
                kwargs[arg_splitted[0]] = arg_splitted[1]
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        new_instance = HBNBCommand.available_classes[arg_list[0]](**kwargs)
        new_instance.save()
        print(new_instance.id)

    def help_create(self):
        """ Help information for the create method """
        print("Creates a class of any type")
        print("[Usage]: create <className>\n")

    def do_show(self, args):
        """ Method to show an individual object """
        new = args.partition(" ")
        class_name = new[0]
        object_id = new[2]

        # guard against trailing args
        if object_id and ' ' in object_id:
            object_id = object_id.partition(' ')[0]

        if not class_name:
            print("** class name missing **")
            return

        if class_name not in HBNBCommand.available_classes:
            print("** class doesn't exist **")
            return

        if not object_id:
            print("** instance id missing **")
            return

        key = class_name + "." + object_id
        try:
            print(storage._FileStorage__objects[key])
        except KeyError:
            print("** no instance found **")

    def help_show(self):
        """ Help information for the show command """
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

    def do_destroy(self, args):
        """ Destroys a specified object """
        new = args.partition(" ")
        class_name = new[0]
        object_id = new[2]
        if object_id and ' ' in object_id:
            object_id = object_id.partition(' ')[0]

        if not class_name:
            print("** class name missing **")
            return

        if class_name not in HBNBCommand.available_classes:
            print("** class doesn't exist **")
            return

        if not object_id:
            print("** instance id missing **")
            return

        key = class_name + "." + object_id

        try:
            del(storage.all()[key])
            storage.save()
        except KeyError:
            print("** no instance found **")

    def help_destroy(self):
        """ Help information for the destroy command """
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, args):
        """ Shows all objects, or all objects of a class"""
        print_list = []

        if args:
            args = args.split(' ')[0]  # remove possible trailing args
            if args not in HBNBCommand.available_classes:
                print("** class doesn't exist **")
                return
            for key, value in storage.all(HBNBCommand.available_classes[args]).items():
                print_list.append(str(value))
        else:
            for key, value in storage.all().items():
                print_list.append(str(value))
        print(print_list)

    def help_all(self):
        """ Help information for the all command """
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className>\n")

    def do_count(self, args):
        """Count current number of class instances"""
        count = 0
        for key, value in storage._FileStorage__objects.items():
            if args == key.split('.')[0]:
                count += 1
        print(count)

    def help_count(self):
        """ Help information for the count command """
        print("Counts the current number of instances for a given class")
        print("[Usage]: count <className>\n")

    def do_update(self, args):
        """ Updates a certain object with new info """
        class_name = object_id = attribute_name = attribute_value = kwargs = ''

        # isolate class_name from id/args, ex: (<class_name>, delim, <id/args>)
        args = args.partition(" ")
        if args[0]:
            class_name = args[0]
        else:  # class name not present
            print("** class name missing **")
            return
        if class_name not in HBNBCommand.available_classes:  # class name invalid
            print("** class doesn't exist **")
            return

        # isolate object_id from args
        args = args[2].partition(" ")
        if args[0]:
            object_id = args[0]
        else:  # object id not present
            print("** instance id missing **")
            return

        # generate key from class and id
        key = class_name + "." + object_id

        # determine if key is present
        if key not in storage.all():
            print("** no instance found **")
            return

        # first determine if kwargs or args
        if '{' in args[2] and '}' in args[2] and type(eval(args[2])) is dict:
            kwargs = eval(args[2])
            args = []  # reformat kwargs into list, ex: [<name>, <value>, ...]
            for k, v in kwargs.items():
                args.append(k)
                args.append(v)
        else:  # isolate args
            args = args[2]
            if args and args[0] == '\"':  # check for quoted arg
                second_quote = args.find('\"', 1)
                attribute_name = args[1:second_quote]
                args = args[second_quote + 1:]

            args = args.partition(' ')

            # if attribute_name was not quoted arg
            if not attribute_name and args[0] != ' ':
                attribute_name = args[0]
            # check for quoted val arg
            if args[2] and args[2][0] == '\"':
                attribute_value = args[2][1:args[2].find('\"', 1)]

            # if attribute_value was not quoted arg
            if not attribute_value and args[2]:
                attribute_value = args[2].partition(' ')[0]

            args = [attribute_name, attribute_value]

        # retrieve dictionary of current objects
        new_dict = storage.all()[key]

        # iterate through attribute names and values
        for i, attribute_name in enumerate(args):
            # block only runs on even iterations
            if (i % 2 == 0):
                attribute_value = args[i + 1]  # following item is value
                if not attribute_name:  # check for attribute_name
                    print("** attribute name missing **")
                    return
                if not attribute_value:  # check for attribute_value
                    print("** value missing **")
                    return
                # type cast as necessary
                if attribute_name in HBNBCommand.attribute_types:
                    attribute_value = HBNBCommand.attribute_types[attribute_name](attribute_value)

                # update dictionary with name, value pair
                new_dict.__dict__.update({attribute_name: attribute_value})

        new_dict.save()  # save updates to file

    def help_update(self):
        """ Help information for the update class """
        print("Updates an object with new information")
        print("[Usage]: update <className> <id> <attributeName> <attributeValue>\n")

if __name__ == "__main__":
    HBNBCommand().cmdloop()
