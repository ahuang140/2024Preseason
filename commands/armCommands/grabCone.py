#from subsystems.climbingsubsystem import ClimbingSubsystem
import commands2


class grabCone(commands2.CommandBase):
    def __init__(self, angle, arm: ArmSubsystem) -> None:
        super().__init__()
        self.angle = angle
        self.arm= arm

    def initialize(self):
        pass

    def execute(self) -> None:
        speed = 0.3
        angle = 88
        self.arm.setGrabbingArmAngle(self.angle,speed)

    def end(self, interrupted: bool) -> None:
        self.arm.setGrabbingArmSpeedWithAuto(0)

    def isFinished(self) -> bool:
        return (self.angle - self.arm.tolerance <= self.arm.grabbingArmEncoderDegrees or self.angle + self.arm.tolerance >= self.arm.grabbingArmEncoderDegrees)