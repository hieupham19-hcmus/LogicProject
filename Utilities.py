from KnowledgeBase import KnowledgeBase


def read_file(file):
    try:
        with open(file, "r") as f:
            alpha = f.readline().rstrip("\n")
            length_kb = int(f.readline())
            KB = KnowledgeBase()
            for _ in range(length_kb):
                KB.add_sentence(f.readline().rstrip("\n"))
            f.close()
        return KB, alpha
    except IOError:
        print("Could not open file!!!")
        return None, None
