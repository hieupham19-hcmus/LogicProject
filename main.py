
from KnowledgeBase import KnowledgeBase
from PL_Resolution import PL_Resolution
from Utilities import read_file

def main():
    KB, alpha = read_file("input.txt")

    f = open("output.txt", "w")
    
    PL = PL_Resolution()
    check = PL.pl_resolution(KB, alpha, f)
    if check == True:
        print("YES")
        f.write("YES")
    else:
        print("NO")
        f.write("NO")
    f.close()

if __name__ == '__main__':
    main()
