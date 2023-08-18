import scipy
import matplotlib.pyplot as plt
import numpy as np
import pickle
import sys
import shutil
import os

# sys.path.insert(0, r"/home/yeok/Github/Asymetric-tesselations-1")
# sys.path.insert(0, r"D:\Github\Asymetric-tesselations-1")
# sys.path.append(r"C:\Users\ytcheah\OneDrive - hkclr\Documents\Projects\Asymetric-tesselations\scikit-spatial\src")
# print(sys.path)
from skspatial.objects import Plane, Sphere, Circle, Circle3D, Vector, Point, LineSegment, Line, Triangle, Cylinder, Elipse3D
from skspatial.transformation import *
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

    P_norm = S_1.radius/(S_1.radius+S_2.radius)*norm(S_2.point-S_1.point)
    P_vec = (S_2.point-S_1.point)/norm(S_2.point-S_1.point)
    P = P_norm*P_vec
    plane = Plane(S_1.point + P, P)
    C_1 = S_1.intersect_plane(plane)
    return C_1

def norm_2(v):
    return v.dot(v)
def norm(v):
    return np.sqrt(norm_2(v))

def dist(v):
    assert np.shape(v)[0] == 3, "v should be a 3D vector"
    return np.sqrt(v[0]**2 + v[1]**2 + v[2]**2)

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
    n = cross(AB, AC)
    n = n / norm(n)
    AB = AB / l_AB
    b = cross(n, AB)
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
    # B_0 = B
    # C_0 = C

    x_axis = Vector.from_points([0,0,0], [1,0,0])
    # y_axis = Vector.from_points([0,0,0], [0,1,0])
    # z_axis = Vector.from_points([0,0,0], [0,0,1])

    def rotation_matrix(axis, theta):
        """
        Return the rotation matrix associated with counterclockwise rotation about
        the given axis by theta radians.
        """
        axis = np.asarray(axis)
        axis = axis / np.sqrt(dot(axis, axis))
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

    # CHANGED FOR SPEED
    ortho_axis = AB_n.cross(x_axis)
    # ortho_axis = cross(x_axis, AB_n)
    
    
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

    # C = np.dot(rotation_matrix(x_axis, theta_2), C)
    D = np.dot(rotation_matrix(x_axis, theta_2), D)
    E = np.dot(rotation_matrix(x_axis, theta_2), E)

    # B = np.dot(rotation_matrix(ortho_axis, -theta_1), B)
    # C = np.dot(rotation_matrix(ortho_axis, -theta_1), C)
    D = np.dot(rotation_matrix(ortho_axis, -theta_1), D)
    E = np.dot(rotation_matrix(ortho_axis, -theta_1), E)


    D = Point(D)
    E = Point(E)

    # A = A+A_0
    # B = B+A_0
    # C = C+A_0
    D = D+A_0
    E = E+A_0

    return D, E

def cross(a,b):
    return np.array([a[1]*b[2] - a[2]*b[1], a[2]*b[0] - a[0]*b[2], a[0]*b[1] - a[1]*b[0]])
    

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


vector_x = Vector([1, 0, 0])
vector_y = Vector([0, 1, 0])
vector_z = Vector([0, 0, 1])
origin = Point([0, 0, 0])

def dot(a,b):
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]

def translate_and_rotate(origin_point: Point, destination_point: Point, 
                         vector_norm_origin: Vector, vector_norm_dest: Vector,
                         target_array: np.array):
                         
    vector_norm_dest=vector_norm_dest/vector_norm_dest.norm()
    # vector_norm_dest=Vector(vector_norm_dest/vector_norm_dest.norm())
    
    # DIRECTLY PUT HERE FOR SPEED    
    # rotmat = rotation_matrix_from_vectors(vector_norm_origin, vector_norm_dest)
    a, b = (vector_norm_origin / norm(vector_norm_origin)).reshape(3), (vector_norm_dest / norm(vector_norm_dest)).reshape(3)
    # print(a,b)
    
    # REMOVED FOR SPEED - Retiring np.cross, rewriting cross manually
    # v = np.cross(a, b)
    v = np.array([a[1]*b[2] - a[2]*b[1], a[2]*b[0] - a[0]*b[2], a[0]*b[1] - a[1]*b[0]])
    
    # CHANGED FOR SPEED - retiring np.dot, rewriting dot manually
    # c = np.dot(a, b)
    c = dot(a,b)


    s = norm(v)
    kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    rotmat = np.eye(3) + kmat + kmat.dot(kmat) * ((1 - c) / (s ** 2))


    # CHANGED FOR SPEED
    # transmat = np.expand_dims((destination_point-origin_point).to_array(), axis=1)
    transmat = np.array([destination_point-origin_point.to_array()],).T

    homo_mat = np.concatenate((rotmat, transmat), axis=1)
    # homogeneous = np.expand_dims(np.array([0,0,0,1]), axis=0)
    homogeneous = np.array([[0,0,0,1]])
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


