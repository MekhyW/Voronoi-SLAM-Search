import rospy, random

from geometry_msgs.msg import Twist, Vector3
from std_msgs.msg import Empty
from nav_msgs.msg import Odometry

def escutou(info):
    global x,y,z
    x = info.pose.pose.position.x
    y = info.pose.pose.position.y
    z = info.pose.pose.position.z


if __name__ == "__main__":
    rospy.init_node("print_odom")
    
    state = "INI"
    x = None
    y = None
    z = None

    saida_vel = rospy.Publisher("/cmd_vel",Twist,queue_size=3)
    escuta_odom = rospy.Subscriber("/odom",Odometry,queue_size=3,callback=escutou)
    rospy.sleep(1.0)

    while not rospy.is_shutdown():

        if state == "INI":
            ang = random.randint(0,359)
            roda = Twist(Vector3(0,0,0),Vector3(0,0,-ang*0.0175))
            saida_vel.publish(roda)
            rospy.sleep(1.0)
            state = "ANDA"
            x_ini, y_ini, z_ini = x, y, z

        if state == "ANDA":
            frente = Twist(Vector3(0.1,0,0),Vector3(0,0,0))
            saida_vel.publish(frente)
            rospy.sleep(1.0)
            if x - x_ini > 1.33 or x - x_ini < -1.33:
                para =  Twist(Vector3(0,0,0),Vector3(0,0,0))
                saida_vel.publish(para)
                rospy.sleep(2.0)
                print(x-x_ini)
                state = "PARA"
