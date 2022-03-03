#
# See the documentation for more details on how this works
#
# The idea here is you provide a simulation object that overrides specific
# pieces of WPILib, and modifies motors/sensors accordingly depending on the
# state of the simulation. An example of this would be measuring a motor
# moving for a set period of time, and then changing a limit switch to turn
# on after that period of time. This can help you do more complex simulations
# of your robot code without too much extra effort.
#
import wpilib
import wpilib.simulation
from wpimath.system import LinearSystemId
from wpimath.system.plant import DCMotor
from robot import MyRobot
import constants

from pyfrc.physics.core import PhysicsInterface


class PhysicsEngine:
    """
    Simulates a motor moving something that strikes two limit switches,
    one on each end of the track. Obviously, this is not particularly
    realistic, but it's good enough to illustrate the point
    """

    def __init__(self, physics_controller: PhysicsInterface, robot: "MyRobot"):

        self.physics_controller = physics_controller

        # Motors
        self.l_motor = wpilib.simulation.PWMSim(1)
        self.r_motor = wpilib.simulation.PWMSim(2)
        self.system = LinearSystemId.identifyDrivetrainSystem(1.98, 0.2, 1.5, 0.3)
        self.drivesim = wpilib.simulation.DifferentialDrivetrainSim(
            self.system,
            constants.kTrackWidth,
            DCMotor.CIM(constants.kDriveTrainMotorCount),
            constants.kGearingRatio,
            constants.kWheelRadius,
        )
        # print()
        # robot.container.drive.sd.putValue("simcollection",robot.container.drive.left1.getSimCollection())
        self.leftEncoderSim = robot.container.drive.left1.getSimCollection()
        self.rightEncoderSim = robot.container.drive.right1.getSimCollection()
        # self.leftEncoderSim = wpilib.simulation.EncoderSim.createForChannel(
        #     constants.kLeftEncoderPorts[0]
        # )
        # wpilib.simulation.EncoderSim.cou
        # self.rightEncoderSim = wpilib.simulation.EncoderSim().createForChannel(
        #     constants.kRightEncoderPorts[0]
        # )

    def update_sim(self, now: float, tm_diff: float) -> None:
        """
        Called when the simulation parameters for the program need to be
        updated.

        :param now: The current time as a float
        :param tm_diff: The amount of time that has passed since the last
                        time that this function was called
        """

        # Simulate the drivetrain
        l_motor = self.l_motor.getSpeed()
        r_motor = self.r_motor.getSpeed()

        voltage = wpilib.RobotController.getInputVoltage()
        self.drivesim.setInputs(l_motor * voltage, r_motor * voltage)
        self.drivesim.update(tm_diff)
        print("ayo")
        print(self.drivesim.getLeftPosition())
        print()
        self.leftEncoderSim.setQuadratureRawPosition(int(self.drivesim.getLeftPosition() * 39.37))
        self.rightEncoderSim.setQuadratureRawPosition(int(self.drivesim.getRightPosition() * 39.37))
        self.leftEncoderSim.setQuadratureVelocity(int(self.drivesim.getLeftVelocity() * 39.37))
        self.rightEncoderSim.setQuadratureVelocity(int(self.drivesim.getRightVelocity() * 39.37))
        # self.leftEncoderSim.setDistance(self.drivesim.getLeftPosition() * 39.37)
        # self.leftEncoderSim.setRate(self.drivesim.getLeftVelocity() * 39.37)
        # self.rightEncoderSim.setDistance(self.drivesim.getRightPosition() * 39.37)
        # self.rightEncoderSim.setRate(self.drivesim.getRightVelocity() * 39.37)

        self.physics_controller.field.setRobotPose(self.drivesim.getPose())
