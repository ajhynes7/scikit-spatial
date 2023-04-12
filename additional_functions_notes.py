import scipy
import matplotlib.pyplot as plt
import numpy as np

import sys
import os
sys.path.append(r"C:\Users\ytcheah\OneDrive - hkclr\Documents\Projects\Asymetric-tesselations\scikit-spatial\src")
print(sys.path)
from skspatial.objects import Plane, Sphere, Circle, Circle3D, Vector, Point, LineSegment, Line, Triangle, Cylinder, Elipse3D
from skspatial.transformation import rotation_matrix_from_vectors, rotation_matrix_from_axis_and_angle
from skspatial.plotting import plot_3d


def intersect_spheres(S_1: Sphere, S_2: Sphere):
    # 3D circle resulting from intersection of two spheres
    # # Method 1
    # # (x-h1)^2 + (y-k1)^2 + (z-l1)^2 = R1^2     -- (1)
    # # (x-h2)^2 + (y-k2)^2 + (z-l2)^2 = R2^2     -- (2)
    # # (1) - (2)
    # # (x-h1)^2 + (y-k1)^2 + (z-l1)^2 - (x-h2)^2 - (y-k2)^2 - (z-l2)^2 = R1^2 - R2^2
    # x_offset, y_offset, z_offset = 2*(S_2.point-S_1.point)
    # coefficient = S_1.radius**2 + S_2.radius**2 + np.sum(S_2.point**2) - np.sum(S_1.point**2)
    # print(f"equation of plane: {x_offset:.04f}x + {y_offset:.04f}y + {z_offset:.04f}z = {coefficient:.04f}")

    # Method 2
    # ||P|| = R1/(R1+R2)*d
    # P_vec = (S_2C-S_1C) / ||(S_2C-S_1C)||
    # P = ||P|| * P_vec
    P_norm = S_1.radius/(S_1.radius+S_2.radius)*np.linalg.norm(S_2.point-S_1.point)
    P_vec = (S_2.point-S_1.point)/np.linalg.norm(S_2.point-S_1.point)
    P = P_norm*P_vec
    plane = Plane(S_1.point + P, P)
    C_1 = S_1.intersect_plane(plane)
    return C_1

def norm_2(v):
    return v.dot(v)
def norm(v):
    return np.sqrt(norm_2(v))

def extract_center_and_radius(sphere_coefficients):
    '''
    sphere_equation should be 
    x^2 + y^2 + z^2 + a1*x + a2*y + a3*z + a4 = 0
    so sphere equation should be parametrized
    as a list of 4 coefficients
    [a1, a2, a3, a4]
    '''
    a = np.array(sphere_coefficients)
    center = - a[0:3] / 2
    radius = np.sqrt(center.dot(center) - a[3])
    return center, radius

def intersecton_3_spheres(sphere1, sphere2, sphere3):
    '''
    spherei = (center, radius) is a tuple or a list, 
    with first entry an np.array representing
    the coordinates of the center, 
    the second being the radius
    '''
    # A, rA = sphere1
    # B, rB = sphere2
    # C, rC = sphere3
    A, rA = sphere1.point, sphere1.radius
    B, rB = sphere2.point, sphere2.radius
    C, rC = sphere3.point, sphere3.radius
    assert(A[2]==B[2]==C[2]), f"The spheres should all belong on xy plane, with the same z. A: {A}, B: {B}, C: {C}"
    AB = B-A
    AC = C-A
    l_AB = norm(AB)
    l_AC = norm(AC)
    l_BC = norm(C-B)
    x2 = (l_AB**2 + l_AC**2 - l_BC**2) / (2 * l_AB)
    y2 = np.sqrt(l_AC**2 - x2**2)
    x3 = (l_AB**2 + rA**2 - rB**2) / (2*l_AB)
    y3 = (l_AC**2 + rA**2 - rC**2) / 2
    y3 = (y3 - x2*x3) / y2
    z3 = np.sqrt(rA**2 - x3**2 - y3**2)
    n = np.cross(AB, AC)
    n = n / norm(n)
    AB = AB / l_AB
    b = np.cross(n, AB)
    return A + x3*AB + y3*b + z3*n, A + x3*AB + y3*b - z3*n

def intersecton_of_3_spheres(sphere1, sphere2, sphere3):
    '''
    the input is three lists of 4 coefficients each
    e.g. [a1, a2, a3, a4] which describe the coefficients 
    of three sphere equations 
    x^2 + y^2 + z^2 + a1*x + a2*y + a3*z + a4 = 0    
    '''
    center_radius_1 = extract_center_and_radius(sphere1)
    center_radius_2 = extract_center_and_radius(sphere2)
    center_radius_3 = extract_center_and_radius(sphere3)
    return intersecton_3_spheres(center_radius_1, center_radius_2, center_radius_3)

