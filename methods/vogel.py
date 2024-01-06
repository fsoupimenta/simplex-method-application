import numpy as np


class Vogel:
    def __init__(self, matrix):
        self.matrix = matrix
        self.answer = ""
        self.zmax = 0.0

    def calculate_penalty(self):
        new_row = []
        for i, row in enumerate(self.matrix[:-1, :-1].T):
            row_sorted = sorted(row)[:2]
            new_row.append(row_sorted[1] - row_sorted[0])

        new_row.append(0)
        self.matrix = np.vstack((self.matrix, new_row))

        new_column = []
        for i, row in enumerate(self.matrix[:-2, :-1]):
            column_sorted = sorted(row)[:2]
            new_column.append(column_sorted[1] - column_sorted[0])

        new_column.append(0)
        new_column.append(0)
        self.matrix = np.column_stack((self.matrix, new_column))

        print("Matriz Atualizada:")
        print(self.matrix)

    def get_difference_between_lower_costs(self):
        pass

    def get_biggest_difference(self):
        max_value = np.max(self.matrix[-1, :-1])

    def operate_demand_capacity(self, minimum_between):
        pass

    def calculate_min_between_capacity_demand(self, capacity, demand):
        return min(capacity, demand)

    def construct_answer(self, minimum_between, column, row):
        self.answer += \
            ("X-Column:" + str(column) + "-Row:" + str(row) + " = "
             + str(minimum_between) + "\n")

    def construct_zmax(self, minimum_between, cell_value):
        self.zmax += (minimum_between * cell_value)

    def vogel_method(self):
        # antes de chamar novamente o penalty tenho que retirar a ultima linha e coluna da penalidade atual
        temp_matrix = None
        zmax = 0.0

        while True:
            self.calculate_penalty()
            temp_matrix = self.matrix
            max_index_last_row = np.argmax(self.matrix[-1])  # Maior valor da última linha de penalidades
            max_index_last_column = np.argmax(self.matrix[:, -1])  # Maior valor da última coluna de penalidades
            value_last_row = self.matrix[-1, max_index_last_row]
            value_last_column = self.matrix[max_index_last_column, -1]
            minor_value_index = None
            if value_last_column >= value_last_row:
                # opera com last_row
                penalty_line = temp_matrix[max_index_last_column, : -2]
                minor_value_index = np.argmin(penalty_line)

                min_between_capacity_demand = (
                    self.calculate_min_between_capacity_demand(
                        temp_matrix[max_index_last_column, -2], temp_matrix[-2, minor_value_index]))

                self.matrix[max_index_last_column, -2] -= min_between_capacity_demand
                self.matrix[-2, minor_value_index] -= min_between_capacity_demand
                self.construct_answer(min_between_capacity_demand, max_index_last_row, minor_value_index)
                self.construct_zmax(min_between_capacity_demand, temp_matrix[minor_value_index, max_index_last_row])

                print(self.matrix)

            else:
                # operar com colunas
                penalty_column = temp_matrix[:-2, max_index_last_row]
                minor_value_index = np.argmin(penalty_column)

                min_between_capacity_demand = (
                    self.calculate_min_between_capacity_demand(
                        temp_matrix[-2, max_index_last_row], temp_matrix[minor_value_index, -2]))

                self.matrix[-2, max_index_last_row] -= min_between_capacity_demand
                self.matrix[minor_value_index, -2] -= min_between_capacity_demand
                self.construct_answer(min_between_capacity_demand, max_index_last_row, minor_value_index)
                self.construct_zmax(min_between_capacity_demand, temp_matrix[minor_value_index, max_index_last_row])
                print(self.matrix)


            self.matrix = self.matrix[:-1, :-1]  # Tirar colunas de penalidade

            # if else para verificar se a capacidade ou demanda está zerada para remover a linha e/ou coluna
            if self.matrix[-1, max_index_last_row] == 0:
                self.matrix = np.delete(self.matrix, max_index_last_row, axis=1)
            if self.matrix[minor_value_index, -1] == 0:
                self.matrix = np.delete(self.matrix, minor_value_index, axis=0)

            # Lógica final para caso tenha apenas uma linha ou coluna restante
            if self.matrix.shape[0] <= 2:  # menos ou 2 linhas
                for column in range(len(self.matrix[0]) - 1):
                    min_between_capacity_demand = (
                        self.calculate_min_between_capacity_demand(self.matrix[0, -1], self.matrix[1, column]))
                    self.construct_answer(min_between_capacity_demand, column, 0)
                    self.construct_answer(min_between_capacity_demand, column, 1)
                    self.construct_zmax(min_between_capacity_demand, self.matrix[0, column])

                    # zmax += (self.matrix[1, column] * self.matrix[0, column])
                    # answer += \
                    #     ("X-Column:" + str(column) + "-Row:" + str(0) + " = "
                    #      + str(self.matrix[0, column]) + "\n")
                    # answer += \
                    #     ("X-Column:" + str(column) + "-Row:" + str(1) + " = "
                    #      + str(self.matrix[1, column]) + "\n")
                print(self.zmax)
                print(self.answer)
                print("Matrix final")
                print(self.matrix)
                break
            elif self.matrix.shape[1] <= 2:
                print("em desenvolvimento")
                break
            print(self.matrix)
            print("Fim do ciclo")
