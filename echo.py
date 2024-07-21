import betterproto

from tinkoff.invest.grpc.instruments_pb2 import GetBondEventsResponse


message = GetBondEventsResponse.BondEvent(instrument_id="asd")
# serialize message using betterproto
serialized = message.SerializeToString()
print(serialized)

# deserialize serialized BondEvent into BondEvent
deserialized = GetBondEventsResponse.BondEvent.FromString(serialized)
print(serialized)

