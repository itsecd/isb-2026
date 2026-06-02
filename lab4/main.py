import sys
import command_line_interface
import graphical_interface

def main():
  """
  определяет режим запуска:
  если переданы аргументы командной строки, запускается command_line_interface, иначе - graphical_interface

  arguments: -
  return: -
  """

  try:
    if len(sys.argv) > 1:
      command_line_interface.main()
    else:
      graphical_interface.main()
      
  except Exception as error:
      print(f"Error has occurred: {error}")
      sys.exit(1)

if __name__ == "__main__":
  main()