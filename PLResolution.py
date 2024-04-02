class PLResolution:
    def __init__(self, output_file=None):
        self.output_file = output_file

    @staticmethod
    def _create_resolution_sentence(knowledge_base, alpha) -> None:
        """
        Add negative of alpha in to knowledge_base
        """
        temp = alpha
        if "-" in temp:
            temp = temp.replace("-", "")
        else:
            temp = "-" + temp
        knowledge_base.add_sentence(temp)

    @staticmethod
    def _write_file(f, lst):
        f.write(str(len(lst)) + "\n")
        for item in lst:
            f.write(" OR ".join(item) + "\n")

    def pl_resolution(self, knowledge_base, alpha, output_file: str) -> bool:
        try:
            file_pointer = open(output_file, "w")
        except IOError:
            print("Could not open file!!!")
            return False

        self._create_resolution_sentence(knowledge_base, alpha)
        clauses = knowledge_base.sentences
        clauses_new = clauses

        while True:
            new_clauses = []
            check = False
            for clause1 in clauses_new:
                for clause2 in clauses:
                    if self._equal(clause1, clause2) == 0:
                        resolvent = self._resolve_clauses(clause1, clause2)
                        if len(resolvent) != 0:
                            if self._contains_empty(resolvent) == 1:
                                check = True
                            new_clauses = self._merge_lists(new_clauses, [resolvent])

            clauses_new = self._diff(clauses, new_clauses)
            self._write_file(file_pointer, clauses_new)
            if check:
                file_pointer.write("YES")
                file_pointer.close()
                return True

            if len(clauses_new) == 0:
                file_pointer.write("NO")
                file_pointer.close()
                return False

            clauses = self._merge_lists(clauses, new_clauses)

    def _resolve_clauses(self, clause1, clause2) -> list:
        """
        Resolve two clauses to derive a new clause.
        """
        global index1, index2
        result = []
        matches = 0
        length1 = len(clause1)
        length2 = len(clause2)
        for i in range(length1):
            for j in range(length2):
                if (clause1[i] in clause2[j] or clause2[j] in clause1[i]) and clause1[i] != clause2[j]:
                    matches += 1
                    if matches > 1:
                        return result
                    index1 = i
                    index2 = j
                    break
        if matches == 1:
            lst1 = clause1[:index1] + clause1[index1 + 1:]
            lst2 = clause2[:index2] + clause2[index2 + 1:]
            result = self._add_sentence(lst1, lst2)
            if not result:
                result.append("{}")
        return result

    @staticmethod
    def _contains_empty(lst) -> bool:
        for ele in lst:
            if ele == "{}":
                return True
        return False

    @staticmethod
    def _is_sublist(list1, list2) -> bool:
        if len(list1) == 0:
            return True
        if len(list1) > len(list2):
            return False

        for i in range(len(list2) - len(list1) + 1):
            if list2[i:i + len(list1)] == list1:
                return True

        return False

    def _merge_lists(self, list1, list2) -> list:
        for element in list2:
            if self._is_not_in_list(element, list1):
                list1.append(element)
        return list1

    @staticmethod
    def _equal(clause1, clause2) -> bool:
        if len(clause1) == len(clause2):
            for element in clause1:
                if not (element in clause2):
                    return False
            return True
        return False

    def _is_not_in_list(self, ele, lst) -> bool:
        for ele1 in lst:
            if self._equal(ele, ele1):
                return False
        return True

    @staticmethod
    def _add_sentence(clause1, clause2) -> list:
        combined_clause = list(clause1)
        result_set = set(tuple(subclause) for subclause in clause1)

        for ele in clause2:
            ele_tuple = tuple(ele)
            if ele_tuple not in result_set:
                combined_clause.append(ele)
                result_set.add(ele_tuple)

        return combined_clause

    def _diff(self, lst1, lst2) -> list:
        differences = []
        for ele in lst2:
            if self._is_not_in_list(ele, lst1):
                differences.append(ele)
        return differences
