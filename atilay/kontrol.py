
from pymavlink import mavutil
import time
# Create the connection
master = mavutil.mavlink_connection("/dev/ttyACM0",115200,wait_ready=True,time_out=30)
master.wait_heartbeat(1)
print("connected")


mode = 'MANUAL'


deger_sagSol=1500
deger_batCik=1500

sayac=0
kanal=5

sinir=20
# Create a function to send RC values
# More information about Joystick channels
# here: https://www.ardusub.com/operators-manual/rc-input-and-output.html#rc-inputs
def ileri_geriF(pwm):

    # Mavlink 2 supports up to 18 channels:65535
    # https://mavlink.io/en/messages/common.html#RC_CHANNELS_OVERRIDE
    rc_channel_values = [65535 for _ in range(8)]
    rc_channel_values[5-1] = pwm
    master.mav.rc_channels_override_send(
        master.target_system,                # target_system
        master.target_component,             # target_component
        *rc_channel_values) # RC channel list, in microseconds.
        
def bat_cikF(pwm):

    # Mavlink 2 supports up to 18 channels:65535
    # https://mavlink.io/en/messages/common.html#RC_CHANNELS_OVERRIDE
    rc_channel_values = [65535 for _ in range(8)]
    rc_channel_values[3-1] = pwm
    master.mav.rc_channels_override_send(
        master.target_system,                # target_system
        master.target_component,             # target_component
        *rc_channel_values) # RC channel list, in microseconds.
        
        
def sag_solF(pwm):


    rc_channel_values = [65535 for _ in range(8)]
    rc_channel_values[4-1] = pwm
    master.mav.rc_channels_override_send(
        master.target_system,                # target_system
        master.target_component,             # target_component
        *rc_channel_values) # RC channel list, in microseconds.  
        
if mode not in master.mode_mapping():
    print('Unknown mode : {}'.format(mode))
    print('Try:', list(master.mode_mapping().keys()))
    exit(1)

# Get mode ID
mode_id = master.mode_mapping()[mode]
# Set new mode
# master.mav.command_long_send(
#    master.target_system, master.target_component,
#    mavutil.mavlink.MAV_CMD_DO_SET_MODE, 0,
#    0, mode_id, 0, 0, 0, 0, 0) or:
# master.set_mode(mode_id) or:
master.mav.set_mode_send(
    master.target_system,
    mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
    mode_id)


ack = False
while not ack:
    # Wait for ACK command
    ack_msg = master.recv_match(type='COMMAND_ACK', blocking=True)
    ack_msg = ack_msg.to_dict()

    # Check if command in the same in `set_mode`
    if ack_msg['command'] != mavutil.mavlink.MAVLINK_MSG_ID_SET_MODE:
        continue

    # Print the ACK result !
    print(mavutil.mavlink.enums['MAV_RESULT'][ack_msg['result']].description)
    break
    




master.mav.command_long_send(
    master.target_system,
    master.target_component,
    mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
    0,
    1, 0, 0, 0, 0, 0, 0)
    
sag_sol=False
bat_cik=False
ileri_geri=True

while(True):
	dosya=open("state","r")
	state=dosya.readline()
	dosya.close()
	
	dosya=open("koordinat_x","r")
	koordinat_x=dosya.readline()
	dosya.close()
	try:
		koordinat_x=int(koordinat_x)
	except:
		koordinat_x=0

	dosya=open("koordinat_y","r")
	koordinat_y=dosya.readline()
	dosya.close()
	try:
		koordinat_y=int(koordinat_y)
	except:
		koordinat_y=0

	
	if state and koordinat_x >0:
		
		
		deger_sagSol=1500-int(koordinat_x/2)
	


	if state and koordinat_x <0:
		
		
		
		deger_sagSol=1500-int(koordinat_x/2)
	

	"""
	if keyboard.is_pressed("w") and sayac>=sinir:
		
		sayac=0
		
		ileri_geri=True
		deger+=200
		bat_cik=False
		sag_sol=False
		d=deger
	
		
	if keyboard.is_pressed("s") and sayac>=sinir:
		
		sayac=0
		ileri_geri=True
		deger-=200
		bat_cik=False
		sag_sol=False
		d=deger
	"""			
	if state and koordinat_y >0:
		
	
		
		deger_batCik=1500-int(koordinat_y/2)

	
		
	if state and koordinat_y <0:
		
		
		deger_batCik=1500-int(koordinat_y)


		
	if  deger_batCik > 1800:
		deger_batCik=1800
		
	if deger_sagSol > 1800:
		deger_sagSol=1800
		
	if deger_batCik < 1200:
		deger_batCik=1200
	if deger_sagSol < 1200:
		deger_sagSol=1200

			
	#print("PWM1 :",d," Sag Sol :",sag_sol," İleri Geri :",ileri_geri," Bat Çık :",bat_cik,"\n")
	
	if state:
		print("sag_sol :",deger_sagSol)
		sag_solF(deger_sagSol)

		
	if state:
		print("bat_cik :",deger_batCik)
		bat_cikF(deger_batCik)
	

	"""	
	if ileri_geri:
		ileri_geriF(deger)
	"""
		
			
	time.sleep(0.01)


"""
	master.mav.command_long_send(
    	master.target_system,
    	master.target_component,
    	mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
    	0,
    	1, 0, 0, 0, 0, 0, 0)
	print("motors arming")
	master.motors_armed_wait()
	print("armed\n")
	"""

	





