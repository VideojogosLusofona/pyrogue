"""2d vector class and helper functions 
Adapted from PyXYZ (https://github.com/VideojogosLusofona/PyXYZ)
"""
import math

class InvalidOperationException(Exception):
    """Exception thrown when there's an invalid operation with vectors"""
    def __init__(self, op, type1, type2):
        super().__init__(self)
        self.op = op
        self.type1 = type1
        self.type2 = type2

    def __str__(self):
        """Returns a readable version of the exception"""
        return f"Invalid operation ({self.op}) between {self.type1} and {self.type2}!"

class Vector2:
    """2d vector class.
    It stores XY values as floats."""

    def __init__(self, x=0, y=0):
        if isinstance(x, tuple):
            self.x = x[0]
            self.y = x[1]
        elif isinstance(x, Vector2):
            self.x = x.x
            self.y = x.y
        else:
            self.x = x
            self.y = y

    def __str__(self):
        """Converts the 2d vector to a displayable string
        Returns:
            String - Vector in text format (x,y)"""
        return f"({self.x},{self.y})"

    def __add__(self, v):
        """Adds this Vector2 to another.
        If we try to add anything other than a Vector2 to it, it throws the
        InvalidOperationException.
        Arguments:
            v {Vector2} -- Vector to add
        Returns:
            Vector2 - Sum of this Vector2 and the given one
        """
        if isinstance(v, Vector2):
            return Vector2(self.x + v.x, self.y + v.y)
        else:
            raise InvalidOperationException("add", type(self), type(v))

    def __sub__(self, v):
        """Subtracts a Vector2 from this one.
        If we try to subtract anything other than a Vector2, it throws the
        InvalidOperationException.
        Arguments:
            v {Vector2} -- Vector to subtract
        Returns:
            Vector2 - Subraction of the given vector from this one
        """
        if isinstance(v, Vector2):
            return Vector2(self.x - v.x, self.y - v.y)
        else:
            raise InvalidOperationException("sub", type(self), type(v))

    def __mul__(self, v):
        """Multiplies this Vector2 by a scalar or a Vector2.
        Multiplication of two vector2 values does a piecewise multiplication of the 
        components.
        Arguments:
            v {number/Vector2} -- Other element to multiply
        Returns:
            Vector2 - Multiplication of the Vector2
        """
        if isinstance(v, (int, float)):
            return Vector2(self.x * v, self.y * v)
        elif isinstance(v, (Vector2)):
            return Vector2(self.x * v.x, self.y * v.y)
        else:
            raise InvalidOperationException("mult", type(self), type(v))

    def __rmul__(self, v):
        """Multiplies this Vector2 by a scalar or a Vector2
        Multiplication of two vector2 values does a piecewise multiplication of the 
        components.
        Arguments:
            v {number/Vector2} -- Other element to multiply
            this number
        Returns:
            Vector2 - Multiplication of the Vector2
        """
        if isinstance(v, (int, float)):
            return Vector2(self.x * v, self.y * v)
        elif isinstance(v, (Vector2)):
            return Vector2(self.x * v.x, self.y * v.y)
        else:
            raise InvalidOperationException("mult", type(self), type(v))

    def __truediv__(self, v):
        """Divides this Vector2 by a scalar.
        If we try to divide anything other than a scalar, it throws the InvalidOperationException
        Arguments:
            v {number} -- Scalar to divide: all components of the vector are divided by this number
        Returns:
            Vector2 - Division of the Vector2
        """
        if isinstance(v, (int, float)):
            return Vector2(self.x / v, self.y / v)
        else:
            raise InvalidOperationException("mult", type(self), type(v))

    def __eq__(self, v):
        """Checks if this Vector2 is equal to the given one, with a tolerance of 0.0001.
        Exception InvalidOperationException is thrown if we compare something other than a
        Vector2.
        Arguments:
            v {Vector2} -- Vector to compare
        Returns:
            Bool - True if the vectors are the same, false otherwise
        """
        if isinstance(v, Vector2):
            return ((self - v).magnitude()) < 0.0001
        else:
            raise InvalidOperationException("eq", type(self), type(v))

    def __ne__(self, v):
        """Checks if this Vector2 is different to the given one, with a tolerance of 0.0001.
        Exception InvalidOperationException is thrown if we compare something other than a
        Vector2.
        Arguments:
            v {Vector2} -- Vector to compare
        Returns:
            Bool - True if the vectors are different, false otherwise
        """
        if isinstance(v, Vector2):
            return ((self - v).magnitude()) > 0.0001
        else:
            raise InvalidOperationException("neq", type(self), type(v))

    def __isub__(self, v):
        """Subtracts a Vector2 from this one.
        If we try to subtract anything other than a Vector2, it throws the
        InvalidOperationException.
        Arguments:
            v {Vector2} -- Vector to subtract
        Returns:
            Vector2 - Subraction of the given vector from this one
        """
        return self - v

    def __iadd__(self, v):
        """Adds this Vector2 to another.
        If we try to add anything other than a Vector2 to it, it throws the
        InvalidOperationException.
        Arguments:
            v {Vector2} -- Vector to add
        Returns:
            Vector2 - Sum of this Vector2 and the given one
        """
        return self + v

    def __imul__(self, v):
        """Multiplies this Vector2 by a scalar or a Vector2.
        Arguments:
            v {number/Vector2} -- Other element to multiply
        Returns:
            Vector2 - Multiplication of the Vector2
        """
        return self * v

    def __idiv__(self, v):
        """Divides this Vector2 by a scalar.
        If we try to divide anything other than a scalar, it throws the InvalidOperationException
        Arguments:
            v {number} -- Scalar to divide: all components of the vector are divided by this number
        Returns:
            Vector2 - Division of the Vector2
        """
        return self / v

    def __neg__(self):
        """Negates this Vector2, component-wise. Equivelent to multiplying by (-1)
        Returns:
            Vector2 - Negated Vector2
        """
        return Vector2(-self.x, -self.y)

    def is_null(self):
        return self == Vector2(0,0)

    def magnitude(self):
        """Returns the magnitude of the Vector2.
        Returns:
            Number - Magnitude of the vector
        """
        return math.sqrt(self.dot(self))

    def magnitude_squared(self):
        """Returns the squared magnitude of the Vector2.
        Returns:
            Number - Magnitude of the vector
        """
        return self.dot(self)

    def dot(self, v):
        """Computes the dot product of this Vector2 with another.
        If we try to do this operation with anything other than a Vector2, it throws
        the InvalidOperationException.
        Arguments:
            v {Vector2} -- Vector2 to do the dot product with
        Returns:
            Number - Scalar value corresponding to the dot product of both vectors
        """
        if isinstance(v, Vector2):
            return self.x * v.x + self.y * v.y
        else:
            raise InvalidOperationException("dot", type(self), type(v))

    def normalize(self):
        """Normalizes this vector"""
        d = 1.0 / self.magnitude()
        self.x *= d
        self.y *= d

    def normalized(self):
        """Returns the normalized version of this Vector2
        Returns:
            Vector2 - Normalized vector
        """
        d = 1.0 / self.magnitude()
        return Vector2(self.x * d, self.y * d)

    def to_tuple(self):
        """Returns this vector in a tuple form
        Returns:
            Tuple - (x,y)
        """
        return (self.x, self.y)

    def to_int_tuple(self):
        """Returns this vector in a tuple form, truncating the components to integers
        Returns:
            Tuple - (x,y)
        """
        return (int(self.x), int(self.y))

    @staticmethod
    def distance(v1, v2):
        """Returns the distance between two positions/vectors
        Arguments:
            v1 {Vector2} - First vector
            
            v2 {Vector2} - Second vector
        Returns:
            number - Distance between the two positions/vectors
        """
        return (v1 - v2).magnitude()

    @staticmethod
    def manhattan_distance(v1, v2):
        """Returns the manhattan distance between two positions/vectors
        Arguments:
            v1 {Vector2} - First vector
            
            v2 {Vector2} - Second vector
        Returns:
            number - Distance between the two positions/vectors
        """
        return abs(v1.x - v2.x) + abs(v1.y - v2.y)

def dot_product(v1, v2):
    """Returns the dot product between two vectors
    Arguments:
        v1 {Vector2} - First vector
        v2 {Vector2} - Second vector
    Returns:
        number - Dot product between the vectors
    """
    return v1.dot(v2)

