import math


image_width = 
image_height = 
horizontal_fov, vertical_fov = 78
image_cx = image_width/2
image_cy = image_height/2
fov_pixel_ratio_x = horizontal_fov/image_width
fov_pixel_ratio_y = vertical_fov/image_height

R = 6371000
camera_heading = 180
bearing = (camera_heading + detection_bearing_x)*(math.pi/180.0)

lat_camera = math.radians(camera_lat)
lon_camera = math.radians(camera_lon)

X = math.cos(plane_lat)*math.sin(plane_lon-lon_camera)
Y = math.cos(lat_camera)*math.sin(lon_camera) - math.sin(lat_camera)*math.cos(lon_camera)*math.cos(plane_lon-lon_camera)
detection_bearing_x = math.atan2(X,Y)

A = math.pow(math.sin((plane_lat-lat_camera)/2),2) 
B = math.cos(lat_camera)*math.cos(plane_lat)*math.pow(math.sin((plane_lon-lon_camera)/2))
dif_dist = 2*R*math.asin(math.sqrt(A+B))

detection_elevation_y = math.tan((plane_alt-camera_alt)/dif_dist)*(180.0/math.pi)

diff_x = detection_bearing_x/fov_pixel_ratio_x
diff_y = detection_elevation_y/fov_pixel_ratio_y

#insert conditional if statements for location in qu

plane_cx = diff_x+image_cx
plane_cy = diff_y+image_cy