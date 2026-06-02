import unittest
import shutil
import os
import hashlib
import hashing

class HashModuleTests(unittest.TestCase):
    def test_serialize(self):
        data = b"sample text!"
        path = "./temp/data.txt" # arrange 

        hashing.serialize(path, data) # act

        with open(path, mode="rb") as f:
            file_data = f.read()

        self.assertEqual(data, file_data) # assert
    

    def test_deserialize(self):
        data = b"something"
        path = "./temp/data_2.txt"

        if not os.path.exists("./temp"):
            os.mkdir("./temp")

        with open(path, mode="wb") as f:
            f.write(data)
        
        res = hashing.deserialize(path)
        self.assertEqual(data, res)
    

    def test_serialize_deserialize(self):
        data = b"my generic binary string"
        path = "./temp/string.txt"
        hashing.serialize(path, data)

        res = hashing.deserialize(path)

        self.assertEqual(data, res)


    def test_get_file_hash_sha256(self):
        data = b"hashable"
        hash = hashlib.sha256(data).hexdigest()

        res = hashing.get_file_hash(data, "sha256")
        self.assertEqual(hash, res)


    def test_get_file_hash_md5(self):
        data = b"hashable"
        hash = hashlib.md5(data).hexdigest()

        res = hashing.get_file_hash(data, "md5")
        self.assertEqual(hash, res)


    def test_load_checksums_empty(self):
        path = "./this/path/does/not/exists/file.json"

        res = hashing.load_checksums({"hash_db_path": path})

        self.assertDictEqual(dict(), res)
    

    def test_load_checksums_empty(self):
        path = "./temp/json.json"
        data = { "key": "value" }
        json_string = str(data).replace("'", '"').encode("UTF-8")

        if not os.path.exists("./temp"):
            os.mkdir("./temp")

        with open(path, mode="wb") as f:
            f.write(json_string)
        
        res =  hashing.load_checksums({"hash_db_path": path})

        self.assertDictEqual(data, res)


    def tearDownClass():
        shutil.rmtree("./temp")

if __name__ == "__main__":
    unittest.main()