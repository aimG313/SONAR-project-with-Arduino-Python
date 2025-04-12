add_library('serial')

# Global variables
simulate = False     # Set to True to simulate data; False to use real serial data
iAngle = 90          # Start with a mid position for a 180° servo
iDistance = 25.0     # Starting distance (in cm)

# For simulation (180° servo movement)
servo_direction = 1  # 1 = increasing angle, -1 = decreasing
servo_speed = 1      # Degrees to move per frame

def setup():
    size(1200, 700)  # Change this to your screen resolution
    smooth()
    if not simulate:
        global myPort
        myPort = Serial(this, "COM3", 9600)  # Adjust COM port and baud rate as needed
        myPort.bufferUntil(ord('.'))         # Listen until the ASCII value for '.' is received

def draw():
    global iAngle, iDistance, servo_direction, servo_speed
    # Create a fade effect for motion blur
    noStroke()
    fill(0, 4)
    rect(0, 0, width, height - height * 0.065)
    
    if simulate:
        # Simulate servo: oscillate angle between 0 and 180 degrees
        iAngle += servo_direction * servo_speed
        if iAngle >= 180 or iAngle <= 0:
            servo_direction *= -1
            iAngle = constrain(iAngle, 0, 180)
        # Simulate distance as a function of angle (example: sine-based variation)
        iDistance = 25 + 15 * sin(radians(iAngle))
        print("Simulated -> Angle:", iAngle, "Distance:", iDistance)
    
    drawRadar()
    drawLine()
    drawObject()
    drawText()

def serialEvent(myPort):
    global iAngle, iDistance
    data = myPort.readStringUntil(ord('.'))
    if data:
        data = data[:-1]  # Remove the trailing delimiter ('.')
        index1 = data.find(",")
        if index1 != -1:
            angle_str = data[:index1]
            distance_str = data[index1+1:]
            try:
                iAngle = int(angle_str)
                iDistance = float(distance_str)
                print("Received -> Angle:", iAngle, "Distance:", iDistance)
            except Exception as e:
                print("Error parsing data:", e)

def drawRadar():
    pushMatrix()
    translate(width/2, height - height * 0.074)  # Move to radar's center
    noFill()
    strokeWeight(2)
    stroke(98, 245, 31)
    # Draw radar arc lines
    arc(0, 0, (width - width * 0.0625), (width - width * 0.0625), PI, TWO_PI)
    arc(0, 0, (width - width * 0.27), (width - width * 0.27), PI, TWO_PI)
    arc(0, 0, (width - width * 0.479), (width - width * 0.479), PI, TWO_PI)
    arc(0, 0, (width - width * 0.687), (width - width * 0.687), PI, TWO_PI)
    # Draw angle lines
    line(-width/2, 0, width/2, 0)
    line(0, 0, (-width/2) * cos(radians(30)), (-width/2) * sin(radians(30)))
    line(0, 0, (-width/2) * cos(radians(60)), (-width/2) * sin(radians(60)))
    line(0, 0, (-width/2) * cos(radians(90)), (-width/2) * sin(radians(90)))
    line(0, 0, (-width/2) * cos(radians(120)), (-width/2) * sin(radians(120)))
    line(0, 0, (-width/2) * cos(radians(150)), (-width/2) * sin(radians(150)))
    line((-width/2) * cos(radians(30)), 0, width/2, 0)
    popMatrix()

def drawLine():
    pushMatrix()
    strokeWeight(9)
    stroke(30, 250, 60)
    translate(width/2, height - height * 0.074)
    # Draw the rotating line (radar sweep) based on the current angle
    line(0, 0,
         (height - height * 0.12) * cos(radians(iAngle)),
         -(height - height * 0.12) * sin(radians(iAngle)))
    popMatrix()

