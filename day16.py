from typing import List, Tuple
from dataclasses import dataclass
from functools import reduce

def hex_char_to_bin(hex_char: str) -> str:
    """Convert a hex character to a binary string."""
    return bin(int(hex_char, 16))[2:].zfill(4)

def hex_to_bin(hex_str: str) -> str:
    """Convert a hex string to a binary string."""
    return ''.join(hex_char_to_bin(hex_char) for hex_char in hex_str)

assert hex_to_bin('D2FE28') == '110100101111111000101000'

@dataclass
class Packet:
    version: int
    type_id: int
    subpackets: List['Packet'] = ()
    value: int = None
    op: str = None

    def sum_of_versions(self) -> int:
        return self.version + sum(packet.sum_of_versions() for packet in self.subpackets)

    def evaluate(self) -> int:
        if self.type_id == 0:
            # sum packet
            return sum(packet.evaluate() for packet in self.subpackets)
        elif self.type_id == 1:
            # product packet
            return reduce(lambda x, y: x * y, (packet.evaluate() for packet in self.subpackets))
        elif self.type_id == 2:
            # minimum packet
            return min(packet.evaluate() for packet in self.subpackets)
        elif self.type_id == 3:
            # maximum packet
            return max(packet.evaluate() for packet in self.subpackets)
        elif self.type_id == 4:
            # literal value
            return self.value
        elif self.type_id == 5:
            # greater than packet
            assert len(self.subpackets) == 2
            return 1 if self.subpackets[0].evaluate() > self.subpackets[1].evaluate() else 0
        elif self.type_id == 6:
            # less than packet
            assert len(self.subpackets) == 2
            return 1 if self.subpackets[0].evaluate() < self.subpackets[1].evaluate() else 0
        elif self.type_id == 7:
            # equal to packet
            assert len(self.subpackets) == 2
            return 1 if self.subpackets[0].evaluate() == self.subpackets[1].evaluate() else 0
        else:
            raise ValueError(f'Unknown packet type: {self.type_id}')

def parse(byt3s: str, start: int = 0) -> Tuple['Packet', int]:
    """Parse a packet from a byt3s string."""
    # check for all zeros
    if all(byt3s[i] == '0' for i in range(start, len(byt3s))):
        return None

    version = int(byt3s[start:start+3], 2)
    type_id = int(byt3s[start+3:start+6], 2)
    start += 6

    if type_id == 4:
        # literal
        digits = []
        while byt3s[start] == '1':
            digits.append(byt3s[start+1:start+5])
            start += 5
        # and now we have the last byte
        digits.append(byt3s[start+1:start+5])
        start += 5

        value = int(''.join(digits), 2)

        packet = Packet(version, type_id, value=value)
        return packet, start

    else:
        # operator
        length_type_id = byt3s[start]
        start += 1
        nsp = tlib = None
        if length_type_id == '0':
            tlib = int(byt3s[start:start+15], 2)
            start += 15
            end = start + tlib

            subpackets = []
            while True:
                subpacket, start = parse(byt3s, start)
                if subpacket is None:                   
                    break
                subpackets.append(subpacket)
                if start >= end:
                    break
            packet = Packet(version, type_id, subpackets=subpackets)
            return packet, start

        elif length_type_id == '1':
            nsp = int(byt3s[start:start+11], 2)
            start += 11
            subpackets = []

            while len(subpackets) < nsp:
                subpacket, start = parse(byt3s, start)
                subpackets.append(subpacket)
            packet = Packet(version, type_id, subpackets=subpackets)
            return packet, start
        else:
            raise ValueError(f'Unknown length type id: {length_type_id}')

def add_up_all_version_numbers(hex_string: str) -> int:
    """Add up all version numbers in a hex string."""
    byt3s = hex_to_bin(hex_string)
    packet, _ = parse(byt3s)
    return packet.sum_of_versions()

assert add_up_all_version_numbers('8A004A801A8002F478') == 16
assert add_up_all_version_numbers('620080001611562C8802118E34') == 12
assert add_up_all_version_numbers('C0015000016115A2E0802F182340') == 23
assert add_up_all_version_numbers('A0016C880162017C3686B18A3D4780') == 31

def evaluate(hex_str: str) -> int:
    """Evaluate a hex string."""
    byt3s = hex_to_bin(hex_str)
    packet, _ = parse(byt3s)
    return packet.evaluate()

assert evaluate('C200B40A82') == 3
assert evaluate('04005AC33890') == 54
assert evaluate('880086C3E88112') == 7
assert evaluate('CE00C43D881120') == 9
assert evaluate('D8005AC2A8F0') == 1
assert evaluate('F600BC2D8F') == 0
assert evaluate('9C005AC2F8F0') == 0
assert evaluate('9C0141080250320F1802104A08') == 1

if __name__ == "__main__":
    raw = """220D790065B2745FF004672D99A34E5B33439D96CEC80373C0068663101A98C406A5E7395DC1804678BF25A4093BFBDB886CA6E11FDE6D93D16A100325E5597A118F6640600ACF7274E6A5829B00526C167F9C089F15973C4002AA4B22E800FDCFD72B9351359601300424B8C9A00BCBC8EE069802D2D0B945002AB2D7D583E3F00016B05E0E9802BA00B4F29CD4E961491CCB44C6008E80273C393C333F92020134B003530004221347F83A200D47F89913A66FB6620016E24A007853BE5E944297AB64E66D6669FCEA0112AE06009CAA57006A0200EC258FB0440010A8A716A321009DE200D44C8E31F00010887B146188803317A3FC5F30056C0150004321244E88C000874468A91D2291802B25EB875802B28D13550030056C0169FB5B7ECE2C6B2EF3296D6FD5F54858015B8D730BB24E32569049009BF801980803B05A3B41F1007625C1C821256D7C848025DE0040E5016717247E18001BAC37930E9FA6AE3B358B5D4A7A6EA200D4E463EA364EDE9F852FF1B9C8731869300BE684649F6446E584E61DE61CD4021998DB4C334E72B78BA49C126722B4E009C6295F879002093EF32A64C018ECDFAF605989D4BA7B396D9B0C200C9F0017C98C72FD2C8932B7EE0EA6ADB0F1006C8010E89B15A2A90021713610C202004263E46D82AC06498017C6E007901542C04F9A0128880449A8014403AA38014C030B08012C0269A8018E007A801620058003C64009810010722EC8010ECFFF9AAC32373F6583007A48CA587E55367227A40118C2AC004AE79FE77E28C007F4E42500D10096779D728EB1066B57F698C802139708B004A5C5E5C44C01698D490E800B584F09C8049593A6C66C017100721647E8E0200CC6985F11E634EA6008CB207002593785497652008065992443E7872714"""
    packet, _ = parse(hex_to_bin(raw))
    print(packet.sum_of_versions())
    print(packet.evaluate())