import zipfile
import shutil
import glob
import os


class Directory:
    def __init__(self, path):
        self.path = path

    def get_path(self):
        return self.path

    def get_name(self):
        return os.path.basename(self.path)

    def get_files(self, extension='*', recursive=False):
        file_list = [File(f) for f in glob.glob(f"{self.path}/*.{extension}") if os.path.isfile(f)]
        if recursive:
            subdirectories = self.get_subdirectories()
            for subdirectory in subdirectories:
                file_list.extend(subdirectory.get_files(extension, recursive))

        return file_list

    def get_text_files(self, extension='*', recursive=False):
        file_list = [TextFile(f) for f in glob.glob(f"{self.path}/*.{extension}") if os.path.isfile(f)]
        if recursive:
            subdirectories = self.get_subdirectories()
            for subdirectory in subdirectories:
                file_list.extend(subdirectory.get_text_files(extension, recursive))

        return file_list

    def get_subdirectories(self):
        return [Directory(d) for d in glob.glob(f"{self.path}/*") if os.path.isdir(d)]

    def get_parent(self):
        return Directory(os.path.dirname(self.path))

    def is_exist(self):
        return os.path.exists(self.path)

    def create(self):
        os.makedirs(self.path)

    def delete(self):
        shutil.rmtree(self.path)
        del self

    def count_files(self, extension='*', recursive=False):
        try:
            cnt = sum(os.path.isfile(f) for f in os.listdir(self.path) if f.endswith(f".{extension}"))
        except:
            cnt = 0

        if recursive:
            subdirectories = self.get_subdirectories()
            for subdirectory in subdirectories:
                cnt += subdirectory.count_files(extension, recursive)

        return cnt

    def exists(self):
        return os.path.exists(self.path)


class File:
    def __init__(self, path: str = None, directory: Directory = None, file_name: str = None):
        if path is None and directory is not None and file_name is not None:
            self.path = f"{directory.get_path()}/{file_name}"
        elif path is not None and directory is None and file_name is None:
            self.path = path
        else:
            raise ValueError('Invalid arguments')

    def get_path(self):
        return self.path

    def get_name(self):
        return os.path.basename(self.path)

    def get_parent(self):
        return Directory(os.path.dirname(self.path))

    def get_extension(self):
        return os.path.splitext(self.path)[1]

    def delete(self):
        os.remove(self.path)
        del self


class TextFile(File):
    def __init__(self, path: str = None, directory: Directory = None, file_name: str = None):
        super().__init__(path, directory, file_name)

        self.text = ''
        try:
            with open(path, 'r', encoding='utf-8') as f:
                self.text = f.read()
        except FileNotFoundError:
            pass

    def get_text(self):
        return self.text

    def set_text(self, text):
        self.text = text

    def append_text(self, text):
        self.text += text

    def save(self):
        with open(self.path, 'w', encoding='utf-8') as f:
            f.write(self.text)


class ZipFile(File):
    def __init__(self, path):
        super().__init__(path=path)
        self.files = []
        with zipfile.ZipFile(path) as existing_zip:
            self.files = existing_zip.namelist()

    def get_files(self):
        return self.files

    def extract_all(self, directory=None):
        with zipfile.ZipFile(self.path) as existing_zip:
            if directory is None:
                existing_zip.extractall(self.get_parent().get_path())
            else:
                existing_zip.extractall(directory)

    def extract(self, file, directory):
        with zipfile.ZipFile(self.path) as existing_zip:
            existing_zip.extract(file, directory)

    def add(self, file: File):
        with zipfile.ZipFile(self.path, 'a') as existing_zip:
            existing_zip.write(file.get_path())