def drawObject():
    pushMatrix()
    translate(width/2, height - height * 0.074)
    strokeWeight(9)
    stroke(255, 10, 10)  # Red color for detected object
    # Convert sensor distance (in cm) to pixels
    pixsDistance = iDistance * ((height - height * 0.1666) * 0.025)
    # Only draw object if within 40 cm range
    if iDistance < 40:
        line(pixsDistance * cos(radians(iAngle)),
             -pixsDistance * sin(radians(iAngle)),
             (width - width * 0.505) * cos(radians(iAngle)),
             -(width - width * 0.505) * sin(radians(iAngle)))
    popMatrix()

# def drawText():
#     pushMatrix()
#     noObject = "In Range" if iDistance < 40 else "Out of Range"
#     fill(0, 0, 0)
#     noStroke()
#     rect(0, height - height * 0.0648, width, height)
#     fill(98, 245, 31)
#     textSize(25)
#     text("10cm", width - width * 0.3854, height - height * 0.0833)
#     text("20cm", width - width * 0.281, height - height * 0.0833)
#     text("30cm", width - width * 0.177, height - height * 0.0833)
#     text("40cm", width - width * 0.0729, height - height * 0.0833)
#     textSize(30)
#     text("RADAR", width - width * 0.875, height - height * 0.0277)
#     textAlign(LEFT, BASELINE)
#     text("Angle:" + str(iAngle) + "  ", width - width * 0.48, height - height * 0.0277)
#     textAlign(CENTER,BASELINE)
#     text("Distance:", width - width * 0.26, height - height * 0.0277)

#     if iDistance < 40:
#         text("        " + "{:.2f}".format(iDistance) + " cm", width - width * 0.225, height - height * 0.0277)
#     textSize(25)
#     fill(98, 245, 60)
    
#     pushMatrix()
#     translate((width - width * 0.4994) + width/2 * cos(radians(30)),
#               (height - height * 0.0907) - width/2 * sin(radians(30)))
#     rotate(-radians(-60))
#     text("30 ", 0, 0)
#     popMatrix()
    
#     pushMatrix()
#     translate((width - width * 0.503) + width/2 * cos(radians(60)),
#               (height - height * 0.0888) - width/2 * sin(radians(60)))
#     rotate(-radians(-30))
#     text("60 ", 0, 0)
#     popMatrix()
    
#     pushMatrix()
#     translate((width - width * 0.507) + width/2 * cos(radians(90)),
#               (height - height * 0.0833) - width/2 * sin(radians(90)))
#     rotate(radians(0))
#     text("90 ", 0, 0)
#     popMatrix()
    
#     pushMatrix()
#     translate(width - width * 0.513 + width/2 * cos(radians(120)),
#               (height - height * 0.07129) - width/2 * sin(radians(120)))
#     rotate(radians(-30))
#     text("120 ", 0, 0)
#     popMatrix()
    
#     pushMatrix()
#     translate((width - width * 0.5104) + width/2 * cos(radians(150)),
#               (height - height * 0.0574) - width/2 * sin(radians(150)))
#     rotate(radians(-60))
#     text("150 ", 0, 0)
#     popMatrix()
    
#     popMatrix()

def drawText():
    pushMatrix()
    # Draw a black background rectangle for the text area at the bottom
    noStroke()
    fill(0, 0, 0)
    # Using 10% of the screen height for the text background
    rect(0, height - height * 0.1, width, height * 0.1)
    
    # Main title: centered horizontally and vertically in the upper part of the text area
    fill(98, 245, 31)
    textAlign(CENTER, CENTER)
    textSize(40)
    text("RADAR Project", width/2, height - height * 0.075)
    
    # Display angle on the left side
    textAlign(LEFT, CENTER)
    textSize(25)
    text("Angle: " + str(iAngle) + " degree", width * 0.05, height - height * 0.05)
    
    # Display distance on the right side
    textAlign(RIGHT, CENTER)
    text("Distance: " + "{:.2f}".format(iDistance) + " cm", width * 0.95, height - height * 0.05)
    
    popMatrix()
