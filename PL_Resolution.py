from Utilities import write_file


class PL_Resolution:
    def pl_resolution(self, knowledge_base, alpha, file_pointer):
        self._create_resolution_sentence(knowledge_base, alpha)
        clauses = knowledge_base.sentences
        clauses_new = clauses

        while True:
            new_clauses = []
            check = False
            for clause1 in clauses_new:
                for clause2 in clauses:
                    if equal(clause1, clause2) == 0:
                        resolvent = self._pl_solve(clause1, clause2)
                        if len(resolvent) != 0:
                            if _contain_empty(resolvent) == 1:
                                check = True
                            new_clauses = union(new_clauses, [resolvent])

            clauses_new = diff(clauses, new_clauses)
            write_file(file_pointer, clauses_new)
            if check:
                return True

            if len(clauses_new) == 0:
                return False
            clauses = union(clauses, new_clauses)

    def _create_resolution_sentence(self, knowledge_base, alpha):
        """
        Add negative of alpha in to knowledge_base
        """
        temp = alpha
        if "-" in temp:
            temp = temp.replace("-", "")
        else:
            temp = "-" + temp
        knowledge_base.add_sentence(temp)

    def _pl_solve(self, clause1, clause2):
        result = []
        check = 0
        lst1 = clause1.copy()
        lst2 = clause2.copy()
        len1 = len(lst1)
        len2 = len(lst2)
        for i in range(len1):
            for j in range(len2):
                if ((lst1[i] in lst2[j]) or (lst2[j] in lst1[i])) and lst1[i] != lst2[j]:
                    check += 1
                    if check > 1:
                        return result
                    idx1 = i
                    idx2 = j
                    break
        if check == 1:
            del lst1[idx1]
            del lst2[idx2]
            result = add_sentence(lst1, lst2)
            if len(result) == 0:
                result.append("{}")
        del lst1
        del lst2
        return result


def _contain_empty(lst):
    for ele in lst:
        if ele == "{}":
            return 1
    return 0


def sub_list(lst1, lst2):
    """
    return lst1 is sublist(lst2)
    """
    if (len(lst1) != 0 and len(lst2) != 0):
        for ele1 in lst1:
            for ele2 in lst2:
                if equal(ele1, ele2) == 0:
                    return False
    return True


def union(lst1, lst2):
    """
    union of two lists
    """
    for ele in lst2:
        if not_in(ele, lst1):
            lst1.append(ele)
    return lst1


def equal(clause1, clause2):
    if len(clause1) == len(clause2):
        for ele in clause1:
            if not (ele in clause2):
                return 0
        return 1
    return 0


def not_in(ele, lst):
    for ele1 in lst:
        if equal(ele, ele1):
            return 0
    return 1


def add_sentence(clause1, clause2):
    result = clause1
    for ele in clause2:
        if not ele in clause1:
            result.append(ele)
    return result


def diff(lst1, lst2):
    result = []
    for ele in lst2:
        if not_in(ele, lst1):
            result.append(ele)
    return result
