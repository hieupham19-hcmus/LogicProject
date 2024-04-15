class PLResolution:
    @staticmethod
    def _add_negated_alpha_to_kb(knowledge_base, alpha) -> None:
        """
        Add the negation of alpha into knowledge base.
        """
        if "-" in alpha:
            negated_alpha = alpha.replace("-", "")
        else:
            negated_alpha = "-" + alpha

        if not any(set(clause) == set(negated_alpha.split()) for clause in knowledge_base.sentences):
            knowledge_base.add_sentence(negated_alpha)

    @staticmethod
    def _write_file(f, list):
        """
        Write list of clauses to the output file.
        """
        f.write(str(len(list)) + "\n")
        for item in list:
            f.write(" OR ".join(item) + "\n")

    @staticmethod
    def _contains_empty(list) -> bool:
        """
        Check if the list contains an empty clause.
        """
        return "{}" in list

    @staticmethod
    def _equal(clause1, clause2) -> bool:
        """
        Check if two clauses are equal.
        """
        return set(clause1) == set(clause2)

    def _diff(self, list1, list2) -> list:
        """
        Find the difference between two lists of clauses.
        """
        return [element for element in list2 if self._is_not_in_list(element, list1)]

    def _is_not_in_list(self, element, list) -> bool:
        """
        Check if element is not in the list of clauses.
        """
        return all(not self._equal(element, tmp) for tmp in list)

    def _merge_lists(self, list1, list2) -> list:
        """
        Merge two lists of clauses, removing duplicates.
        """
        for element in list2:
            if self._is_not_in_list(element, list1):
                list1.append(element)
        return list1

    @staticmethod
    def _add_sentence(clause1, clause2) -> list:
        """
        Add two clauses together.
        """
        combined_clause = list(clause1)
        result_set = set(tuple(subclause) for subclause in clause1)

        for element in clause2:
            elements_tuple = tuple(element)
            if elements_tuple not in result_set:
                combined_clause.append(element)
                result_set.add(elements_tuple)

        return combined_clause

    @staticmethod
    def _is_always_right(clause) -> bool:
        """
        Check if a clause is always true.
        """
        literals = set()
        negations = set()

        for literal in clause:
            if literal.startswith("-"):
                negations.add(literal[1:])
            else:
                literals.add(literal)

        # Check for contradiction (A AND -A)
        if any(lit in negations for lit in literals):
            return False

        # Check if there's any literal that makes the clause always true (A OR -A OR anything_else)
        if any(lit not in literals and lit not in negations for lit in literals.union(negations)):
            return True

        return False

    def _resolve_clauses(self, clause1, clause2) -> list:
        """
        Resolve two clauses to derive a new clause.
        """
        matches = 0
        for i, literal1 in enumerate(clause1):
            for j, literal2 in enumerate(clause2):
                if (literal1 == "-" + literal2) or (literal2 == "-" + literal1):
                    matches += 1
                    if matches > 1:
                        return []
                    index1, index2 = i, j
                    break

        if matches == 1:
            list1 = clause1[:index1] + clause1[index1 + 1:]
            list2 = clause2[:index2] + clause2[index2 + 1:]
            result = self._add_sentence(list1, list2)

            # Check if the resolvent contains contradictory literals
            for literal in result:
                if literal.startswith("-") and literal[1:] in result:
                    return []

            # Sort the result alphabetically, ignoring negations
            result.sort(key=lambda x: x[1:] if x.startswith("-") else x)

            if not result:
                result.append("{}")
            return result
        return []

    def pl_resolution(self, knowledge_base, alpha, output_file: str) -> bool:
        """
        Perform PL resolution.
        """
        try:
            with open(output_file, "w") as file_pointer:
                self._add_negated_alpha_to_kb(knowledge_base, alpha)
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
                        return True

                    if not clauses_new:
                        file_pointer.write("NO")
                        return False

                    clauses = self._merge_lists(clauses, new_clauses)

        except IOError:
            print("Could not open file!!!")
            return False
