from numpy import random
import itertools
from itertools import chain

# CONSTANTS
LINK_LEN = 30
EMPTY_CELL = 0
FULL_CELL = 1

# test map part
minimap = [
    ['a01', 'l01', 'a02']
]

connections = [
    ['a01', 'l01'],
    ['a02', 'l01'],
]

vehicles = 20


# end map part


class Link:
    def __init__(self, source: 'Point', destination: 'Point'):
        self.code = '{}-{}'.format(source.code, destination.code)
        self.reverse_code = '{}-{}'.format(destination.code, source.code)
        self.source = source
        self.destination = destination
        self.queue = LINK_LEN * [0]
        self.stucked = 0
        self.inactive = False

    def step(self):
        self.stucked = 0
        self.inactive = True
        skip = False

        for i in range(LINK_LEN - 1):
            if skip or self.queue[i] == EMPTY_CELL:
                skip = False
                continue
            if self.queue[i + 1] == FULL_CELL:
                self.stucked += 1
            else:
                skip = True
                self.inactive = False
                self.queue[i] = 0
                self.queue[i + 1] = 1



        if self.queue[-1] == FULL_CELL:
            if self.destination._redirect(self):
                self.queue[-1] = 0
                self.inactive = False
            else:
                self.stucked += 1

        print(self.queue)

    def reset(self):
        self.queue = [0] * LINK_LEN
        self.stucked = 0

    def generate(self, empty_cells=1):
        empty = self.si_empty(empty_cells)
        if empty:
            self.queue[0] = 1
            self.inactive = False
        return empty

    def _redirect(self, *_):
        return self.generate()

    def si_empty(self, span: int = 1):
        return not any(self.queue[:span])


class LinkPoint:
    def __init__(self, code: str):
        self.code = code
        self.incomming = []
        self.outcomming = []
        self.register = 0

    def register_links(self, incomming: Link, outcomming: Link):
        self.incomming.append(incomming)
        self.outcomming.append(outcomming)
        self.register += 2

    def lock(self):
        try:
            self.incomming[0].destination = self.outcomming[1]
            self.incomming[1].destination = self.outcomming[0]
        except IndexError as e:
            raise RuntimeError(e, self)

        if self.register != 4:
            raise RuntimeError('LinkPoint got links instead of 4')


class Point:
    def __init__(self, code):
        self.code = code
        self.incomming_cicle = None
        self.outcomming_cicle = None
        self.incomming = []
        self.outcomming = []

    def register_links(self, incomming: Link, outcomming: Link):
        self.incomming.append(incomming)
        self.outcomming.append(outcomming)

    def lock(self):
        self.incomming_cicle = itertools.cycle(self.incomming)
        self.outcomming_cicle = itertools.cycle(self.outcomming)

    def _redirect(self, link):
        raise RuntimeError('not user in object')


class AccessPoint(Point):
    def __init__(self, code):
        super().__init__(code)
        self.callback = None
        self.to_generate = 0
        self.inactive = False
        self.skip = False

    def _redirect(self, link):
        self.callback()
        return True

    def generate(self):
        self.to_generate += 1

    def step(self):
        print("a")
        self.inactive = True
        if self.to_generate == 0:
            return False
        if self.skip:
            self.skip=False
            return

        for _ in range(len(self.outcomming)):
            print("lduhgliurhgpieruhg")
            print(self.outcomming_cicle)
            possible_link = next(self.outcomming_cicle)
            if possible_link._redirect:
                self.to_generate -= 1
                self.skip = True
                return True
            self.inactive = True




class JunctionPoint(Point):
    def __init__(self, code):
        super().__init__(self, code)


    def _redirect(self, link) -> bool:

        if self.open[link.code]:
            for _ in range(len(self.links)):
                possible_link = next(self.outcoming_cicle)
                if possible_link.code != link.reverse_code and possible_link._redirect():
                    return True
                else:
                    continue


        else:
            return False


class Core:
    """
    Core object for controlling other objects.
    Works with AI and is controlled by Controller
    In init method implements minimap, connections and vehicles
    """

    def __init__(self, minimap: list, connections: list, vehicles: int):

        self.TYPES = {"a": AccessPoint,
                      "j": JunctionPoint,
                      "l": LinkPoint,
                      }
        self.vehicles = vehicles
        self.access_points = []
        self.junction_points = []
        self.junction_queues = []
        self.points = {}
        self.links = []


        self.nn = False
        self.__process(minimap, connections)

    def __process(self, minimap, connections):
        """


        """
        for code in chain.from_iterable(minimap):
            if not code:
                continue

            point = self.TYPES[code[0]](code=code)
            self.points[code] = point

            if code[0] == "a":
                point.callback = self.spawn_vehicle
                self.access_points.append(point)

            if code[0] == "j":
                self.junction_points.append(point)

        for connection in connections:
            self.create_links(*connection)

    def __exec_nn(self):
        pass

    def reset(self):
        self.nn = False
        for link in self.links:
            link.reset()
        for point in self.points.values():
            point.reset()

    def spawn_vehicle(self):
        for _ in range(self.vehicles):
            random.choice(self.access_points).generate()

    def create_links(self, code1, code2):

        point1 = self.points[code1]
        point2 = self.points[code2]
        print("Point1", point1)
        print("Point2", point2)
        link1 = Link(source=point1, destination=point2)
        link2 = Link(source=point2, destination=point1)

        self.links.extend((link1, link2))
        if code1[0] == "j":
            self.junction_queues.append(point2)
        if code2[0] == "j":
            self.junction_queues.append(point1)

        point1.register_links(incomming=link1, outcomming=link2)
        point2.register_links(incomming=link2, outcomming=link1)
        point1.lock()
        point2.lock()
    def finalize(self):

        self.links = self.links.sort(key=lambda point: self.links.code)
        self.points = self.points.sort(key=lambda point: self.points.code)
        for point in self.points.values():
            point.lock()

    def step(self):

        for link in self.links:
            link.step()
        for access_point in self.access_points:
            access_point.step()


# test part
test = Core(minimap, connections, vehicles)
for i in range(100):

    test.spawn_vehicle()
for i in range(100):
    test.step()
    input()
lukas = Lukas()
lukas.repair_our_code()