def intersect_spheres(S_1: Sphere, S_2: Sphere):
    # Method 2
    # ||P|| = R1/(R1+R2)*d
    # P_vec = (S_2C-S_1C) / ||(S_2C-S_1C)||
    # P = ||P|| * P_vec

    # P_norm = S_1.radius/(S_1.radius+S_2.radius)*dist(S_2.point-S_1.point)
    d = dist(S_2.point-S_1.point)
    P_norm = (d**2 + S_1.radius**2 - S_2.radius**2)/(2*d) 
    # print(d, P_norm, P_norm_test)
    P_vec = (S_2.point-S_1.point)/d
    P = P_norm*P_vec
    plane = Plane(S_1.point + P, P)


    C_1 = S_1.intersect_plane(plane)
    # print(P_norm, P_vec, P, plane, "\n\n\n")
    return C_1

def intersect_circle(self: Elipse3D, circle: Circle3D):
    """Find the intersection between a circle and a elipse on a 2D plane"""

    # vector_x = Vector([1, 0, 0])
    # vector_y = Vector([0, 1, 0])
    vector_z = Vector([0, 0, 1])
    origin = Point([0, 0, 0])


    # TODO Check if same plane


    # Conduct all calculations on 2D plane first --- 
    r = circle.radius
    x0 = norm(circle.point-self.point)
    # print(circle.point-self.point)
    a = self.a
    b = self.b
    c = 1-(b/a)**2

    A = 1
    B = -2*x0/c
    C = -(r**2-b**2-x0**2)/c
    X1 = (-B + np.sqrt(B**2 - 4*A*C))/(2*A)
    X2 = (-B - np.sqrt(B**2 - 4*A*C))/(2*A)
    # Y1 = np.sqrt(r**2-(X1-x0)**2)

    TEMP = r**2-(X2-x0)**2
    if TEMP < 0:
        return None, None
    else:
        Y2 = np.sqrt(TEMP)

    # print(f"r={r}, x0={x0}, a={a}, b={b}, X1={X1}, X2={X2}, Y1={Y1}, Y2={Y2}")
    P1 = np.array([X2, Y2, 0])
    P2 = np.array([X2,-Y2, 0])

    # def rotZ(psi):    
    #     rotz = np.array([
    #         [ np.cos(psi), -np.sin(psi), 0 ],
    #         [np.sin(psi), np.cos(psi), 0 ],
    #         [   0        ,     0      , 1 ] ])   
    #     return rotz

    # angle = self.plane.normal.angle_between(Vector([0, 0, 1]))
    # P1 = np.matmul(rotY(angle), P1)
    # P2 = np.matmul(rotY(angle), P2)
    # P1 = self.point + Point(P1)
    # P2 = self.point + Point(P2)
    # print(P1,P2)

    # Translate and rotate to the circle's plane
    # The necessary rotation is the angle between circle.plane.normal (normal of circle's plane) and vector_z (normal of xy-plane) 
    P1 = translate_and_rotate(
        origin, self.point, vector_z, circle.plane.normal, P1)
    P2 = translate_and_rotate(
        origin, self.point, vector_z, circle.plane.normal, P2)
    
    # Move (P1, P2) on the xy-plane (normal vector= vector_z) so that the new normal vector=circle.plane.normal

    return 0, P2


