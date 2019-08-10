# automatically generated by the FlatBuffers compiler, do not modify

# namespace: FBOutput

import tdw.flatbuffers

class AvatarSegmentationColor(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsAvatarSegmentationColor(cls, buf, offset):
        n = tdw.flatbuffers.encode.Get(tdw.flatbuffers.packer.uoffset, buf, offset)
        x = AvatarSegmentationColor()
        x.Init(buf, n + offset)
        return x

    # AvatarSegmentationColor
    def Init(self, buf, pos):
        self._tab = tdw.flatbuffers.table.Table(buf, pos)

    # AvatarSegmentationColor
    def Id(self):
        o = tdw.flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

    # AvatarSegmentationColor
    def EnvId(self):
        o = tdw.flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.Get(tdw.flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 0

    # AvatarSegmentationColor
    def SegmentationColor(self):
        o = tdw.flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            x = o + self._tab.Pos
            from .Color import Color
            obj = Color()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

def AvatarSegmentationColorStart(builder): builder.StartObject(3)
def AvatarSegmentationColorAddId(builder, id): builder.PrependUOffsetTRelativeSlot(0, tdw.flatbuffers.number_types.UOffsetTFlags.py_type(id), 0)
def AvatarSegmentationColorAddEnvId(builder, envId): builder.PrependInt32Slot(1, envId, 0)
def AvatarSegmentationColorAddSegmentationColor(builder, segmentationColor): builder.PrependStructSlot(2, tdw.flatbuffers.number_types.UOffsetTFlags.py_type(segmentationColor), 0)
def AvatarSegmentationColorEnd(builder): return builder.EndObject()
