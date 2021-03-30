import os
import sys
import shutil

class FMCore:
    """Core functionality for file manager."""

    def __init__(self):
        self._work_dir = ''
        self._current_dir = ''

    def message(self, *args, **kargs):
        print(*args, file=sys.stdout, **kargs)

    def error(self, *args, **kargs):
        print(*args, file=sys.stderr, **kargs)

    def prompt(self, text):
        return input(text + ' ')

    @property
    def work_dir(self):
        return self._work_dir

    @work_dir.setter
    def work_dir(self, value):
        self._work_dir = value

    @property
    def current_dir(self):
        return self._current_dir

    @current_dir.setter
    def current_dir(self, value):
        self._current_dir = value
        if value:
            os.chdir(value)

    def show_cur_dir(self):
        print(self.current_dir)

    def show_work_dir(self):
        print(self.work_dir)
    
    def change_cur_dir(self, name):
        path = self.__get_abspath(name)

        if not self.__is_under_parent(self.work_dir, path):
            self.error(f"Path {path} is under work directory!",
                f"You can work only inside {self.work_dir}.")
            return 1

        if os.path.isdir(path):
            self.current_dir = path
            self.message(
                f"Current dir was changed to {self.current_dir}.")
        else:
            self.error("Wrong path name, try again.")

    def change_work_dir(self, name):
        path = self.__get_abspath(name)

        if os.path.isdir(path):
            self.work_dir = path
            self.message(
                f"Work dir was changed to {self.work_dir}.")
            self.change_cur_dir(name)
        else:
            self.error("Wrong path name, try again.")

    def create_dir(self, name):
        path = self.__get_abspath(name)

        if not self.__is_under_parent(self.work_dir, path):
            self.error(f"Path {path} is under work directory!",
                f"You can work only inside {self.work_dir}.")
            return 1
            
        parent, child = os.path.split(path)
        if os.path.isdir(parent):
            os.makedirs(path)
            self.message(f"Dir {path} was created.")
        else:
            self.error("Wrong path name, try again.")

    def delete_dir(self, name):
        path = self.__get_abspath(name)

        if not self.__is_under_parent(self.work_dir, path):
            self.error(f"Path {path} is under work directory!",
                f"You can work only inside {self.work_dir}.")
            return 1

        if os.path.isdir(path):
            content = self.__has_content(path)
            if content:
                self.message(f"Dir {path} is not empty.")
                delete = self.prompt(
                    f"Are you sure to delete it? (y/N)").lower()
                if delete == 'y':
                    shutil.rmtree(path)
                    self.message(f"Dir {path} was deleted.")
            else:
                os.rmdir(path)
                self.message(f"Dir {path} was deleted.")
        else:
            self.error("Wrong path name, try again.")

    def create_emptyf(self, name):
        if not name:
            self.error("Wrong file name, try again.")
            return 1

        path = self.__get_abspath(name)

        if not self.__is_under_parent(self.work_dir, path):
            self.error(f"Attempt to create file outside work directory!",
                f"You can work only inside {self.work_dir}.")
            return 1

        with open(path, 'a'):
            os.utime(path, None)
            self.message(f"File {path} was created.")

    def write_to_file(self, name, data):
        if not name:
            self.error("Wrong file name, try again.")
            return 1

        path = self.__get_abspath(name)

        if not self.__is_under_parent(self.work_dir, path):
            self.error(f"Attempt to write to file outside work directory!",
                f"You can work only inside {self.work_dir}.")
            return 1
        
        with open(path, 'w') as file:
            file.write(data)
        self.message(f"Data was written to file {path}.")

    def delete_file(self, name):
        if not name:
            self.error("Wrong file name, try again.")
            return 1

        path = self.__get_abspath(name)

        if not self.__is_under_parent(self.work_dir, path):
            self.error(f"Attempt to delete file outside work directory!",
                f"You can work only inside {self.work_dir}.")
            return 1

        os.remove(path)
        self.message(f"File {path} was deleted.")

    def copy_file(self, name1, name2):
        path1 = self.__get_abspath(name1)
        path2 = self.__get_abspath(name2)

        if path1 == self.current_dir or not os.path.exists(path1):
            self.error("Wrong file name, try again.")
            return 1
        elif path2 == self.current_dir:
            self.error(
                "Specify the name to which you want to copy the file.")
            return 1

        if not self.__is_under_parent(self.work_dir, path1):
            self.error(
                f"Attempt to copy file from outside work directory!",
                f"You can work only inside {self.work_dir}."
            )
            return 1
        elif not self.__is_under_parent(self.work_dir, path2):
            self.error(
                f"Attempt to copy file to outside of work directory!",
                f"You can work only inside {self.work_dir}."
            )
            return 1

        shutil.copy2(path1, path2)
        self.message(f"File {path1} was copied to {path2}.")

    def move_file(self, name1, name2):
        path1 = self.__get_abspath(name1)
        path2 = self.__get_abspath(name2)

        if path1 == self.current_dir or not os.path.exists(path1):
            self.error("Wrong file name, try again.")
            return 1
        elif path2 == self.current_dir:
            self.error(
                "Specify the name to which you want to move the file.")
            return 1

        if not self.__is_under_parent(self.work_dir, path1):
            self.error(
                f"Attempt to move file from outside work directory!",
                f"You can work only inside {self.work_dir}."
            )
            return 1
        elif not self.__is_under_parent(self.work_dir, path2):
            self.error(
                f"Attempt to move file to outside of work directory!",
                f"You can work only inside {self.work_dir}."
            )
            return 1

        shutil.move(path1, path2)
        self.message(f"File {path1} was moved to {path2}.")

    def rename_file(self, name1, name2):
        path1 = self.__get_abspath(name1)
        path2 = self.__get_abspath(name2)

        if path1 == self.current_dir or not os.path.exists(path1):
            self.error("Wrong file name, try again.")
            return 1
        elif path2 == self.current_dir:
            self.error(
                "Specify the name to which you want to rename the file.")
            return 1

        if not self.__is_under_parent(self.work_dir, path1):
            self.error(
                f"Attempt to rename file outside work directory!",
                f"You can work only inside {self.work_dir}."
            )
            return 1
        elif not self.__is_under_parent(self.work_dir, path2):
            self.error(
                f"Attempt to rename file outside of work directory!",
                f"You can work only inside {self.work_dir}."
            )
            return 1

        os.rename(path1, path2)
        self.message(f"File {path1} was renamed to {path2}.")

    def show_content(self, name):
        if not name:
            for i in os.listdir(self.current_dir): 
                print(i, end=' ')
        else:
            for i in os.listdir(name):
                print(i, end=' ')
        print()

    def __has_content(self, name):
        return os.listdir(name)

    def __is_under_parent(self, parent, child):
        """Checks that user make actions under work directory."""

        if parent in child:
            return True
        return False

    def __get_abspath(self, name):
        return os.path.abspath(name)

    def show_help(self):
        message = """
    show_help - show help message
    show_content {name} - show content of directory {name}
    create_dir {name} - create directory {name}
    delete_dir {name} - delete directory {name}
    change_cur_dir {name} - change current directory to {name}
    show_cur_dir {name} - show current directory 
    create_emptyf {name} - create empty file {name}
    write_to_file {name} {data} - write {data} to file {name}
    delete_file {name} - delete file {name}
    copy_file {name1} {name2} - copy file from {name1} to {name2}
    move_file {name1} {name2} - move file from {name1} to {name2}
    rename_file {name1} {name2} - rename file from {name1} to {name2}
    change_work_dir {name} - change work directory
    show_work_dir {name} - show work directory
    quit - exit from program
        """
        print(message)

    def quit(self):
        self.message("Exiting from program.")
        sys.exit(0)
