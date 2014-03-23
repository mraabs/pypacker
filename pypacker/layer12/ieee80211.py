"""IEEE 802.11"""

from pypacker import pypacker
from pypacker import triggerlist

import struct
import logging

logger = logging.getLogger("pypacker")

# Frame Types
MGMT_TYPE		= 0
CTL_TYPE		= 1
DATA_TYPE		= 2

# Frame Sub-Types
M_ASSOC_REQ		= 0
M_ASSOC_RESP		= 1
M_REASSOC_REQ		= 2
M_REASSOC_RESP		= 3
M_PROBE_REQ		= 4
M_PROBE_RESP		= 5
M_DISASSOC		= 10
M_AUTH			= 11
M_DEAUTH		= 12
M_BEACON		= 8
M_ATIM			= 9

C_BLOCK_ACK_REQ		= 8
C_BLOCK_ACK		= 9
C_PS_POLL		= 10
C_RTS			= 11
C_CTS			= 12
C_ACK			= 13
C_CF_END		= 14
C_CF_END_ACK		= 15

D_NORMAL		= 0
D_DATA_CF_ACK		= 1
D_DATA_CF_POLL		= 2
D_DATA_CF_ACK_POLL	= 3
D_NULL			= 4
D_CF_ACK		= 5
D_CF_POLL		= 6
D_CF_ACK_POLL		= 7
D_QOS_DATA		= 8
D_QOS_CF_ACK		= 9
D_QOS_CF_POLL		= 10
D_QOS_CF_ACK_POLL	= 11
D_QOS_NULL		= 12
D_QOS_CF_POLL_EMPTY	= 14

TO_DS_FLAG		= 10
FROM_DS_FLAG		= 1
INTER_DS_FLAG		= 11

# Bitshifts for Frame Control
_VERSION_MASK		= 0x0300
_TYPE_MASK		= 0x0c00
_SUBTYPE_MASK		= 0xf000
_TO_DS_MASK		= 0x0001
_FROM_DS_MASK		= 0x0002
_MORE_FRAG_MASK		= 0x0004
_RETRY_MASK		= 0x0008
_PWR_MGT_MASK		= 0x0010
_MORE_DATA_MASK		= 0x0020
_PROTECTED_MASK		= 0x0040
_ORDER_MASK		= 0x0080
_VERSION_SHIFT		= 8
_TYPE_SHIFT		= 10
_SUBTYPE_SHIFT		= 12
_TO_DS_SHIFT		= 0
_FROM_DS_SHIFT		= 1
_MORE_FRAG_SHIFT	= 2
_RETRY_SHIFT		= 3
_PWR_MGT_SHIFT		= 4
_MORE_DATA_SHIFT	= 5
_PROTECTED_SHIFT	= 6
_ORDER_SHIFT		= 7


# needed to distinguish subtypes via types
TYPE_FACTORS		= [16, 32, 64]
TYPE_FACTOR_PROTECTED	= 128

