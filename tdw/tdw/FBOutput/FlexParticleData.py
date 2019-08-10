# automatically generated by the FlatBuffers compiler, do not modify

# namespace: FBOutput

import tdw.flatbuffers

class FlexParticleData(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsFlexParticleData(cls, buf, offset):
        n = tdw.flatbuffers.encode.Get(tdw.flatbuffers.packer.uoffset, buf, offset)
        x = FlexParticleData()
        x.Init(buf, n + offset)
        return x

    # FlexParticleData
    def Init(self, buf, pos):
        self._tab = tdw.flatbuffers.table.Table(buf, pos)

    # FlexParticleData
    def Id(self):
        o = tdw.flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(tdw.flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 0

    # FlexParticleData
    def Particles(self, j):
        o = tdw.flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            x = self._tab.Vector(o)
            x += tdw.flatbuffers.number_types.UOffsetTFlags.py_type(j) * 16
            from .Vector4 import Vector4
            obj = Vector4()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # FlexParticleData
    def ParticlesLength(self):
        o = tdw.flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # FlexParticleData
    def Velocities(self, j):
        o = tdw.flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            x = self._tab.Vector(o)
            x += tdw.flatbuffers.number_types.UOffsetTFlags.py_type(j) * 12
            from .Vector3 import Vector3
            obj = Vector3()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # FlexParticleData
    def VelocitiesLength(self):
        o = tdw.flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

def FlexParticleDataStart(builder): builder.StartObject(3)
def FlexParticleDataAddId(builder, id): builder.PrependInt32Slot(0, id, 0)
def FlexParticleDataAddParticles(builder, particles): builder.PrependUOffsetTRelativeSlot(1, tdw.flatbuffers.number_types.UOffsetTFlags.py_type(particles), 0)
def FlexParticleDataStartParticlesVector(builder, numElems): return builder.StartVector(16, numElems, 4)
def FlexParticleDataAddVelocities(builder, velocities): builder.PrependUOffsetTRelativeSlot(2, tdw.flatbuffers.number_types.UOffsetTFlags.py_type(velocities), 0)
def FlexParticleDataStartVelocitiesVector(builder, numElems): return builder.StartVector(12, numElems, 4)
def FlexParticleDataEnd(builder): return builder.EndObject()
