import unittest
from missense import missense as ms
import tempfile
import os
import hashlib

class MyTest(unittest.TestCase):

    def calc_hash(self, filename):
        with open(filename, "rb") as f:
            bytes = f.read()  # read file as bytes
            readable_hash = hashlib.md5(bytes).hexdigest();
            return readable_hash

    def test_pdf_and_and_are_generated(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            ms._run(uniprot_id="Q9UQ13",
                    output_path=tmpdirname,
                    maxacid=200,
                    pdbpath=None
                    )

            self.assertEqual(True, os.path.exists(os.path.join(tmpdirname,"Q9UQ13.pdf")))
            self.assertEqual(True, os.path.exists(os.path.join(tmpdirname, "Q9UQ13-edit.pdb")))

    def test_pdb_check_with_reference(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            ms._run(uniprot_id="Q9UQ13",
                    output_path=tmpdirname,
                    maxacid=200,
                    pdbpath=None
                    )

            ref_pth = os.path.join(os.path.dirname(__file__), "../resources/tests/Q9UQ13/Q9UQ13-edit.pdb")
            new_pth = os.path.join(os.path.join(tmpdirname, "Q9UQ13-edit.pdb"))
            ref_hash = self.calc_hash(ref_pth)
            new_hash = self.calc_hash(new_pth)

            self.assertTrue( ref_hash == new_hash)

    def test_pdb_check_with_reference_with_pdb(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            ms._run(uniprot_id="Q9UQ13",
                    output_path=tmpdirname,
                    maxacid=200,
                    pdbpath=os.path.join(os.path.dirname(__file__), "../resources/tests/Q9UQ13-with-pdb/7upi.pdb")
                    )

            ref_pth = os.path.join(os.path.dirname(__file__), "../resources/tests/Q9UQ13-with-pdb/Q9UQ13-edit.pdb")
            new_pth = os.path.join(os.path.join(tmpdirname, "Q9UQ13-edit.pdb"))
            ref_hash = self.calc_hash(ref_pth)
            new_hash = self.calc_hash(new_pth)

            self.assertTrue( ref_hash == new_hash)





if __name__ == '__main__':
    unittest.main()