class IEEE80211(pypacker.Packet):
	__hdr__ = (
		# AAAABBCC | 00000000
		# AAAA = subtype BB = type CC = version
		("framectl", "H", 0),
		("duration", "H", 0)
	)

	def _get_version(self):
		return (self.framectl & _VERSION_MASK) >> _VERSION_SHIFT

	def _set_version(self, val):
		self.framectl = (val << _VERSION_SHIFT) | (self.framectl & ~_VERSION_MASK)

	def _get_type(self):
		return (self.framectl & _TYPE_MASK) >> _TYPE_SHIFT

	def _set_type(self, val):
		self.framectl = (val << _TYPE_SHIFT) | (self.framectl & ~_TYPE_MASK)

	def _get_subtype(self):
		return (self.framectl & _SUBTYPE_MASK) >> _SUBTYPE_SHIFT

	def _set_subtype(self, val):
		self.framectl = (val << _SUBTYPE_SHIFT) | (self.framectl & ~_SUBTYPE_MASK)

	def _get_to_ds(self):
		return (self.framectl & _TO_DS_MASK) >> _TO_DS_SHIFT

	def _set_to_ds(self, val):
		self.framectl = (val << _TO_DS_SHIFT) | (self.framectl & ~_TO_DS_MASK)

	def _get_from_ds(self):
		return (self.framectl & _FROM_DS_MASK) >> _FROM_DS_SHIFT

	def _set_from_ds(self, val):
		self.framectl = (val << _FROM_DS_SHIFT) | (self.framectl & ~_FROM_DS_MASK)

	def _get_more_frag(self):
		return (self.framectl & _MORE_FRAG_MASK) >> _MORE_FRAG_SHIFT

	def _set_more_frag(self, val):
		self.framectl = (val << _MORE_FRAG_SHIFT) | (self.framectl & ~_MORE_FRAG_MASK)

	def _get_retry(self):
		return (self.framectl & _RETRY_MASK) >> _RETRY_SHIFT

	def _set_retry(self, val):
		self.framectl = (val << _RETRY_SHIFT) | (self.framectl & ~_RETRY_MASK)

	def _get_pwr_mgt(self):
		return (self.framectl & _PWR_MGT_MASK) >> _PWR_MGT_SHIFT

	def _set_pwr_mgt(self, val):
		self.framectl = (val << _PWR_MGT_SHIFT) | (self.framectl & ~_PWR_MGT_MASK)

	def _get_more_data(self):
		return (self.framectl & _MORE_DATA_MASK) >> _MORE_DATA_SHIFT

	def _set_more_data(self, val):
		self.framectl = (val << _MORE_DATA_SHIFT) | (self.framectl & ~_MORE_DATA_MASK)

	def _get_protected(self):
		return (self.framectl & _PROTECTED_MASK) >> _PROTECTED_SHIFT

	def _set_protected(self, val):
		self.framectl = (val << _PROTECTED_SHIFT) | (self.framectl & ~_PROTECTED_MASK)

	def _get_order(self):
		return (self.framectl & _ORDER_MASK) >> _ORDER_SHIFT

	def _set_order(self, val):
		self.framectl = (val << _ORDER_SHIFT) | (self.framectl & ~_ORDER_MASK)

	version = property(_get_version, _set_version)
	type = property(_get_type, _set_type)
	subtype = property(_get_subtype, _set_subtype)
	to_ds = property(_get_to_ds, _set_to_ds)
	from_ds = property(_get_from_ds, _set_from_ds)
	more_frag = property(_get_more_frag, _set_more_frag)
	retry = property(_get_retry, _set_retry)
	pwr_mgt = property(_get_pwr_mgt, _set_pwr_mgt)
	more_data = property(_get_more_data, _set_more_data)
	protected = property(_get_protected, _set_protected)
	order = property(_get_order, _set_order)

	def _dissect(self, buf):
		self.framectl = struct.unpack(">H", buf[0:2])[0]
		protected_factor = 0

		if self.protected == 1:
			protected_factor = TYPE_FACTOR_PROTECTED
			#logger.debug("got protected packet, type/sub/prot: %d/%d/%d" %
			#	(TYPE_FACTORS[self.type], self.subtype, protected_factor))
		#logger.debug("ieee80211 lazy type is: %s" %
		#	pypacker.Packet._handler["IEEE80211"][TYPE_FACTORS[self.type] + self.subtype + protected_factor])
		self._parse_handler( TYPE_FACTORS[self.type] + self.subtype + protected_factor, buf[4:])

	#
	# mgmt frames
	#

	class Beacon(pypacker.Packet):
		__hdr__ = (
			("dst", "6s", b"\x00" * 6),
			("src1", "6s", b"\x00" * 6),
			("src2", "6s", b"\x00" * 6),
			("frag_seq", "H", 0),
			("ts", "Q", 0),
			("interval", "H", 0),
			("capa", "H", 0),
			("params", None, triggerlist.TriggerList)
		)

		dst_s = pypacker.Packet._get_property_mac("dst")
		src1_s = pypacker.Packet._get_property_mac("src1")
		src2_s = pypacker.Packet._get_property_mac("src2")

		def _dissect(self, buf):
			self.params.init_lazy_dissect(buf[32:], IEEE80211._unpack_ies)

	class ProbeReq(pypacker.Packet):
		__hdr__ = (
			("dst", "6s", b"\x00" * 6),
			("src1", "6s", b"\x00" * 6),
			("src2", "6s", b"\x00" * 6),
			("frag_seq", "H", 0),
			("params", None, triggerlist.TriggerList)
		)

		dst = pypacker.Packet._get_property_mac("dst")
		src1 = pypacker.Packet._get_property_mac("src1")
		src2 = pypacker.Packet._get_property_mac("src2")

		def _dissect(self, buf):
			self.params.init_lazy_dissect(buf[20:], IEEE80211._unpack_ies)

	class ProbeResp(Beacon):
		pass

	class AssocReq(pypacker.Packet):
		__hdr__ = (
			("dst", "6s", b"\x00" * 6),
			("src1", "6s", b"\x00" * 6),
			("src2", "6s", b"\x00" * 6),
			("frag_seq", "H", 0),
			("capa", "H", 0),
			("interval", "H", 0),
			("params", None, triggerlist.TriggerList)
		)

		dst = pypacker.Packet._get_property_mac("dst")
		src1_s = pypacker.Packet._get_property_mac("src1")
		src2_s = pypacker.Packet._get_property_mac("src2")

		def _dissect(self, buf):
			self.params.init_lazy_dissect(buf[24:], IEEE80211._unpack_ies)

	class AssocResp(pypacker.Packet):
		__hdr__ = (
			("dst", "6s", b"\x00" * 6),
			("src1", "6s", b"\x00" * 6),
			("src2", "6s", b"\x00" * 6),
			("frag_seq", "H", 0),
			("capa", "H", 0),
			("status", "H", 0),
			("aid", "H", 0),
			("params", None, triggerlist.TriggerList)
		)

		dst_s = pypacker.Packet._get_property_mac("dst")
		src1_s = pypacker.Packet._get_property_mac("src1")
		src2_s = pypacker.Packet._get_property_mac("src2")

		def _dissect(self, buf):
			self.params.init_lazy_dissect(buf[26:], IEEE80211._unpack_ies)

	class Disassoc(pypacker.Packet):
		__hdr__ = (
			("dst", "6s", b"\x00" * 6),
			("src1", "6s", b"\x00" * 6),
			("src2", "6s", b"\x00" * 6),
			("frag_seq", "H", 0),
			("reason", "H", 0),
		)

		dst_s = pypacker.Packet._get_property_mac("dst")
		src1_s = pypacker.Packet._get_property_mac("src1")
		src2_s = pypacker.Packet._get_property_mac("src2")

	class ReassocReq(pypacker.Packet):
		__hdr__ = (
			("dst", "6s", b"\x00" * 6),
			("src1", "6s", b"\x00" * 6),
			("src2", "6s", b"\x00" * 6),
			("frag_seq", "H", 0),
			("capa", "H", 0),
			("interval", "H", 0),
			("current_ap", "6s", b"\x00" * 6)
		)

		dst_s = pypacker.Packet._get_property_mac("dst")
		src1_s = pypacker.Packet._get_property_mac("src1")
		src2_s = pypacker.Packet._get_property_mac("src2")

	class Auth(pypacker.Packet):
		__hdr__ = (
			("dst", "6s", b"\x00" * 6),
			("src1", "6s", b"\x00" * 6),
			("src2", "6s", b"\x00" * 6),
			("frag_seq", "H", 0),
			("algo", "H", 0),
			("auth_seq", "H", 0)
		)

		dst_s = pypacker.Packet._get_property_mac("dst")
		src1_s = pypacker.Packet._get_property_mac("src1")
		src2_s = pypacker.Packet._get_property_mac("src2")

	class Deauth(pypacker.Packet):
		__hdr__ = (
			("dst", "6s", b"\x00" * 6),
			("src1", "6s", b"\x00" * 6),
			("src2", "6s", b"\x00" * 6),
			("frag_seq", "H", 0),
			("reason", "H", 0)
		)

		dst_s = pypacker.Packet._get_property_mac("dst")
		src1_s = pypacker.Packet._get_property_mac("src1")
		src2_s = pypacker.Packet._get_property_mac("src2")

	m_decoder = {
		M_BEACON	: Beacon,
		M_ASSOC_REQ	: AssocReq,
		M_ASSOC_RESP	: AssocResp,
		M_DISASSOC	: Disassoc,
		M_REASSOC_REQ	: ReassocReq,
		M_REASSOC_RESP	: AssocResp,
		M_AUTH		: Auth,
		M_PROBE_REQ	: ProbeReq,
		M_PROBE_RESP	: ProbeResp,
		M_DEAUTH	: Deauth,
	#	M_ATIM		:
	}

	#
	# Control frames: no need for extra layer: 802.11 Base data is enough
	#

	class RTS(pypacker.Packet):
		__hdr__ = (
			("dst", "6s", b"\x00" * 6),
			("src", "6s", b"\x00" * 6)
		)

		dst_s = pypacker.Packet._get_property_mac("dst")
		src_s = pypacker.Packet._get_property_mac("src")

	class CTS(pypacker.Packet):
		__hdr__ = (
			("dst", "6s", b"\x00" * 6),
		)

		dst_s = pypacker.Packet._get_property_mac("dst")

	class ACK(pypacker.Packet):
		__hdr__ = (
			("dst", "6s", b"\x00" * 6),
		)

		dst_s = pypacker.Packet._get_property_mac("dst")

	class BlockAckReq(pypacker.Packet):
		__hdr__ = (
			("dst", "6s", b"\x00" * 6),
			("src", "6s", b"\x00" * 6),
			("reqctrl", "H", 0),
			("seq", "H", 0)
		# TODO: this contains a FCS
		)

	class BlockAck(pypacker.Packet):
		__hdr__ = (
			("dst", "6s", b"\x00" * 6),
			("src", "6s", b"\x00" * 6),
			("reqctrl", "H", 0),
			("seq", "H", 0),
			("bitmap", "Q", 0)
		# TODO: this contains a FCS
		)

	c_decoder = {
		C_RTS		: RTS,
		C_CTS		: CTS,
		C_ACK		: ACK,
		C_BLOCK_ACK_REQ	: BlockAckReq,
		C_BLOCK_ACK	: BlockAck
	}

	#
	# data frames: 4 types of Data => Data, Data+QoS, Data+Secure, Data+Secure+QoS
	#
	class Dataframe(pypacker.Packet):
		__hdr__ = (
			("dst", "6s", b"\x00" * 6),
			("src1", "6s", b"\x00" * 6),
			("src2", "6s", b"\x00" * 6),
			("frag_seq", "H", 0),
		)

		dst_s = pypacker.Packet._get_property_mac("dst")
		src1_s = pypacker.Packet._get_property_mac("src1")
		src2_s = pypacker.Packet._get_property_mac("src2")

	class DataframeQos(pypacker.Packet):
		__hdr__ = (
			("dst", "6s", b"\x00" * 6),
			("src1", "6s", b"\x00" * 6),
			("src2", "6s", b"\x00" * 6),
			("frag_seq", "H", 0),
			("qos_ctrl", "H", 0),
		)

		dst_s = pypacker.Packet._get_property_mac("dst")
		src1_s = pypacker.Packet._get_property_mac("src1")
		src2_s = pypacker.Packet._get_property_mac("src2")

	class DataframeSecured(pypacker.Packet):
		__hdr__ = (
			("dst", "6s", b"\x00" * 6),
			("src1", "6s", b"\x00" * 6),
			("src2", "6s", b"\x00" * 6),
			("frag_seq", "H", 0),
			("sec_param", "Q", 0),
		)

		dst_s = pypacker.Packet._get_property_mac("dst")
		src1_s = pypacker.Packet._get_property_mac("src1")
		src2_s = pypacker.Packet._get_property_mac("src2")

	class DataframeQosSecured(pypacker.Packet):
		__hdr__ = (
			("dst", "6s", b"\x00" * 6),
			("src1", "6s", b"\x00" * 6),
			("src2", "6s", b"\x00" * 6),
			("frag_seq", "H", 0),
			("qos_ctrl", "H", 0),
			("sec_param", "Q", 0),
		)

		dst_s = pypacker.Packet._get_property_mac("dst")
		src1_s = pypacker.Packet._get_property_mac("src1")
		src2_s = pypacker.Packet._get_property_mac("src2")

	d_decoder = {
		D_NORMAL		: Dataframe,
		D_DATA_CF_ACK		: Dataframe,
		D_DATA_CF_POLL 		: Dataframe,
		D_DATA_CF_ACK_POLL 	: Dataframe,
		D_NULL			: Dataframe,
		D_CF_ACK		: Dataframe,
		D_CF_POLL		: Dataframe,
		D_CF_ACK_POLL		: Dataframe,
		D_QOS_DATA		: DataframeQos,
		D_QOS_CF_ACK		: DataframeQos,
		D_QOS_CF_POLL		: DataframeQos,
		D_QOS_CF_ACK_POLL	: DataframeQos,
		D_QOS_NULL		: DataframeQos,
		D_QOS_CF_POLL_EMPTY	: DataframeQos
	}

	#
	# IEs for Mgmt-Frames
	#
	def _unpack_ies(buf):
		"""Parse IEs and return them as Triggerlist."""
		# each IE starts with an ID and a length
		ies = []
		off = 0
		buflen = len(buf)

		while off < buflen:
			ie_id = buf[off]
			try:
				parser = IEEE80211.ie_decoder[ie_id]
			except KeyError:
				# some unknown tag, use standard format
				parser = IEEE80211.IE

			dlen = buf[off + 1]
			#logger.debug("IE parser is: %d = %s = %s" % (ie_id, parser, buf[off: off+2+dlen]))
			ie = parser( buf[off: off + 2 + dlen])
			ies.append(ie)
			off += 2 + dlen

		return ies

	class IE(pypacker.Packet):
		__hdr__ = (
			("id", "B", 0),
			("len", "B", 0)
		)

	class FH(pypacker.Packet):
		__hdr__ = (
			("id", "B", 0),
			("len", "B", 0),
			("tu", "H", 0),
			("hopset", "B", 0),
			("hoppattern", "B", 0),
			("hopindex", "B", 0)
		)

	class DS(pypacker.Packet):
		__hdr__ = (
			("id", "B", 0),
			("len", "B", 0),
			("ch", "B", 0)
		)

	class CF(pypacker.Packet):
		__hdr__ = (
			("id", "B", 0),
			("len", "B", 0),
			("count", "B", 0),
			("period", "B", 0),
			("max", "H", 0),
			("dur", "H", 0)
		)

	class TIM(pypacker.Packet):
		__hdr__ = (
			("id", "B", 0),
			("len", "B", 0),
			("count", "B", 0),
			("period", "B", 0),
			("ctrl", "H", 0)
		)

	class IBSS(pypacker.Packet):
		__hdr__ = (
			("id", "B", 0),
			("len", "B", 0),
			("atim", "H", 0)
		)

	# IEs
	IE_SSID			= 0
	IE_RATES		= 1
	IE_FH			= 2
	IE_DS			= 3
	IE_CF			= 4
	IE_TIM			= 5
	IE_IBSS			= 6
	IE_HT_CAPA		= 45
	IE_ESR			= 50
	IE_HT_INFO		= 61

	ie_decoder = {
		IE_SSID		: IE,
		IE_RATES	: IE,
		IE_FH		: FH,
		IE_DS		: DS,
		IE_CF		: CF,
		IE_TIM		: TIM,
		IE_IBSS		: IBSS,
		IE_HT_CAPA	: IE,
		IE_ESR		: IE,
		IE_HT_INFO	: IE
	}



# position in list = type-ID
dicts			= [IEEE80211.m_decoder, IEEE80211.c_decoder, IEEE80211.d_decoder]
decoder_dict_complete	= {}

for pos, dict in enumerate(dicts):
	for key, val in dict.items():
		# same subtype-ID for different typ-IDs, distinguish via "type_factor + subtype)"
		decoder_dict_complete[TYPE_FACTORS[pos] + key] = val

		# add secured data frame versions for normal and QoS data
		if pos == 2:
			if val == IEEE80211.Dataframe:
				decoder_dict_complete[TYPE_FACTORS[2] + key + TYPE_FACTOR_PROTECTED] = IEEE80211.DataframeSecured
			elif val == IEEE80211.DataframeQos:
				decoder_dict_complete[TYPE_FACTORS[2] + key + TYPE_FACTOR_PROTECTED] = IEEE80211.DataframeQosSecured

pypacker.Packet.load_handler(IEEE80211, decoder_dict_complete)
