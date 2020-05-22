import random;


class mastermind(object):

    def __init__(self, nb_colors=6, combination_length=4, max_tries=12):
        self.nb_colors = nb_colors;
        self.combination_length = combination_length;
        self.max_tries = max_tries;
        self.combination = [0 for _ in range(combination_length)];
        self.str_game_state = "";
        self.current_nb_tries = 0;
        self.rst();


    def rst(self):
        self.str_game_state = "*Mastermind* \n Nombre d'Essais: {} ; Nombre de Couleurs: {}. \n".format(self.max_tries, self.nb_colors);
        self.combination = [random.randint(0, self.combination_length-1)];
        self.combination = [0,1,1,2]
        self.current_nb_tries = 0;

    def check_proposition_consistency(self, str_solution):
        array_proposition = [];
        ## Check Solution Consistency
        if str_solution[0] == "(" and str_solution[-1] == ")":
            str_solution = str_solution[1:-1] # remove brackets
            array_proposition = str_solution.split(",");
            if len(array_proposition) == self.combination_length:
                array_proposition = [int(i) for i in array_proposition]; # conversion to int array.
                for i in array_proposition:
                    if i >= self.nb_colors:
                        array_proposition = [];
                        break;
            else:
                array_proposition = [] ;
        return array_proposition;

    # Takes as Input "array_proposition"
    def compare_proposition_with_solution(self, array_proposition):
        right_pos = 0;
        right_col = 0;
        combination = self.combination.copy();
        for i in range(self.combination_length):
            if array_proposition[i] == combination[i]:
                right_pos +=1 ;
                combination[i], array_proposition[i] = -1, -1;
        for i in range(self.combination_length):
            if array_proposition[i] != -1:
                if array_proposition[i] in combination:
                    right_col +=1 ;
                    indx = combination.index(array_proposition[i]);
                    combination[indx] = -1;
        return (right_pos, right_col);


    def propose(self, str_proposition):
        ret = "";
        array_proposition = self.check_proposition_consistency(str_proposition);
        if array_proposition:
            (right_pos, right_col) = self.compare_proposition_with_solution(array_proposition);
            self.str_game_state += str(self.current_nb_tries) +". " + str_proposition + " " +right_pos*'O'+right_col*'X' + (self.combination_length-right_col-right_pos)*'_'+'\n'
            self.current_nb_tries += 1;
            if right_pos == self.combination_length:
                self.str_game_state += "Bravo, Vous avez gagné !\n"
            else:
                if self.current_nb_tries == self.max_tries:
                    return "Oh non ! Vous avez manqué de perspicacité !\n"
                    self.rst();
            ret = self.str_game_state;

        return ret[:-1];



if __name__ == "__main__":
    mastermind_inst = mastermind();
    mastermind_inst.combination = [0,1,1,2];
    while(True):
        proposition = input();
        cmp = mastermind_inst.propose(proposition);
        print(cmp);