def sphere_trisections(A_S: Sphere, B_S: Sphere, C_S: Sphere) -> tuple[Point, Point]:
    A = A_S.point
    B = B_S.point
    C = C_S.point
    A_S_r = A_S.radius
    B_S_r = B_S.radius
    C_S_r = C_S.radius


    distances_0 = np.array([
        A.distance_point(B),
        A.distance_point(C),
        B.distance_point(C)
    ])

    A_0 = A
    B_0 = B
    C_0 = C

    # A_0 = A
    # B_0 = B
    # C_0 = C

    x_axis = Vector.from_points([0,0,0], [1,0,0])
    y_axis = Vector.from_points([0,0,0], [0,1,0])
    z_axis = Vector.from_points([0,0,0], [0,0,1])

    def rotation_matrix(axis, theta):
        """
        Return the rotation matrix associated with counterclockwise rotation about
        the given axis by theta radians.
        """
        axis = np.asarray(axis)
        axis = axis / np.sqrt(np.dot(axis, axis))
        a = np.cos(theta / 2.0)
        b, c, d = -axis * np.sin(theta / 2.0)
        aa, bb, cc, dd = a * a, b * b, c * c, d * d
        bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
        return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                        [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                        [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])

    # Algo start
    A = A-A_0 
    B = B-A_0
    C = C-A_0

    # Rotate B, C so that B aligns with X axis
    AB = Vector.from_points(A, B)
    AB_0 = AB

    # Determine angle and ortho_axis of rotation
    AB_n = AB/AB.norm()
    ortho_axis = AB_n.cross(x_axis)
    theta_1 = AB_n.angle_between(x_axis)

    # Rotate AB, AC
    B = np.dot(rotation_matrix(ortho_axis, theta_1), B)
    B = Point(B).round(10)
    # B = rot_vec(AB, A, AB.cross(x_axis), AB.angle_between(x_axis))
    AB = Vector.from_points(A, B)

    AC = Vector.from_points(A, C)
    AC_0 = AC
    AC = AC/AC.norm()

    # ortho_axis = AC.cross(y_axis)
    # theta = AC.angle_between(y_axis)
    C = np.dot(rotation_matrix(ortho_axis, theta_1), C)
    C = Point(C).round(10)
    # B = rot_vec(AB, A, AB.cross(x_axis), AB.angle_between(x_axis))
    AC = Vector.from_points(A, C)
    AC_1 = AC

    # Rotate C along x-axis so that C aligns with y axis
    theta_2 = np.arctan2(C[2],C[1])
    C = np.dot(rotation_matrix(x_axis, -theta_2), C)
    C = Point(C).round(10)
    # B = rot_vec(AB, A, AB.cross(x_axis), AB.angle_between(x_axis))
    AC = Vector.from_points(A, C)
    # print(f"C: {C}, theta: {theta_2/180*np.pi}")
    # print(f"AB = {AB}, B = {B}, Angle_between: {AB.angle_between(x_axis)/np.pi*180}")
    AC = Vector.from_points(A, C)


    distances_1 = np.array([
        A.distance_point(B),
        A.distance_point(C),
        B.distance_point(C)
    ])

    assert(np.allclose(distances_0, distances_1, atol=0)), "triangle is the not the same"

    # print(f"A: {A}, B: {B}, C: {C}")
    A_S_plane = Sphere(A, A_S_r)
    B_S_plane = Sphere(B, B_S_r)
    C_S_plane = Sphere(C, C_S_r)


    # Use sphere trisection algorithm
    D, E = intersecton_3_spheres(A_S_plane, B_S_plane, C_S_plane)

    # Rotate them back TODO

    C = np.dot(rotation_matrix(x_axis, theta_2), C)
    D = np.dot(rotation_matrix(x_axis, theta_2), D)
    E = np.dot(rotation_matrix(x_axis, theta_2), E)

    B = np.dot(rotation_matrix(ortho_axis, -theta_1), B)
    C = np.dot(rotation_matrix(ortho_axis, -theta_1), C)
    D = np.dot(rotation_matrix(ortho_axis, -theta_1), D)
    E = np.dot(rotation_matrix(ortho_axis, -theta_1), E)


    D = Point(D)
    E = Point(E)

    A = A+A_0
    B = B+A_0
    C = C+A_0
    D = D+A_0
    E = E+A_0

    return D, E

# Project P1_Sphere to plane2 
def rotX(phi):
        rotx = np.array([
            [1,     0    ,    0    ],
            [0,  np.cos(phi), -np.sin(phi)],
            [0,  np.sin(phi), np.cos(phi)] ])
        return rotx

def rotY(theta):    
    roty = np.array([
        [np.cos(theta), 0, np.sin(theta) ],
        [0         , 1,     0       ],
        [-np.sin(theta), 0,  np.cos(theta) ] ])   
    return roty
    
