import array

class VDP:
    def __init__(self, GG = True):
        self.GG = GG
        self.registers = array.array('B', [0] * 16) # * 11
        self.vram = array.array('B', [0] * 16 * 1024)
        if GG:
            self.cram = array.array('B', [0] * 64)
        else:
            self.cram = array.array('B', [0] * 32)
        
        self.INT = 0
        self.OVR = 0
        self.COL = 0

        self.first = False
        self.control = [0, 0]

        self.command = 0
        self.address = 0

        self.mode = 0
        self.table_address = 0
        self.table_base_address = 0
        self.lines = 240
        self.sprite_height = 8
        self.sprite_zoom = False
        self.line_interrupt_enabled = False
        self.frame_interrupt_enabled = False
        self.display_visible = False
        self.overscan_color = 0
        self.bg_scroll_x = 0
        self.bg_scroll_y = 0
        self.line_counter = 0
        

    def calculate_state(self):

        self.line_interrupt_enabled = (self.registers[0] & 16) > 0
        
        if self.registers[0] & 4:
            self.mode = 4

            self.display_visible = (self.registers[1] & 64) > 0
            self.frame_interrupt_enabled = (self.registers[1] & 32) > 0
            if self.registers[1] & 8:
                self.lines = 240
            if self.registers[1] & 16:
                self.lines = 224
            if self.registers[1] & 2:
                self.sprite_height = 16
            else:
                self.sprite_height = 8
            self.sprite_zoom = (self.registers[1] & 1) > 0
            
            self.table_address = ((self.registers[2] >> 1) & 5) << 11

            self.table_base_address = ((self.registers[5] >> 1) & 63) << 8

            self.overscan_color = self.registers[6] & 15

            self.bg_scroll_x = self.registers[8]
            self.bg_scroll_y = self.registers[9]
            self.line_counter = self.registers[10]
        else:
            self.mode = 0
        

    def print_state(self):
        print "Mode", self.mode
        print "Visible", self.display_visible
        print "Table address: " + format(self.table_address, "04x")
        print "Table base address: " + format(self.table_base_address, "04x")
        print "lines:", self.lines
        print "sprite:", self.sprite_height, self.sprite_zoom
        print "Line interrupt:", self.line_interrupt_enabled
        print "Frame interrupt:", self.frame_interrupt_enabled
        print "overscan color:", self.overscan_color
        print "background scroll:", self.bg_scroll_x, self.bg_scroll_y
        print "line counter:", self.line_counter


    def regs(self):
        r = ""
        for i in range(12):
            r += format(self.registers[i], "02x") + " "
            if i != 0 and (i % 2) == 1:
                r += "\n"
        r += "\nA:"+format(self.address, "04x")
        return r

    def palette(self):
        p = ""
        for c in self.cram:
            p += format(c, "02x") + " "
        return p

    def dump_mem(self, start = 0, size = 16 * 1024):
        for i in xrange(start, start + size):
            if i > 16 * 1024:
                break
            if i % 16 == 0:
                print "\n" +  addr2str(i) + ":",
            print format(self.vram[i], "02x"),
        print

    def get_status(self):
        return (self.INT << 7) | (self.OVR << 6) | (self.COL << 5)

    def read_control(self):
        s = self.get_status()
        self.INT = False
        return s

    def write_control(self, value):
        if self.first:
            self.control[1] = value
            self.first = False
            self.execute_command()
        else:
            self.control[0] = value
            self.first = True

    def read_data(self):
        return 0

    def write_data(self, value):
        if self.command == 0:
            self.vram[self.address] = value
        elif self.command == 1:
            self.vram[self.address] = value
        elif self.command == 3:
            self.cram[self.address] = value
        self.address = (self.address + 1) & (16 * 1024)

    def execute_command(self):
        self.command = self.control[1] >> 6
        if self.command == 0 or self.command == 1:
            self.address = self.control[0] | ((self.control[1] & 0x3F) << 8)
            #print "VDP Command: " + format(self.command, "02b") + " " + format(self.address, "04x")
        elif self.command == 2:
            r = self.control[1] & 0xf
            self.registers[r] = self.control[0]
            #print "reg write: ", r, format(self.control[0], "02x")
            self.calculate_state()
        elif self.command == 3:
            self.address = self.control[0]
            #print "to cram"

