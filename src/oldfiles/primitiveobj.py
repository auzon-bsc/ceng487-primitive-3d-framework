
# @staticmethod
# def sphere(radius, sector_count, stack_count):
#   point_arr = []
#   for stack_step in range(stack_count + 1):
#     sector_arr = []
#     for sector_step in range(sector_count + 1):
#       theta = (2 * math.pi) * (sector_step / sector_count)
#       phi = (math.pi / 2) - (math.pi * stack_step / stack_count)

#       x = radius * math.cos(phi) * math.cos(theta)
#       y = radius * math.cos(phi) * math.sin(theta)
#       z = radius * math.sin(phi)
#       w = 1

#       tmp_vec = Vec3d(x, y, z, w)
#       sector_arr.append(tmp_vec)
#     point_arr.append(sector_arr)

#   poly_arr = []
#   for i in range(sector_count):
#     for j in range(stack_count):
#       tmp_arr = []
#       tmp_arr.append(point_arr[i][j].clone())
#       tmp_arr.append(point_arr[i+1][j].clone())
#       tmp_arr.append(point_arr[i+1][j+1].clone())
#       tmp_arr.append(point_arr[i][j+1].clone())
#       poly_arr.append(tmp_arr)

#   return Obj3d(poly_arr)

# @staticmethod
# def cylinder(radius, height, sector_count):
#   top_points = []
#   bot_points = []

#   for sector_step in range(sector_count + 1):
#     theta = (2 * math.pi) * (sector_step / sector_count)
#     x = radius * math.cos(theta)
#     z = radius * math.sin(theta)
#     y = height / 2
#     w = 1
#     top_points.append(Vec3d(x, y, z, w))
#     bot_points.append(Vec3d(x, -y, z, w))

#   poly_arr = []

#   poly_arr.append(top_points)

#   for i in range(sector_count):
#     quad_points = []
#     quad_points.append(top_points[i].clone())
#     quad_points.append(bot_points[i].clone())
#     quad_points.append(bot_points[i+1].clone())
#     quad_points.append(top_points[i+1].clone())
#     poly_arr.append(quad_points)

#   poly_arr.append(bot_points)

#   return Obj3d(poly_arr)

# @staticmethod
# def square(a, sector_count):
#   poly_arr = []   # array of polygons/vertice arrays
#   pivot_vertice = Vec3d(-(a/2),(a/2),0,1)
#   point_arr = []
#   for i in range(sector_count + 1):
#     tmp_arr = []

#     offset_y = a * i / sector_count   # offset_y
#     for j in range(sector_count + 1):
#       offset_x = a * j / sector_count   # offset_x
#       tmp_v = pivot_vertice.clone()
#       tmp_v.x += offset_x
#       tmp_v.y -= offset_y
#       tmp_arr.append(tmp_v)
#     point_arr.append(tmp_arr)

#   for i in range(sector_count):
#     for j in range(sector_count):
#       tmp_arr = []
#       tmp_arr.append(point_arr[i][j])
#       tmp_arr.append(point_arr[i][j+1])
#       tmp_arr.append(point_arr[i+1][j+1])
#       tmp_arr.append(point_arr[i+1][j])
#       poly_arr.append(Poly(tmp_arr))

#   s1 = Obj3d(copy.deepcopy(poly_arr))   # Surface 1
#   s2 = Obj3d(copy.deepcopy(poly_arr))
#   s3 = Obj3d(copy.deepcopy(poly_arr))
#   s4 = Obj3d(copy.deepcopy(poly_arr))
#   s5 = Obj3d(copy.deepcopy(poly_arr))
#   s6 = Obj3d(copy.deepcopy(poly_arr))

#   s1.translate(0, 0, a/2)

#   s2.translate(0, 0, -a/2)

#   s3.rotate("y", Vec3d(0, 0, 0), 90)
#   s3.translate(a/2, 0, 0)

#   s4.rotate("y", Vec3d(0, 0, 0), -90)
#   s4.translate(-a/2, 0, 0)

#   s5.rotate("x", Vec3d(0, 0, 0), 90)
#   s5.translate(0, a/2, 0)

#   s6.rotate("x", Vec3d(0, 0, 0), -90)
#   s6.translate(0, -a/2, 0)

#   return Obj3d(poly_arr)
