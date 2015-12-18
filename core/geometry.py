# -*- coding: utf-8 -*-

# Mathmaker creates automatically maths exercises sheets with their answers
# Copyright 2006-2015 Nicolas Hainaux <nico_h@users.sourceforge.net>

# This file is part of Mathmaker.

# Mathmaker is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# any later version.

# Mathmaker is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Mathmaker; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @package core.geometry
# @brief Mathematical geometrical objects.

import math
import locale
import copy
from decimal import *

from .base import *
from .base_geometry import *
from lib import *
from lib import randomly
from lib.maths_lib import *
from core.calculus import *
from lib.common.cfg import CONFIG

markup_choice = CONFIG['MARKUP']['USE']

if debug.ENABLED:
    from lib.common import latex
    import machine

if markup_choice == 'latex':
    from lib.common.latex import MARKUP

try:
    locale.setlocale(locale.LC_ALL, default.LANGUAGE + '.' + default.ENCODING)
except:
    locale.setlocale(locale.LC_ALL, '')





# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class Polygon
# @brief
class Polygon(Drawable):






    # --------------------------------------------------------------------------
    ##
    #   @brief Polygon's constructor.
    #   @param arg : Polygon |
    #                [Point, Point...] |
    #                [str, str...] <-- not implemented yet
    #            NB : the str will be the vertices' names
    #   @param options
    #   Options details :
    #   - rotate_around_gravity_center = 'no'|'any'|nb
    #                        (nb being the angle,
    #               defaulting to 'any' if sketch or 'no' if not a sketch)
    def __init__(self, arg, **options):
        self._rotation_angle = 0
        if 'rotate_around_isobarycenter' in options:
            if options['rotate_around_isobarycenter'] == 'randomly':
                self._rotation_angle = randomly.integer(0, 35) * 10
            elif is_.a_number(options['rotate_around_isobarycenter']):
                self._rotation_angle = \
                                      options['rotate_around_isobarycenter']
        if isinstance(arg, Polygon):
            self._vertex = [ v.clone() for v in arg.vertex ]
            self._rotation_angle = arg.rotation_angle
            self._side = [s.clone() for s in arg.side ]
            self._angle = [a.clone() for a in arg.angle ]
            self._rotation_angle = arg.rotation_angle

        elif type(arg) == list:
            if len(arg) <= 2:
                raise error.WrongArgument("A list of length " + str(len(arg)),
                                          "a list of length >= 3")
            if all([type(elt) == str for elt in arg]):
                raise NotImplementedError(\
                                'Using a list of str is not implemented yet')
            elif all([isinstance(elt, Point) for elt in arg]):
                self._vertex = [ p.clone() for p in arg ]
                self._side = []
                self._angle = []
                shifted_vertices = copy.deepcopy(self._vertex)
                shifted_vertices += [shifted_vertices.pop(0)]
                for (p0, p1) in zip(self._vertex, shifted_vertices):
                    self._side += [Segment((p0, p1))]
                left_shifted_vertices = copy.deepcopy(self._vertex)
                left_shifted_vertices = [left_shifted_vertices.pop(-1)] \
                                        + left_shifted_vertices
                for (p0, p1, p2) in zip(left_shifted_vertices,
                                        self._vertex,
                                        shifted_vertices):
                    self._angle += [Angle((p0, p1, p2))]
            else:
                raise error.WrongArgument("A list of Points or str "\
                                          + str(len(arg)),
                                          "a list containing something else")

        else:
            raise error.WrongArgument(str(type(arg)),
                                      "Polygon|[Point, Point...]|[str, str...]")

        self._name = ''.join([v.name for v in self._vertex])



    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the vertices (as a list of Points)
    @property
    def vertex(self):
        return self._vertex





    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the sides (as a list of Segments)
    @property
    def side(self):
        return self._side





    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the three angles (as a list of Angles)
    @property
    def angle(self):
        return self._angle





    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the angle of rotation around the isobarycenter
    @property
    def rotation_angle(self):
        return self._rotation_angle





    # --------------------------------------------------------------------------
    ##
    #   @brief Works out the dimensions of the box
    #   @param options Any options
    #   @return (x1, y1, x2, y2)
    def work_out_euk_box(self, **options):
        x_list = [ v.x for v in self.vertex ]
        y_list = [ v.y for v in self.vertex ]

        return (min(x_list)-Decimal("0.6"), min(y_list)-Decimal("0.6"),
                max(x_list)+Decimal("0.6"), max(y_list)+Decimal("0.6"))





    # --------------------------------------------------------------------------
    ##
    #   @brief Creates the euk string to put in the file
    #   @param options Any options
    #   @return The string to put in the picture file
    def into_euk(self, **options):
        box_values = self.work_out_euk_box()
        result = "box {val0}, {val1}, {val2}, {val3}"\
                 .format(val0=str(box_values[0]),
                         val1=str(box_values[1]),
                         val2=str(box_values[2]),
                         val3=str(box_values[3]))

        result += "\n\n"

        for v in self.vertex:
            result += "{name} = point({x}, {y})\n".format(name=v.name,
                                                          x=v.x,
                                                          y =v.y)

        result += "\n\ndraw\n"

        result += "("
        result += '.'.join([v.name for v in self.vertex])
        result += ")"

        # Let's add the sides' labels, if any
        for s in self.side:
            if s.label != Value(""):
                x = s.length
                scale_factor = round(Decimal(str(1.6*x)),
                                     Decimal('0.1'),
                                     rounding=ROUND_UP)
                if x <= 3:
                    angle_correction = round(Decimal(str(-8*x + 33)),
                                             Decimal('0.1'),
                                             rounding=ROUND_UP)
                else:
                    angle_correction = round(Decimal(str( \
                                                1.1/(1-0.95*math.exp(-0.027*x))
                                                        )
                                                    ),
                                             Decimal('0.1'),
                                             rounding=ROUND_UP)

                side_angle = Vector((s.points[0], s.points[1])).slope

                label_position_angle = round(Decimal(str(self.rotation_angle))\
                                             + side_angle,
                                             Decimal('1'),
                                             rounding=ROUND_HALF_EVEN
                                            )

                rotate_box_angle = Decimal(label_position_angle)

                if (rotate_box_angle >= 90 \
                    and rotate_box_angle <= 270):
                #___
                    rotate_box_angle -= Decimal("180")
                elif (rotate_box_angle <= -90 \
                    and rotate_box_angle >= -270):
               #___
                    rotate_box_angle += Decimal("180")

                result += "\n  "
                result += "$\\rotatebox{"
                result += str(rotate_box_angle)
                result += "}{"
                result += s.label.into_str(display_unit='yes',
                                           graphic_display='yes')
                result += "}$ "
                result += s.points[0].name + " "
                result += str(label_position_angle)
                result += " - "
                result += str(angle_correction) + " deg "
                result += str(scale_factor)
                result += "\n"


        for a in self.angle:
            if a.label != Value(""):
                scale_factor = Decimal('2.7')
                if Decimal(str(a.measure)) < Decimal('28.5'):
                    scale_factor = round(Decimal('38.1')\
                                              *pow(Decimal(str(a.measure)),
                                                   Decimal('-0.8')
                                                  ),
                                         Decimal('0.01'),
                                         rounding=ROUND_HALF_UP
                                         )

                label_display_angle = Vector((a.points[1],
                                              a.points[0]))\
                                      .bisector_vector(Vector((a.points[1],
                                                               a.points[2])))\
                                      .slope

                label_position_angle = label_display_angle \
                                       + Decimal(str(self.rotation_angle))

                rotate_box_angle = Decimal(label_position_angle)

                if (rotate_box_angle >= 90 \
                    and rotate_box_angle <= 270):
                #___
                    rotate_box_angle -= Decimal("180")
                elif (rotate_box_angle <= -90 \
                    and rotate_box_angle >= -270):
                #___
                    rotate_box_angle += Decimal("180")

                result += "\n  "
                result += "$\\rotatebox{"
                result += str(rotate_box_angle)
                result += "}{"
                result += a.label.into_str(display_unit='yes',
                                           graphic_display='yes')
                result += "}$ "
                result += a.vertex.name + " "
                result += str(label_position_angle) + " deg "
                result += str(scale_factor)
                result += "\n"

        result += "\nend"
        result += "\n\nlabel\n"

        names_angles_list = []

        for a in self.angle:
            # We add the labels of the angles
            if a.mark != "":
                result += "  {p0}, {v}, {p2} {m}\n".format(p0=a.points[2].name,
                                                           v=a.vertex.name,
                                                           p2=a.points[0].name,
                                                           m=a.mark)

            # and then we compute the angle to display the name of the vertex
            # of each angle
            names_angles_list += [Vector((a.points[0],
                                          a.points[1]))\
                                  .bisector_vector(Vector((a.points[2],
                                                           a.points[1])))\
                                  .slope]

        for (i, v) in enumerate(self.vertex):
            result += "  {n} {a} deg\n".format(n=v.name,
                                               a=str(names_angles_list[i]))

        return result + "\nend"





# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class Triangle
# @brief
class Triangle(Drawable):





    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor.
    #   @param arg : Triangle |
    #                ((str, str, str), (not implemented yet)'sketch'
    #        OR :                      {'side0':nb0, 'angle1':nb1, 'side1':nb2}
    #        OR : (not implemented yet){'side0':nb0, 'side1':nb1, 'side2':nb2}
    #        OR : (not implemented yet) etc.
    #                )
    #            NB : the three str will be the vertices' names
    #            NB : 'sketch' will just choose (reasonnably) random values
    #   @param options
    #   Options details :
    #   - rotate_around_gravity_center = 'no'|'any'|nb
    #                        (nb being the angle,
    #               defaulting to 'any' if sketch or 'no' if not a sketch)
    #   FOLLOWING STUFF CAN BE REPLACED BY SETTERS
    #   - label_side0, label_side1, label_side2,
    #   - mark_side0, mark_side1, mark_side2,
    #   - label_angle0, label_angle1, label_angle2,
    #   - mark_angle0, mark_angle1, mark_angle2,
    #   @warning Might raise...
    def __init__(self, arg, **options):
        if not (isinstance(arg, Triangle) or type(arg) == tuple):
            raise error.WrongArgument(' Triangle|tuple ',
                                      str(type(arg)))

        self._vertex = [None, None, None]
        self._side = [None, None, None]
        self._angle = [None, None, None]
        self._name = ""
        self._rotation_angle = 0

        if type(arg) == tuple:
            if not len(arg) == 2:
                raise error.WrongArgument(' tuple of length 2 ',
                                          ' tuple of length ' \
                                          + str(len(arg))
                                         )

            vertices_names = arg[0]
            construction_data = arg[1]

            if not type(vertices_names) == tuple:
                raise error.WrongArgument(' a tuple ', str(vertices_names))

            if not type(vertices_names[0]) == str \
                and type(vertices_names[1]) == str \
                and type(vertices_names[2]) == str:
            #___
                raise error.WrongArgument(' three strings ',
                                        ' one of them at least is not a string')

            if not (construction_data == 'sketch' \
                    or (type(construction_data) == dict \
                        and 'side0' in construction_data \
                        and is_.a_number(construction_data['side0']) \
                        and (('side1' in construction_data \
                              and is_.a_number(construction_data['side1']) \
                             ) \
                             or \
                             (('angle1' in construction_data \
                              and is_.a_number(construction_data['angle1']) \
                              ) \
                             ) \
                            ) \
                        ) \
                    ):
            #___
                raise error.WrongArgument(" 'sketch' | " \
                              + "{'side0':nb0, 'angle1':nb1, 'side1':nb2} | ",
                              str(construction_data))

            start_vertex = [None, None, None]

            side0_length = construction_data['side0']
            side1_length = construction_data['side1']

            if 'rotate_around_isobarycenter' in options:
                if options['rotate_around_isobarycenter'] == 'randomly':
                    self._rotation_angle = randomly.integer(0, 35) * 10
                elif is_.a_number(options['rotate_around_isobarycenter']):
                    self._rotation_angle = \
                                          options['rotate_around_isobarycenter']

            start_vertex[0] = Point([vertices_names[0],
                                     (0, 0)
                                    ]
                                   )
            start_vertex[1] = Point([vertices_names[1],
                                     (side0_length, 0)
                                    ]
                                   )
            start_vertex[2] = Point([vertices_names[2],
                                     (side0_length \
                                       - side1_length*Decimal(str(math.cos(\
                                     deg_to_rad(construction_data['angle1'])))),
                                      side1_length*Decimal(str(math.sin( \
                                     deg_to_rad(construction_data['angle1']))))
                                     )
                                    ]
                                   )

            if self._rotation_angle != 0:
                G = barycenter([start_vertex[0],
                                start_vertex[1],
                                start_vertex[2]
                               ],
                               "G"
                               )

                self._vertex = (Point(\
                                start_vertex[0].rotate(G,
                                                       self._rotation_angle,
                                                       keep_name=True
                                                      )
                                               ),
                                  Point(\
                                start_vertex[1].rotate(G,
                                                       self._rotation_angle,
                                                       keep_name=True
                                                      )
                                                ),
                                  Point(\
                                start_vertex[2].rotate(G,
                                                       self._rotation_angle,
                                                       keep_name=True
                                                      )
                                                )
                                  )

            else:
                self._vertex = (start_vertex[0].clone(),
                                start_vertex[1].clone(),
                                start_vertex[2].clone()
                               )

            self._side = (Segment((self._vertex[0],
                                    self._vertex[1]
                                   )
                                  ),
                           Segment((self._vertex[1],
                                    self._vertex[2]
                                   )
                                  ),
                           Segment((self._vertex[2],
                                    self._vertex[0]
                                   )
                                  )
                          )

            self._angle[0] = Angle((self.vertex[1],
                                    self.vertex[0],
                                    self.vertex[2]))

            self._angle[1] = Angle((self.vertex[2],
                                    self.vertex[1],
                                    self.vertex[0]))

            self._angle[2] = Angle((self.vertex[0],
                                    self.vertex[2],
                                    self.vertex[1]))

            self._angle[0].label_display_angle = self._angle[0].measure/2
            self._angle[1].label_display_angle = 180 - self._angle[1].measure/2
            self._angle[2].label_display_angle = 180 + self._angle[0].measure \
                                                     + self._angle[2].measure/2

        else:
            # copy of a given Triangle
            self._vertex = [arg.vertex[0].clone(),
                            arg.vertex[1].clone(),
                            arg.vertex[2].clone()
                           ]
            self._rotation_angle = arg.rotation_angle
            self._side = [arg.side[0].clone(),
                          arg.side[1].clone(),
                          arg.side[2].clone()
                         ]
            self._angle = [arg.angle[0].clone(),
                           arg.angle[1].clone(),
                           arg.angle[2].clone()
                          ]

        self._name = self.vertex[0].name + self.vertex[1].name \
                     + self.vertex[2].name

        random_number = ""
        for i in range(8):
            random_number += str(randomly.integer(0, 9))

        self._filename = _("Triangle") + "_" + self.name \
                         + "-" + random_number







    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the three vertices (as a list of Points)
    @property
    def vertex(self):
        return self._vertex





    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the three sides (as a list of Segments)
    @property
    def side(self):
        return self._side





    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the three angles (as a list of Angles)
    @property
    def angle(self):
        return self._angle





    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the angle of rotation around the isobarycenter
    @property
    def rotation_angle(self):
        return self._rotation_angle





    # --------------------------------------------------------------------------
    ##
    #   @brief Creates the euk string to put in the file
    #   @param options Any options
    #   @return The string to put in the picture file
    def into_euk(self, **options):
        box_values = self.work_out_euk_box()
        result = "box " + str(box_values[0]) + ", " \
                        + str(box_values[1]) + ", " \
                        + str(box_values[2]) + ", " \
                        + str(box_values[3])

        result += "\n\n"

        for v in self.vertex:
            result += v.name + " = point(" + str(v.x) + ", " + str(v.y) + ")\n"

        result += "\n\n"

        result += "draw"

        result += "\n  "

        result += "(" + self.vertex[0].name + "." \
                      + self.vertex[1].name + "." \
                      + self.vertex[2].name + ")"

        scale_factor = 1
        angle_correction = 0

        sides_angles_offsets = {self.side[0] : 0,
                                self.side[1] : 180 - self.angle[1].measure,
                                self.side[2] : self.angle[0].measure
                               }

        labels_angle_correction_signs = {self.side[0] : "-",
                                         self.side[1] : "-",
                                         self.side[2] : "+"
                                        }

        labels_ref_points = {self.side[0] : self.vertex[0].name,
                             self.side[1] : self.vertex[1].name,
                             self.side[2] : self.vertex[0].name
                            }


        for s in self.side:
            if s.label != None and s.label != Value(""):
                x = s.length
                scale_factor = round(Decimal(str(1.6*x)),
                                     Decimal('0.1'),
                                     rounding=ROUND_UP
                                    )
                if x <= 3:
                    angle_correction = round(Decimal(str(-8*x + 33)),
                                             Decimal('0.1'),
                                             rounding=ROUND_UP
                                            )
                else:
                    angle_correction = round(Decimal(str( \
                                                1.1/(1-0.95*math.exp(-0.027*x))
                                                        )
                                                    ),
                                             Decimal('0.1'),
                                             rounding=ROUND_UP
                                            )

                label_position_angle = round(Decimal(str(self.rotation_angle))\
                                             + \
                                             Decimal(str(\
                                                    sides_angles_offsets[s])),
                                             Decimal('1'),
                                             rounding=ROUND_HALF_EVEN
                                            )

                rotate_box_angle = Decimal(label_position_angle)

                if (rotate_box_angle >= 90 \
                    and rotate_box_angle <= 270):
                #___
                    rotate_box_angle -= Decimal("180")
                elif (rotate_box_angle <= -90 \
                    and rotate_box_angle >= -270):
               #___
                    rotate_box_angle += Decimal("180")

                result += "\n  "
                result += "$\\rotatebox{"
                result += str(rotate_box_angle)
                result += "}{"
                result += s.label.into_str(display_unit='yes',
                                           graphic_display='yes')
                result += "}$ "
                result += labels_ref_points[s] + " "
                result += str(label_position_angle)
                result += " " + labels_angle_correction_signs[s] + " "
                result += str(angle_correction) + " deg "
                result += str(scale_factor)
                result += "\n"


        for a in self.angle:
            if a.label != None and a.label != Value(""):
                scale_factor = Decimal('2.7')
                if Decimal(str(a.measure)) < Decimal('28.5'):
                    scale_factor = round(Decimal('38.1')\
                                              *pow(Decimal(str(a.measure)),
                                                   Decimal('-0.8')
                                                  ),
                                         Decimal('0.01'),
                                         rounding=ROUND_HALF_UP
                                         )

                label_position_angle = Decimal(str(a.label_display_angle)) \
                                       + Decimal(str(self.rotation_angle))
                rotate_box_angle = Decimal(label_position_angle)

                if (rotate_box_angle >= 90 \
                    and rotate_box_angle <= 270):
                #___
                    rotate_box_angle -= Decimal("180")
                elif (rotate_box_angle <= -90 \
                    and rotate_box_angle >= -270):
                #___
                    rotate_box_angle += Decimal("180")

                result += "\n  "
                result += "$\\rotatebox{"
                result += str(rotate_box_angle)
                result += "}{"
                result += a.label.into_str(display_unit='yes',
                                           graphic_display='yes')
                result += "}$ "
                result += a.vertex.name + " "
                result += str(label_position_angle) + " deg "
                result += str(scale_factor)
                result += "\n"

        result += "\nend"

        result += "\n\n"

        result += "label"

        result += "\n"

        for a in self.angle:
            if a.mark != "":
                result += "  " + a.points[0].name + ", " \
                        + a.vertex.name + ", " \
                        + a.points[2].name \
                        + " " \
                        + a.mark
                result += "\n"

        result += "  " + self.vertex[0].name + " " \
               + str(self.rotation_angle) + " + 200 deg"

        result += "\n"

        result += "  " + self.vertex[1].name + " " \
               + str(self.rotation_angle) + " - 45 deg"

        result += "\n"

        result += "  " + self.vertex[2].name + " " \
               + str(self.rotation_angle) + " + 65 deg"

        result += "\nend"

        return result





    # --------------------------------------------------------------------------
    ##
    #   @brief Works out the dimensions of the box
    #   @param options Any options
    #   @return (x1, y1, x2, y2)
    def work_out_euk_box(self, **options):
        x_list = [self.vertex[0].x,
                  self.vertex[1].x,
                  self.vertex[2].x
                  ]
        y_list = [self.vertex[0].y,
                  self.vertex[1].y,
                  self.vertex[2].y
                  ]

        return (min(x_list)-Decimal("0.6"), min(y_list)-Decimal("0.6"),
                max(x_list)+Decimal("0.6"), max(y_list)+Decimal("0.6"))






# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class RightTriangle
# @brief
class RightTriangle(Triangle):





    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor.
    #   @param arg : RightTriangle |
    #                ((str, str, str), 'sketch'
    #        OR :                      {'leg0' : nb0, 'leg1' : nb1}
    #        OR : (not implemented yet){'leg0' : nb0, 'angle0' : nb1}
    #                )
    #            NB : the three str will be the vertices' names
    #                 The second name will be the right corner
    #                 so, hypotenuse will be vertices_names[0] & [2]
    #            NB : 'sketch' will just choose (reasonnably) random values
    #   @param options
    #   Options details :
    #   - rotate_around_gravity_center = 'no'|'any'|nb
    #                        (nb being the angle,
    #               defaulting to 'any' if sketch or 'no' if not a sketch)
    #   FOLLOWING ONES HAVE BEEN REPLACED BY MATCHING SETTERS
    #   - label_leg0, label_leg1, label_hypotenuse,
    #   - dont_label_right_angle, label_angle0, label_angle2
    #   @warning Might raise...
    def __init__(self, arg, **options):
        if not (isinstance(arg, RightTriangle) or type(arg) == tuple):
            raise error.WrongArgument(' RightTriangle|tuple ',
                                      str(type(arg)))

        self._vertex = [None, None, None]
        self._rotation_angle = 0
        self._side = [None, None, None]
        self._name = ""

        if type(arg) == tuple:
            if not len(arg) == 2:
                raise error.WrongArgument(' tuple of length 2 ',
                                          ' tuple of length ' \
                                          + str(len(arg))
                                         )
            vertices_names = arg[0]
            construction_data = arg[1]

            if not type(vertices_names) == tuple:
                raise error.WrongArgument(' a tuple ', str(vertices_names))

            if not type(vertices_names[0]) == str \
                and type(vertices_names[1]) == str \
                and type(vertices_names[2]) == str:
            #___
                raise error.WrongArgument(' three strings ',
                                        ' one of them at least is not a string')

            rotation = 0

            if 'rotate_around_isobarycenter' in options \
                and options['rotate_around_isobarycenter'] == 'randomly':
            #___
                rotation = randomly.integer(0, 35) * 10

            elif 'rotate_around_isobarycenter' in options \
                and is_.a_number(options['rotate_around_isobarycenter']):
            #___
                rotation = options['rotate_around_isobarycenter']

            leg0_length = 0
            leg1_length = 0

            if construction_data == 'sketch':
                leg0_length = Decimal(str(randomly.integer(35, 55)))/10
                leg1_length = Decimal(str(randomly.integer(7, 17))) \
                              / Decimal("20") * leg0_length

            elif type(construction_data) == dict \
                and 'leg0' in construction_data \
                and is_.a_number(construction_data['leg0']) \
                and 'leg1' in construction_data \
                and is_.a_number(construction_data['leg1']):
            #___
                leg0_length = construction_data['leg0']
                leg1_length = construction_data['leg1']

            else:
                raise error.WrongArgument(" 'sketch' | " \
                                        + "{'leg0' : nb0, 'leg1' : nb1}",
                                          str(construction_data))

            Triangle.__init__(self,
                              ((vertices_names[0],
                                vertices_names[1],
                                vertices_names[2]
                                ),
                               {'side0' : leg0_length,
                                'angle1' : 90,
                                'side1' : leg1_length
                               }
                              ),
                              rotate_around_isobarycenter=rotation
                             )

        else:
            # copy of a given RightTriangle
            self._vertex = [arg.vertex[0].clone(),
                            arg.vertex[1].clone(),
                            arg.vertex[2].clone()
                           ]
            self._rotation_angle = arg.rotation_angle
            self._side = [arg.side[0].clone(),
                          arg.side[1].clone(),
                          arg.side[2].clone()
                         ]
            self._angle = [arg.angle[0].clone(),
                           arg.angle[1].clone(),
                           arg.angle[2].clone()
                          ]
            # the other fields are re-created hereafter

        self._name = self.vertex[0].name + self.vertex[1].name \
                     + self.vertex[2].name

        self.right_angle.mark = "right"

        random_number = ""
        for i in range(8):
            random_number += str(randomly.integer(0, 9))

        self._filename = _("RightTriangle") + "_" + self.name \
                         + "-" + random_number





    # --------------------------------------------------------------------------
    ##
    #   @brief Returns legs (as a Segment)
    @property
    def leg(self):
        return [self._side[0], self._side[1]]





    # --------------------------------------------------------------------------
    ##
    #   @brief Returns hypotenuse (as a Segment)
    @property
    def hypotenuse(self):
        return self._side[2]





    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the right angle (as an Angle)
    @property
    def right_angle(self):
        return self.angle[1]





    # --------------------------------------------------------------------------
    ##
    #   @brief Creates the correct pythagorean equality hyp²=leg0²+leg1²
    #   @return an Equality but not usable to calculate (see substequality)
    def pythagorean_equality(self, **options):

        objcts = [Item(('+', self.hypotenuse.length_name, 2)),
                  Sum([Item(('+', self.leg[0].length_name, 2)),
                       Item(('+', self.leg[1].length_name, 2))]
                     )]

        return Equality(objcts, **options)




