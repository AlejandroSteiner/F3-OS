const VGA_BUFFER: *mut u8 = 0xb8000 as *mut u8;
const VGA_WIDTH: usize = 80;
const VGA_HEIGHT: usize = 25;

static mut COL: usize = 0;
static mut ROW: usize = 0;

pub fn clear() {
    unsafe {
        for i in 0..(VGA_WIDTH * VGA_HEIGHT) {
            *VGA_BUFFER.add(i * 2) = b' ';
            *VGA_BUFFER.add(i * 2 + 1) = 0x0f;
        }
        COL = 0;
        ROW = 0;
    }
}

fn scroll() {
    unsafe {
        for row in 1..VGA_HEIGHT {
            for col in 0..VGA_WIDTH {
                let src = (row * VGA_WIDTH + col) * 2;
                let dst = ((row - 1) * VGA_WIDTH + col) * 2;
                *VGA_BUFFER.add(dst) = *VGA_BUFFER.add(src);
                *VGA_BUFFER.add(dst + 1) = *VGA_BUFFER.add(src + 1);
            }
        }
        for col in 0..VGA_WIDTH {
            let pos = ((VGA_HEIGHT - 1) * VGA_WIDTH + col) * 2;
            *VGA_BUFFER.add(pos) = b' ';
            *VGA_BUFFER.add(pos + 1) = 0x0f;
        }
        if ROW > 0 {
            ROW -= 1;
        }
    }
}

fn put_char(c: u8) {
    unsafe {
        if c == b'\n' {
            COL = 0;
            ROW += 1;
            if ROW >= VGA_HEIGHT {
                scroll();
            }
        } else {
            let pos = (ROW * VGA_WIDTH + COL) * 2;
            *VGA_BUFFER.add(pos) = c;
            *VGA_BUFFER.add(pos + 1) = 0x0f;
            COL += 1;
            if COL >= VGA_WIDTH {
                COL = 0;
                ROW += 1;
                if ROW >= VGA_HEIGHT {
                    scroll();
                }
            }
        }
    }
}

pub fn print(s: &str) {
    for byte in s.bytes() {
        put_char(byte);
    }
}

