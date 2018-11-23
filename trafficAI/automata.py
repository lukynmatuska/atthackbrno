from numpy import random
from itertools import chain


class Link:
    pass


class LinkPoint:
    pass


class Point:
    pass


class AccessPoint(Point):
    def __init__(self, code):
        super().__init__(code)


class JunctionPoint(Point):
    def __init__(self, code):
        super().__init__(self, code)

    def _redirect(self, link) -> bool:

        if self.open[link.code]:
            for _ in range(len(self.links)):
                possible_link = next(self.outcoming_cycle)
                if possible_link.code != link.reverse_code and possible_link._redirect():
                    return True
                else:
                    continue


        else:
            return False


    def register_links(self):
        pass

    def lock(self):
        pass

    def _redirect(self):
        pass


class Core:
    """
    Core object for controlling other objects.
    Works with AI and is controlled by Controller
    In init method implements minimap, connections and vehicles
    TYPES = {a: AccessPoint,
             j: JunctionPoint,
             l: LinkPoint,
        }"""

    def __init__(self, minimap: list, connections: list, vehicles: int):

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

            point = Point(code=code)
            self.point[code] = point

            if code[0] == "a":
                point.callback = self.spawn
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
            random.choice(self.access_points).spawn()

    def create_links(self, code1, code2):

        point1 = self.points[code1]
        point2 = self.points[code2]
        link1 = Link(source=point1, destination=point2)
        link2 = Link(source=point2, destination=point1)

        self.links.extend((link1, link2))
        if code1[0] == "j":
            self.junction_queues.append(point2)
        if code2[0] == "j":
            self.junction_queues.append(point1)

        point1.register_links(incoming=link1, outcoming = link2)
        point2.register_links(incoming=link2, outcoming = link1)

    def finalize(self):

        self.links = self.links.sort(key=lambda point: self.links.code)
        self.points = self.points.sort(key=lambda point: self.points.code)
        for point in self.points.values():
            point.lock()

    def step(self):

        for link in self.links:
            link.step()

        for point in self.points.values():
            point.step()
