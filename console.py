#!/usr/bin/python3
'''
    Implementing the console for the HBnB project.
'''
import cmd
import json
import shlex
from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
import models

class HBNBCommand(cmd.Cmd):
    '''
        Contains the entry point of the command interpreter.
    '''

    prompt = ("(hbnb) ")

    def do_quit(self, args):
        '''
            Quit command to exit the program.
        '''
        return True

    def do_EOF(self, args):
        '''
            Exits after receiving the EOF signal.
        '''
        return True

    def do_create(self, args):
        '''
            Create a new instance of class BaseModel and saves it
            to the JSON file.
        '''
        if len(args) == 0:
            print("** class name missing **")
            return
        elif len(args) == 1:
            try:
                args = shlex.split(args)
                class_name = args[0]
                new_instance = eval(class_name)()
                new_instance.save()
                print(new_instance.id)

            except:
                print("** class doesn't exist **")
        else:
            try:
                args = shlex.split(args)
                class_name = args.pop(0)
                obj = eval(class_name)()
                for arg in args:
                    attribute, value = arg.split('=')
                    if hasattr(obj, attribute):
                        try:
                            value = eval(value)
                        except:
                            value = value.replace('_',' ')
                        setattr(obj, attribute, value)

                obj.save()
            except:
                return
            print(obj.id)

    def do_show(self, args):
        '''
            Print the string representation of an instance based on
            the class name and id given as args.
        '''
        args = shlex.split(args)
        if len(args) == 0:
            print("** class name missing **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return

        models.storage.reload()
        objects_dict = models.storage.all()
        try:
            class_to_show = eval(args[0])
        except NameError:
            print("** class doesn't exist **")
            return

        instance_key = args[0] + "." + args[1]
        try:
            instance_value = objects_dict[instance_key]
            print(instance_value)
        except KeyError:
            print("** no instance found **")

    def do_destroy(self, args):
        '''
            Deletes an instance based on the class name and id.
        '''
        args = shlex.split(args)
        if len(args) == 0:
            print("** class name missing **")
            return
        elif len(args) == 1:
            print("** instance id missing **")
            return

        class_name = args[0]
        class_id = args[1]

        models.storage.reload()
        objects_dict = models.storage.all()
        try:
            class_to_destroy = eval(class_name)
        except NameError:
            print("** class doesn't exist **")
            return

        instance_key = class_name + "." + class_id
        try:
            del objects_dict[instance_key]
        except KeyError:
            print("** no instance found **")
        models.storage.save()

    def do_all(self, args):
        '''
            Prints all string representation of all instances
            based or not on the class name.
        '''
        instances_list = []

        models.storage.reload()
        all_objects = models.storage.all()
        try:
            if len(args) != 0:
                class_to_filter = eval(args)
        except NameError:
            print("** class doesn't exist **")
            return

        for key, instance in all_objects.items():
            if len(args) != 0:
                if isinstance(instance, class_to_filter):
                    instances_list.append(instance)
            else:
                instances_list.append(instance)

        print(instances_list)

    def do_update(self, args):
        '''
            Update an instance based on the class name and id
            sent as args.
        '''
        models.storage.reload()
        args = shlex.split(args)
        if len(args) == 0:
            print("** class name missing **")
            return
        elif len(args) == 1:
            print("** instance id missing **")
            return
        elif len(args) == 2:
            print("** attribute name missing **")
            return
        elif len(args) == 3:
            print("** value missing **")
            return

        try:
            class_to_update = eval(args[0])
        except NameError:
            print("** class doesn't exist **")
            return

        instance_key = args[0] + "." + args[1]
        objects_dict = models.storage.all()
        try:
            instance_value = objects_dict[instance_key]
        except KeyError:
            print("** no instance found **")
            return

        try:
            attribute_type = type(getattr(instance_value, args[2]))
            args[3] = attribute_type(args[3])
        except AttributeError:
            pass

        setattr(instance_value, args[2], args[3])
        instance_value.save()

    def emptyline(self):
        '''
            Prevents printing anything when an empty line is passed.
        '''
        pass

    def do_count(self, args):
        '''
            Counts/retrieves the number of instances.
        '''
        instances_list = []

        models.storage.reload()
        all_objects = models.storage.all()
        try:
            if len(args) != 0:
                class_to_count = eval(args)
        except NameError:
            print("** class doesn't exist **")
            return

        for key, instance in all_objects.items():
            if len(args) != 0:
                if isinstance(instance, class_to_count):
                    instances_list.append(instance)
            else:
                instances_list.append(instance)

        print(len(instances_list))

    def default(self, args):
        '''
            Catches all the function names that are not explicitly defined.
        '''
        functions = {"all": self.do_all, "update": self.do_update,
                     "show": self.do_show, "count": self.do_count,
                     "destroy": self.do_destroy, "update": self.do_update}
        args = (args.replace("(", ".").replace(")", ".")
                .replace('"', "").replace(",", "").split("."))

        try:
            command_argument = args[0] + " " + args[2]
            function_to_call = functions[args[1]]
            function_to_call(command_argument)
        except:
            print("*** Unknown syntax:", args[0])

if __name__ == "__main__":
    '''
        Entry point for the loop.
    '''
    HBNBCommand().cmdloop()

