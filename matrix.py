import math
from math import sqrt
import numbers


def zeroes(height, width):
    """
        Creates a matrix of zeroes.
        """
    g = [[0.0 for _ in range(width)] for __ in range(height)]
    return Matrix(g)


def identity(n):
    """
        Creates a n x n identity matrix.
        """
    I = zeroes(n, n)
    for i in range(n):
        I.g[i][i] = 1.0
    return I


def get_row(matrix, row):
    return matrix[row]


def get_column(matrix, column_number):
    column = []
    for r in range(len(matrix)):
        column.append(matrix[r][column_number])

    return column


def dot_product(vector_one, vector_two):
    result = 0
    for i in range(len(vector_one)):
        result += vector_one[i] * vector_two[i]

    return result


class Matrix(object):

    # Constructor
    def __init__(self, grid):
        self.g = grid
        self.h = len(grid)
        self.w = len(grid[0])

    #
    # Primary matrix math methods
    #############################

    def determinant(self):
        """
        Calculates the determinant of a 1x1 or 2x2 matrix.
        """
        if not self.is_square():
            raise (ValueError, "Cannot calculate determinant of non-square matrix.")
        if self.h > 2:
            raise (NotImplementedError, "Calculating determinant not implemented for matrices largerer than 2x2.")

        if self.h == 1:
            return self.g[0]

        elif self.h == 2:
            return (self.g[0][0] * self.g[1][1]) - (self.g[0][1] * self.g[1][0])

    def trace(self):
        """
        Calculates the trace of a matrix (sum of diagonal entries).
        """
        if not self.is_square():
            raise (ValueError, "Cannot calculate the trace of a non-square matrix.")

        sum1 = 0
        if self.h == 1:
            return Matrix(self.g[0])
        else:
            for i in range(len(self.g)):
                for j in range(len(self.g[i])):
                    if i == j:
                        sum1 = sum1 + self.g[i][j]
            return sum1

    def inverse(self):
        """
        Calculates the inverse of a 1x1 or 2x2 Matrix.
        """
        if not self.is_square():
            raise (ValueError, "Non-square Matrix does not have an inverse.")
        if self.h > 2:
            raise (NotImplementedError, "inversion not implemented for matrices larger than 2x2.")

        inver = []
        if self.h == 1:
            one_by = 1 / self.g[0][0]
            inver.append([one_by])
            return Matrix(inver)

        elif self.h == 2:
            deter = self.determinant()
            trace1 = self.trace()
            ident = identity(self.h)
            return (1 / deter) * ((trace1 * ident) - self.g)

    def T(self):
        """
        Returns a transposed copy of this Matrix.
        """
        if self.h == 1:
            return self.g

        elif self.h == 2:
            transpose = []
            for i in range(len(self.g[0])):
                row = []
                for j in range(len(self.g)):
                    row.append(self.g[j][i])
                transpose.append(row)
            return Matrix(transpose)

    def is_square(self):
        return self.h == self.w

    #
    # Begin Operator Overloading
    ############################
    def __getitem__(self, idx):
        """
        Defines the behavior of using square brackets [] on instances
        of this class.

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > my_matrix[0]
          [1, 2]

        > my_matrix[0][0]
          1
        """
        return self.g[idx]

    def __repr__(self):
        """
        Defines the behavior of calling print on an instance of this class.
        """
        s = ""
        for row in self.g:
            s += " ".join(["{} ".format(x) for x in row])
            s += "\n"
        return s

    def __add__(self, other):
        """
        Defines the behavior of the + operator
        """
        if self.h != other.h or self.w != other.w:
            raise (ValueError, "Matrices can only be added if the dimensions are the same")

        Sum = []
        for i in range(len(self.g)):
            row = []
            for j in range(len(self.g[i])):
                row.append(self.g[i][j] + other[i][j])
            Sum.append(row)

        return Matrix(Sum)

    def __neg__(self):
        """
        Defines the behavior of - operator (NOT subtraction)

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > negative  = -my_matrix
        > print(negative)
          -1.0  -2.0
          -3.0  -4.0
        """
        Neg = []
        for i in range(len(self.g)):
            row = []
            for j in range(len(self.g[0])):
                row.append(-1 * self.g[i][j])
            Neg.append(row)

        return Matrix(Neg)

    def __sub__(self, other):
        """
        Defines the behavior of - operator (as subtraction)
        """
        Sub = []

        for i in range(len(self.g)):
            row = []
            for j in range(len(self.g[0])):
                row.append(self.g[i][j] - other[i][j])
            Sub.append(row)

        return Matrix(Sub)

    def __mul__(self, other):
        """
        Defines the behavior of * operator (matrix multiplication)
        """
        m_rows = len(self.g)
        p_columns = len(other.g[0])

        result = []
        for i in range(m_rows):
            row_result = []
            rowA = get_row(self.g, i)
            for j in range(p_columns):
                colB = get_column(other.g, j)
                dot_prod = dot_product(rowA, colB)
                row_result.append(dot_prod)
            result.append(row_result)

        return Matrix(result)

    def __rmul__(self, other):
        """
        Called when the thing on the left of the * is not a matrix.

        Example:

        > identity = Matrix([ [1,0], [0,1] ])
        > doubled  = 2 * identity
        > print(doubled)
          2.0  0.0
          0.0  2.0
        """
        if isinstance(other, numbers.Number):

            scalar_multiply = []
            for i in range(len(self.g)):
                row = []
                for j in range(len(self.g[0])):
                    row.append(other * self.g[i][j])
                scalar_multiply.append(row)

            return Matrix(scalar_multiply)
