#!/usr/bin/env python3

# this is binary spliter encoder

def darwin():
    with open("spliter.darwin.bin", "rb") as f:
        with open("spliter.darwin.sh", "wb") as w:
            w.write((
                "darwin(){\n" + process(f.read()) + "\n}\n"
            ).encode("ascii"))
def elfx64():
    with open("spliter.elfx64.bin", "rb") as f:
        f.read(8)
        with open("spliter.elfx64.sh", "wb") as w:
            w.write((
                "printelfx64tail(){\n" + process(f.read()) + "\n}\n"
                + "elf0x64(){\np '\\177ELF\\002\\001\\001\\0'; printelfx64tail;\n}\n"
                + "elf9x64(){\np '\\177ELF\\002\\001\\001\\011'; printelfx64tail;\n}\n"
            ).encode("ascii"))
def elfaa64():
    with open("spliter.elfaa64.bin", "rb") as f:
        f.read(8)
        with open("spliter.elfaa64.sh", "wb") as w:
            w.write((
                "printelfaa64tail(){\n" + process(f.read()) + "\n}\n"
                + "elf0aa64(){\np '\\177ELF\\002\\001\\001\\0'; printelfaa64tail;\n}\n"
                + "elf9aa64(){\np '\\177ELF\\002\\001\\001\\011'; printelfaa64tail;\n}\n"
            ).encode("ascii"))
            

def process(data):
    parts = [None]
    for c in data:
        if c == 0:
            if isinstance(parts[-1], int):
                parts[-1] += 1
            else:
                parts.append(1)
            continue
        s = ""
        if c == ord('\\'):
            s = '\\\\'
        elif c < 0x20 or c > 0x7e or c == ord(' ') or c == ord('`') or c == ord("'") or c == ord("%"):
            s="\\%.03o" % c
        else:
            s = chr(c)
        if isinstance(parts[-1], str):
            parts[-1] += s
        else:
            parts.append(s)
        continue

    #print(parts)

    parts2=[]
    lastis_0 = False
    for part in parts[1:]:
        if isinstance(part, int):
            #zeros.append(part)
            l = part
            while l>0:
                if l>=1024:
                    parts2.append(10)
                    l -= 1024
                elif l>=128:
                    parts2.append(7)
                    l -= 128
                elif l>=8:
                    parts2.append(3)
                    l -= 8
                elif l>=4:
                    parts2.append(2)
                    l -= 4
                else:
                    parts2.append("\\0" * l)
                    break
            lastis_0 = True
        elif isinstance(part, str):
            if lastis_0 == True and part[0] in "1234567890abcdefABCDEF":
                parts2.append("\\%.03o" % ord(part[0]))
                parts2.append(part[1:])
            else:
                parts2.append(part)
            lastis_0 = False

    #print(parts2)

    parts3 = [None]
    for part in parts2:
        if isinstance(part, str) and isinstance(parts3[-1], str) and len(parts3[-1]) < 128:
            parts3[-1]+=part
        else:
            parts3.append(part)

    #print(parts3)

    ret = ""
    for part in parts3[1:]:
        if isinstance(part, int):
            ret += "z%d\n" % part
        elif isinstance(part, str):
            ret += "p '" + part +"'\n"
            pass
    
    #print(ret.encode())
    return ret


if __name__ == "__main__":
    elfx64()
    darwin()