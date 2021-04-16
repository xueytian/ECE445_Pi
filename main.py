
import argparse
import pi
from picamera import PiCamera

parser = argparse.ArgumentParser()
parser.add_argument('--table', type=int, help='1 : food, 2 : pic', required=True)
args = parser.parse_args()

table = args.table
if table == 1:
    pi.insert_data(table)
elif table == 2:
    camera = PiCamera()
    species = pi.object_detection(camera)
    print(species)
    pi.insert_data(table, species)
