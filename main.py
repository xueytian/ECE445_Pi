
import argparse
import pi

parser = argparse.ArgumentParser()
parser.add_argument('--table', type=int, help='1 : food, 2 : pic', required=True)
args = parser.parse_args()

table = args.table
if table == 1:
    pi.insert_data(table)
elif table == 2:
    species = pi.object_detection()
    print(species)
    pi.insert_data(table, species)