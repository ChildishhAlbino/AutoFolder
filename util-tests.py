from utils import unzip, convert, rename, delete
import shutil
import unittest
from os import remove, removedirs
from os.path import exists


class ZipTest(unittest.TestCase):

    def setup(self):
        try:
            remove("./test.txt")
            remove("./test.zip")
            shutil.rmtree("./test")
        except Exception as E:
            print(E)

        with open("./test.txt", "w") as f:
            f.write("12345")

        shutil.make_archive("test", 'zip', "./", "./test.txt")
        remove("./test.txt")

    def test_A_unzip(self):
        self.setup()
        unzip(".\\test.zip", False, False)

        with open("./test.txt") as f:
            data = f.read()

        self.assertEqual(data, "12345", "Data from file should equal 12345")

    def test_B_unzip(self):
        self.setup()
        unzip(".\\test.zip", True, False)

        with open("./test.txt") as f:
            data = f.read()

        self.assertEqual(data, "12345", "Data from file should equal 12345")
        self.assertEqual(exists("./test.zip"), False,
                         "Archive should be deleted.")

    def test_C_unzip(self):
        self.setup()
        unzip(".\\test.zip", False, True)

        with open("./test/test.txt") as f:
            data = f.read()

        self.assertEqual(data, "12345", "Data from file should equal 12345")
        shutil.rmtree("./test")
        remove("./test.zip")


if __name__ == '__main__':
    unittest.main()