# --------------------------------------------------------------------------
    ##
    #   @brief Creates the correct (substitutable) pythagorean equality
    #   @brief Uses the labels to determine the result...
    #   @return a SubstitutableEquality
    def pythagorean_substequality(self, **options):
        # First, check the number of numeric data
        # and find the unknown side
        n_numeric_data = 0
        unknown_side = ""
        if self.leg[0].label.is_numeric():
            n_numeric_data += 1
        elif self.leg[0].label.raw_value == "":
            unknown_side = 'leg0'
        if self.leg[1].label.is_numeric():
            n_numeric_data += 1
        elif self.leg[1].label.raw_value == "":
            unknown_side = 'leg1'
        if self.hypotenuse.label.is_numeric():
            n_numeric_data += 1
        elif self.hypotenuse.label.raw_value == "":
            unknown_side = 'hypotenuse'

        if n_numeric_data != 2:
            raise error.ImpossibleAction("creation of a pythagorean equality "\
                                         "when the number of known numeric " \
                                         "values is different from 2.")

        # Now create the SubstitutableEquality (so, also create the dictionnary)
        if unknown_side == 'leg0':
            subst_dict = {Value(self.leg[1].length_name): self.leg[1].label,
                          Value(self.hypotenuse.length_name): \
                                                        self.hypotenuse.label
                         }
            objcts = [Item(('+', self.leg[0].length_name, 2)),
                      Sum([Item(('+', self.hypotenuse.length_name, 2)),
                           Item(('-', self.leg[1].length_name, 2))]
                         )]

        elif unknown_side == 'leg1':
            subst_dict = {Value(self.leg[0].length_name): self.leg[0].label,
                          Value(self.hypotenuse.length_name): \
                                                        self.hypotenuse.label
                         }
            objcts = [Item(('+', self.leg[1].length_name, 2)),
                      Sum([Item(('+', self.hypotenuse.length_name, 2)),
                           Item(('-', self.leg[0].length_name, 2))]
                         )]

        elif unknown_side == 'hypotenuse':
            subst_dict = {Value(self.leg[0].length_name): self.leg[0].label,
                          Value(self.leg[1].length_name): self.leg[1].label
                         }
            objcts = [Item(('+', self.hypotenuse.length_name, 2)),
                      Sum([Item(('+', self.leg[0].length_name, 2)),
                           Item(('+', self.leg[1].length_name, 2))]
                         )]

        else:
            raise error.ImpossibleAction("creation of a pythagorean equality "\
                                         "because no unknown side was found")


        return SubstitutableEquality(objcts, subst_dict)