def rotZ(psi):    
    rotz = np.array([
        [ np.cos(psi), -np.sin(psi), 0 ],
        [np.sin(psi), np.cos(psi), 0 ],
        [   0        ,     0      , 1 ] ])   
    return rotz

def mirror_point(point, plane):
    reflected_point = point-plane.distance_point_signed(point)*plane.normal*2
    return reflected_point
    
def _rotate_point(point, theta):
    point = np.matmul(rotZ(theta), point)
    return Point(point)

def rotate_triangles(triangle, theta):
    A = _rotate_point(triangle.point_a, theta)
    B = _rotate_point(triangle.point_b, theta)
    C = _rotate_point(triangle.point_c, theta)
    return Triangle(A,B,C)
    
def mirror_triangles(triangle, plane):
    def mirror_point(point, plane):
        reflected_point = point-plane.distance_point_signed(point)*plane.normal*2
        return reflected_point
    # print(triangle)
    A = mirror_point(triangle.point_a, plane)
    B = mirror_point(triangle.point_b, plane)
    C = mirror_point(triangle.point_c, plane)
    triangle_ = Triangle(A,B,C)
    return triangle_

  

def array_triangle_array(triangle_array, theta):
    triangle_array_ = []
    for triangle in triangle_array:
        # Mirror on plane XY
        plane_xy = Plane([0,0,0], [0,0,1])
        triangle_XY_Mirror = mirror_triangles(triangle, plane_xy)

        # Polar array
        triangle_1 = rotate_triangles(triangle, theta)
        triangle_2 = rotate_triangles(triangle_XY_Mirror, theta)

        triangle_array_.append(triangle_1)
        triangle_array_.append(triangle_2)
    return triangle_array_
      
# def array_triangle_array(triangle_array, theta):
#     def _rotate_point(point, theta):
#         point = np.matmul(rotZ(theta), point)
#         return Point(point)
#     triangle_array_ = []
#     for triangle in triangle_array:
#         A = _rotate_point(triangle.point_a, theta)
#         B = _rotate_point(triangle.point_b, theta)
#         C = _rotate_point(triangle.point_c, theta)
#         triangle_array_.append(Triangle(A,B,C))
#     return triangle_array_

class TPoint():
    def __init__(self, point, plane, r, c):
        self.point = point
        self.folded_point = None
        self.r = r
        self.c = c
        self.plane = plane
    def __repr__(self):
        return f"P_Crease: {self.point}, P_Folded: {self.folded_point}, Plane: {self.plane}, Row: {self.r}, Col: {self.c}"
        # return f"Point in crease pattern: {self.crease_pattern_point}, Edge sameplane len: {self.edge_sameplane}, Edge diffplane len: {self.edge_diffplane}, Plane: {self.plane}"

def edge_len(tpoint1: TPoint, tpoint2:TPoint):
    return abs(np.linalg.norm(tpoint1.point-tpoint2.point))

vector_x = Vector([1, 0, 0])
vector_y = Vector([0, 1, 0])
vector_z = Vector([0, 0, 1])
origin = Point([0, 0, 0])


def translate_and_rotate(origin_point: Point, destination_point: Point, 
                         vector_norm_origin: Vector, vector_norm_dest: Vector,
                         target_array: np.array):
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
    vector_norm_dest=Vector(vector_norm_dest/vector_norm_dest.norm())
    rotmat = rotation_matrix_from_vectors(vector_norm_origin, vector_norm_dest)

    transmat = np.expand_dims((destination_point-origin_point).to_array(), axis=1)
    homo_mat = np.concatenate((rotmat, transmat), axis=1)
    homogeneous = np.expand_dims(np.array([0,0,0,1]), axis=0)
    homo_trans_mat = np.concatenate((homo_mat, homogeneous), axis=0)

    if np.shape(target_array) == (3,):
        ones_array = np.array([1])
    else:
        ones_array = np.ones((1, np.shape(target_array)[1]))
    
    # print(np.shape(target_array), np.shape(ones_array))
    homo_vector_mat = np.concatenate(
        (target_array, ones_array), axis=0)

    new_normal = np.matmul(homo_trans_mat, homo_vector_mat)
    # new_normal = np.dot(homo_trans_mat, homo_vector_mat)
    new_normal = new_normal[:3]/new_normal[3]
    # print(homo_trans_mat, homo_vector_mat, new_normal)    
    return new_normal

# vector_norm_dest = elipse.plane.normal
# vector_norm_origin = vector_z
# calculated_vector_norm_dest = translate_and_rotate(
#     origin, elipse.point, vector_norm_origin, vector_norm_dest, elipse.plane.normal)

# plot_3d(
#     Vector(calculated_vector_norm_dest).plotter(),
#     elipse.plane.normal.plotter(),
# )