# intersect sphere-sphere-cylinder
def ssc_intersect(Point_0:Point, Point_1:Point, Point_2:Point, W:float):
    '''
    Point_0: First sphere center
    Point_1: The crease pattern of the desired point, which is why theres no Point_1.folded point yet
    Point_2: Second sphere center and also cylinder center (the point at the middle of the crease pattern) 

    '''
    last_time = time.time()
    # TIME_SSC = [{"Program started": last_time}]
    # Two spheres intersect to form a 2D circle on a plane ----
    # TIME_SSC, last_time = tim(TIME_SSC, last_time, "Start SSC")
    S_P1P0 = Sphere(Point_0.folded_point, edge_len(Point_1, Point_0))
    S_P1P2 = Sphere(Point_2.folded_point, edge_len(Point_1, Point_2))
    # TIME_SSC, last_time = tim(TIME_SSC, last_time, "Created Spheres")

    # print(S_P1P0, S_P1P2)

    circle = intersect_spheres(S_P1P2, S_P1P0) 
    if circle.plane.normal[2] < 0:
        circle.plane.normal = -circle.plane.normal 
        
    # TIME_SSC, last_time = tim(TIME_SSC, last_time, "Intersected Spheres")
    # print(circle.plane.normal )

    # Cylinder is defined using where the edge and center lines intersect with the plane of the 2D circle ----

    cylinder = Cylinder(Point_2.folded_point-np.array([0,0,-50]), Vector([0,0,-100]), W) # Valid since parallel to z-axis
    cylinder_center_line = Line(Point_2.folded_point, Vector([0, 0, 1]))
    cylinder_long_edge_line = Line(
        # THE W 0 0 IS SUS
        Point_2.folded_point + np.array([W,0,0]), 
        Vector([0, 0, 100]))
    # TIME_SSC, last_time = tim(TIME_SSC, last_time, "Created Cylinder")
    
    # On the 2D plane, find the intersections between circle and elipse ----

    # cylinder_edge_line = Line(Point_2.folded_point+Point([W,0,0]), Vector([0, 0, 1]))
    elipse_c = circle.plane.intersect_line(cylinder_center_line)
    elipse_a_coords = circle.plane.intersect_line(cylinder_long_edge_line)
    # TIME_SSC, last_time = tim(TIME_SSC, last_time, "2x Intersect lines")

    elipse_a = norm((elipse_a_coords-elipse_c))
    elipse_b = W # b = radius of cylinder
    elipse = Elipse3D(elipse_c, [elipse_a, elipse_b], circle.plane)
    # print(elipse, '\n', circle)
    # TIME_SSC, last_time = tim(TIME_SSC, last_time, "Created Elipse")

    P1, P2 = intersect_circle(elipse, circle) 
    # TIME_SSC, last_time = tim(TIME_SSC, last_time, "Intersect circle")
    
    # print(parse_TIME(TIME_SSC))
    # P2 = 0
    return P1, P2, circle, cylinder, elipse, elipse_a_coords, cylinder_center_line, cylinder_long_edge_line, S_P1P0, S_P1P2




def plot_elipse(elipse: Elipse3D):
    t = np.linspace(0, 2*np.pi, 100)
    # generate 'blank' elipse at origin, on the xy-plane
    elipse_array = np.array([
        elipse.a*np.cos(t),
        elipse.b*np.sin(t),
        np.zeros(len(t)),
        ])
    elipse_array = np.concatenate((elipse_array, np.array([[5, 0, 0], [0, 5, 0]]).T ), axis=1)
    # rotate and translate elipse to the correct position
    if (elipse.plane.normal == vector_z).all():
        rotated_elipse_array = elipse_array
    else :
        origin = Vector([0, 0, 0])
        vector_norm_origin = Vector([0, 0, 1])
        vector_norm_dest = elipse.plane.normal
        rotated_elipse_array = translate_and_rotate(
            origin, elipse.point, vector_norm_origin, vector_norm_dest, elipse_array)

    # plt.plot(elipse_array[0], elipse_array[1], elipse_array[2]) # plot the original elipse, before rotation
    plt.plot(rotated_elipse_array[0], rotated_elipse_array[1], rotated_elipse_array[2])
    return rotated_elipse_array

from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def plot_triangle(ax, T, face_color = [0.5, 0.5, 1], edge_color = 'k', alpha = 0.2): 
    triangles = []
    for t in T:
        triangles.append([t.point_a, t.point_b, t.point_c])
    # ax.add_collection(Poly3DCollection(triangles))
    collection = Poly3DCollection(triangles, linewidths=0.2, edgecolors=edge_color, alpha=alpha)
    collection.set_facecolor(face_color)
    ax.add_collection3d(collection)
    return ax

# def tim(self, task_name, print_flag=False):
#     self.current_time = time.time()
#     past_time = self.current_time  - self.last_time
#     self.last_time = self.current_time
#     if print_flag == True:
#         print("Time elapsed for: ", task_name, " - ", past_time)
#     return {task_name: past_time}

import time
# def tim(TIME_LIST, task_name):
#     current_time = time.time()
#     last_time = list(TIME_LIST[-1].values())[0]
#     past_time = current_time - last_time
#     print("Time elapsed for: ", task_name, " - ", past_time)
#     TIME_LIST.append({task_name: last_time})
#     return TIME_LIST

def tim(TIME_LIST, last_time, task_name):
    current_time = time.time()
    # last_time = list(TIME_LIST[-1].values())[0]
    past_time = current_time - last_time
    # print("Time elapsed for: ", task_name, " - ", past_time*1000000, " usec")
    TIME_LIST.append({task_name: last_time})
    return TIME_LIST, current_time

# usage
# t = tim(t, "task")
# both prints out time elapsed and records down current time

def parse_TIME(A):
    duration=[]
    for i in range(len(A)-1):
        duration.append(list(A[i].values())[0]-list(A[i+1].values())[0])
    return duration

