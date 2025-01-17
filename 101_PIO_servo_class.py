from machine import Pin
from rp2 import PIO, asm_pio, StateMachine

PIN_SRV1 = 20
PIN_SRV2 = 21


class ServoMngr:
    instances = []

    @classmethod
    def _get_free_sm(cls, lst):
        return sorted(set(range(8)) - set(lst))

    @classmethod
    def get_servo(cls, pin, init_angle=0, id=None):
        if id == None:
            if len(ServoMngr.instances) == 0:
                id = 0
            else:
                free_list = ServoMngr._get_free_sm(
                    [int(str(inst.sm)[-2]) for inst in ServoMngr.instances]
                )
                if len(free_list) > 0:
                    id = free_list[0]
                else:
                    raise IndexError("no more free state machines")

        elif id in range(8):
            if id in [int(str(inst.sm)[-2]) for inst in ServoMngr.instances]:
                raise IndexError("ID already in use")
        else:
            raise ValueError("non-existent state machine ID")

        servo = Servo(pin, init_angle, id=id)
        ServoMngr.instances.append(servo)
        return servo

    @classmethod
    def kill_servo(cls, servo):
        servo.off()
        ServoMngr.instances.remove(servo)
        del servo


class Servo:
    _FREQ = 2_000_000
    _PERIOD = 19_000

    @asm_pio(out_init=PIO.OUT_LOW, set_init=PIO.OUT_LOW, out_shiftdir=PIO.SHIFT_RIGHT)
    def set_a_sm():
        wrap_target()  # type: ignore # noqa
        mov(x, osr)  # type: ignore #noqa
        mov(y, isr)  # type: ignore  #noqa
        set(pins, 0)  # type: ignore  #noqa

        label("time loop")  # 1ms loop @ freq=2MHz # type: ignore  #noqa
        jmp(x_not_y, "next")  # type: ignore  #noqa
        set(pins, 1)  # type: ignore  #noqa
        nop()  # type: ignore  #noqa
        label("next")  # type: ignore  #noqa
        jmp(y_dec, "time loop")  # type: ignore  #noqa
        wrap()  # type: ignore  #noqa

    def __init__(self, pin, init_angle=0, id=0):
        self._delay = 2_000
        self._init_angle = init_angle
        self.id = id
        self.sm = StateMachine(
            self.id, Servo.set_a_sm, freq=Servo._FREQ, set_base=Pin(pin)
        )
        self.on()
        self.sm.put(Servo._PERIOD)
        self.sm.exec("pull()")
        self.sm.exec("mov(isr, osr)")
        self.set(self._init_angle)

    def on(self):
        self.sm.active(1)

    def off(self):
        self.sm.exec("set(pins, 0)")
        self.sm.active(0)
        self.sm.exec("set(pins, 0)")

    def _d2pw(self, angle):
        return int(angle * 2000 / 180 + 500)

    def set(self, angle):
        self.sm.put(self._d2pw(angle))
        self.sm.exec("pull()")

    def reset(self):
        self.set(self._init_angle)


if __name__ == "__main__":
    from time import sleep_us

    deg_jmp = 2

    try:
        servo1 = ServoMngr.get_servo(PIN_SRV1)
        servo2 = ServoMngr.get_servo(PIN_SRV2, init_angle=180, id=5)
        servo1.off()
        servo2.off()
        servo1.on()
        servo2.on()
        while True:
            for i in range(0, 180, deg_jmp):
                servo1.set(i)
                servo2.set(180 - i)
                sleep_us(self._delay)

            for i in range(180, 0, -deg_jmp):
                servo1.set(i)
                servo2.set(180 - i)

    except KeyboardInterrupt:
        for i in range(2):
            servo1.reset()
            servo2.reset()
        servo1.off()
        servo2.off()
