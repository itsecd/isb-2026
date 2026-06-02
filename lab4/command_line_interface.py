import argparse
import sys
from work_with_hash import calculate_hash, write_hash, read_hash, hash_comparison, clear_hash_file, find_part_collision


def main():
  parser = argparse.ArgumentParser()
  group = parser.add_mutually_exclusive_group(required = True)
  group.add_argument('-s', '--saving', action='store_true', help='1. Starts hash generation and saving mode')
  group.add_argument('-c', '--comparison', action='store_true', help='2. Starts file integrity check mode')
  group.add_argument('-col', '--collision', action='store_true', help='3. Starts partial collision search mode')
  group.add_argument('-cl', '--clear', action='store_true', help='Starts deleting file with hash')
  
  parser.add_argument('-i', '--initial-file', help='path to initial file')
  parser.add_argument('-hf', '--hash-file', default='calculated_hash.txt', help='path to file to save hash')
  parser.add_argument('-pl', '--part-len', default=4, type=int, help='number of characters to search for collision')

  args = parser.parse_args()

  try:
    match (args.saving, args.comparison, args.collision, args.clear):
      case (True, False, False, False):
        print("1. Starts hash generation and saving mode")

        calculated_hash = calculate_hash(args.initial_file)
        print(f"Hash has been calculated: {calculated_hash}")

        write_hash(args.hash_file, calculated_hash)
        print(f"Hash is saved in {args.hash_file}")


      case (False, True, False, False):
        print("2. Starts file integrity check mode")

        result = hash_comparison(args.initial_file, args.hash_file)
        print(f"File {args.initial_file} checked for integrity")

        print("Results of check:\n")
        for key, value in result.items():
          print(f"{key} : {value}")

        if result["comparison"]:
          print(f"File integrity {args.initial_file} confirmed. The file was not modified.")
        else:
          print(f"File integrity {args.initial_file} not confirmed. The file has been changed.")


      case (False, False, True, False):
        print("3. Starts partial collision search mode")

        print(f"Collision detection for number of characters = {args.part_len}")
        result = find_part_collision(args.initial_file, args.part_len)

        print("Results of search:\n")
        for key, value in result.items():
          print(f"{key} : {value}")


      case (False, False, False, True):
        print("Starts deleting file with hash")

        clear_hash_file(args.hash_file)          
        print("Hash file has been deleted")
        
        
      case _:
        print("Error: wrong argument")
            
  except Exception as error:
      print(f"Error has occurred: {error}")

if __name__ == "__main__" :
    main()