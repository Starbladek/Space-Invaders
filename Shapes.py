class Point:
    def __init__(self, x, y):
        self.__x, self.__y = x, y

    def x(self): return self.__x

    def y(self): return self.__y


class Vector:
    def __init__(self, x, y, z):
        self.__x, self.__y, self.__z = x, y, z

    def __str__(self): return 'Vector(' + str(self.x) + ',' + str(self.y) + ',' + str(self.z) + ')'

    def __add__(self, other): return Vector(self.x + other.x,
                                            self.y + other.y,
                                            self.z + other.z)

    def __sub__(self, other): return Vector(self.x - other.x,
                                             self.y - other.y,
                                             self.z - other.z)

    def __neg__(self): return Vector(-self.x, -self.y, -self.z)

    def dot(self, other): return self.x * other.x + self.y * other.y + self.z * other.z

    def cross_product(self, other): return Vector(self.y * other.z - self.z - other.y,
                                                  self.z * other.y - self.x * other.z,
                                                  self.x * other.y - self.y * other.x)

    def getx(self): return self.__x    # x is a private variable, thats why we need this getter function
    def setx(self, x): self.__x = x

    def gety(self): return self.__y
    def sety(self, y): self.__y = y

    def getz(self): return self.__z
    def setz(self, z): self.__z = z

    x = property(getx, setx)
    y = property(gety, sety)
    z = property(getz, setz)

    @classmethod
    def create(cls, pt1, pt2):      # Class methods do not get self
        return cls(pt1.x - pt2.x,
                   pt1.y - pt2.y,
                   pt1.z - pt2.z)

    @staticmethod
    def create_static(pt1, pt2):
        return Vector(pt1.x - pt2.x,
                      pt1.y - pt2.y,
                      pt1.z - pt2.z)


class Rectangle:
    def __init__(self, ul, br):
        self.__ul, self.__br = ul, br
        self.__ur, self.__bl = Point(br.x(), ul.y()), Point(ul.x(), br.y())

    def __str__(self):
        print('lol')

    def ul(self): return self.__ul

    def bl(self): return self.__bl

    def ur(self): return self.__ur

    def br(self): return self.__br

    def width(self):
        return self.__br.x() - self.__bl.x()

    def height(self):
        return self.__ul.y() - self.__bl.y()

    def center(self):
        x = (self.__ul.x() + self.__ur.x()) / 2
        y = (self.__ul.y() + self.__bl.y()) / 2
        return Point(x, y)

    def area(self): return self.width() * self.height()

    def perimeter(self): return 2 * (self.width() + self.height())

    def collides_with(self, other):
        if self.__ul.x() < other.__br.x():
            return True
        else:
            return False


class Triangle:
    def __init__(self, p1=Point(0,0), p2=Point(0,0), p3=Point(0,0)):
        self.__p1, self.__p2, self.__p3 = p1, p2, p3


'''rect1 = Rectangle(Point(-1, 1), Point(0, 0))
rect2 = Rectangle(Point(0, 1), Point(1, 0))

vect1 = Vector(2, 4, 6)
vect1.x = 44    # We can do this because of the @property shit above
vect1.setx(44)  # these two lines do the same thing

print('-vect1 = ' + str(-vect1))    # this does str(vect1.__neg__)'''
