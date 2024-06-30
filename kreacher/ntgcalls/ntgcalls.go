package ntgcalls

//#include <stdint.h>
//#include "ntgcalls.h"
//extern void handleStream(uint32_t uid, int64_t chatID, ntg_stream_type_enum streamType, void*);
//extern void handleUpgrade(uint32_t uid, int64_t chatID, ntg_media_state_struct state, void*);
//extern void handleConnectionChange(uint32_t uid, int64_t chatID, ntg_connection_state_enum state, void*);
//extern void handleSignal(uint32_t uid, int64_t chatID, uint8_t*, int, void*);
import "C"
import (
	"unsafe"
)

var handlerEnd = make(map[uint32][]StreamEndCallback)
var handlerUpgrade = make(map[uint32][]UpgradeCallback)
var handlerConnectionChange = make(map[uint32][]ConnectionChangeCallback)
var handlerSignal = make(map[uint32][]SignalCallback)

func NTgCalls() *Client {
	instance := &Client{
		uid:    uint32(C.ntg_init()),
		exists: true,
	}

	C.ntg_on_stream_end(C.uint32_t(instance.uid), (C.ntg_stream_callback)(unsafe.Pointer(C.handleStream)), nil)
	C.ntg_on_upgrade(C.uint32_t(instance.uid), (C.ntg_upgrade_callback)(unsafe.Pointer(C.handleUpgrade)), nil)
	C.ntg_on_signaling_data(C.uint32_t(instance.uid), (C.ntg_signaling_callback)(unsafe.Pointer(C.handleSignal)), nil)
	C.ntg_on_connection_change(C.uint32_t(instance.uid), (C.ntg_connection_callback)(unsafe.Pointer(C.handleConnectionChange)), nil)

	return instance
}

func (ctx *Client) OnStreamEnd(callback StreamEndCallback) {
	handlerEnd[ctx.uid] = append(handlerEnd[ctx.uid], callback)
}

func (ctx *Client) OnUpgrade(callback UpgradeCallback) {
	handlerUpgrade[ctx.uid] = append(handlerUpgrade[ctx.uid], callback)
}

func (ctx *Client) OnConnectionChange(callback ConnectionChangeCallback) {
	handlerConnectionChange[ctx.uid] = append(handlerConnectionChange[ctx.uid], callback)
}

func (ctx *Client) OnSignal(callback SignalCallback) {
	handlerSignal[ctx.uid] = append(handlerSignal[ctx.uid], callback)
}

func (ctx *Client) CreateCall(chatId int64, desc MediaDescription) (string, error) {
	var buffer [1024]C.char
	size := C.int(len(buffer))
	f := CreateFuture()
	C.ntg_create(C.uint32_t(ctx.uid), C.int64_t(chatId), desc.ParseToC(), &buffer[0], size, f.ParseToC())
	f.wait()

	return C.GoString(&buffer[0]), parseErrorCode(*f.errCode)
}

func (ctx *Client) SendSignalingData(chatId int64, data []byte) error {
	f := CreateFuture()
	dataC, dataSize := parseBytes(data)
	C.ntg_send_signaling_data(C.uint32_t(ctx.uid), C.int64_t(chatId), dataC, dataSize, f.ParseToC())
	f.wait()

	return parseErrorCode(*f.errCode)
}

func (ctx *Client) GetProtocol() Protocol {
	var buffer C.ntg_protocol_struct
	C.ntg_get_protocol(C.uint32_t(ctx.uid), &buffer)
	return Protocol{
		MinLayer:     int32(buffer.minLayer),
		MaxLayer:     int32(buffer.maxLayer),
		UdpP2P:       bool(buffer.udpP2P),
		UdpReflector: bool(buffer.udpReflector),
		Versions:     parseStringVector(unsafe.Pointer(buffer.libraryVersions), buffer.libraryVersionsSize),
	}
}

func (ctx *Client) Connect(chatId int64, params string) error {
	f := CreateFuture()
	C.ntg_connect(C.uint32_t(ctx.uid), C.int64_t(chatId), C.CString(params), f.ParseToC())
	f.wait()

	return parseErrorCode(*f.errCode)
}

func (ctx *Client) ChangeStream(chatId int64, desc MediaDescription) error {
	f := CreateFuture()
	C.ntg_change_stream(C.uint32_t(ctx.uid), C.int64_t(chatId), desc.ParseToC(), f.ParseToC())
	f.wait()

	return parseErrorCode(*f.errCode)
}

func (ctx *Client) Pause(chatId int64) (bool, error) {
	f := CreateFuture()
	C.ntg_pause(C.uint32_t(ctx.uid), C.int64_t(chatId), f.ParseToC())
	f.wait()

	return parseBool(*f.errCode)
}

func (ctx *Client) Resume(chatId int64) (bool, error) {
	f := CreateFuture()
	C.ntg_resume(C.uint32_t(ctx.uid), C.int64_t(chatId), f.ParseToC())
	f.wait()

	return parseBool(*f.errCode)
}

func (ctx *Client) Mute(chatId int64) (bool, error) {
	f := CreateFuture()
	C.ntg_mute(C.uint32_t(ctx.uid), C.int64_t(chatId), f.ParseToC())
	f.wait()

	return parseBool(*f.errCode)
}

func (ctx *Client) UnMute(chatId int64) (bool, error) {
	f := CreateFuture()
	C.ntg_unmute(C.uint32_t(ctx.uid), C.int64_t(chatId), f.ParseToC())
	f.wait()

	return parseBool(*f.errCode)
}

func (ctx *Client) Stop(chatId int64) error {
	f := CreateFuture()
	C.ntg_stop(C.uint32_t(ctx.uid), C.int64_t(chatId), f.ParseToC())
	f.wait()

	return parseErrorCode(*f.errCode)
}

func (ctx *Client) Time(chatId int64) (uint64, error) {
	f := CreateFuture()
	var buffer C.int64_t
	C.ntg_time(C.uint32_t(ctx.uid), C.int64_t(chatId), &buffer, f.ParseToC())
	f.wait()

	return uint64(buffer), parseErrorCode(*f.errCode)
}

func (ctx *Client) CpuUsage() (float64, error) {
	f := CreateFuture()
	var buffer C.double
	C.ntg_cpu_usage(C.uint32_t(ctx.uid), &buffer, f.ParseToC())
	f.wait()

	return float64(buffer), parseErrorCode(*f.errCode)
}

func (ctx *Client) Calls() map[int64]StreamStatus {
	mapReturn := make(map[int64]StreamStatus)

	f := CreateFuture()
	var callSize C.uint64_t
	_ = C.ntg_calls_count(C.uint32_t(ctx.uid), &callSize, f.ParseToC())
	f.wait()
	f = CreateFuture()
	buffer := make([]C.ntg_call_struct, callSize)
	if len(buffer) == 0 {
		return mapReturn
	}

	C.ntg_calls(C.uint32_t(ctx.uid), &buffer[0], callSize, f.ParseToC())
	f.wait()

	for _, call := range buffer {
		var goStreamType StreamStatus
		switch call.status {
		case C.NTG_PLAYING:
			goStreamType = PlayingStream
		case C.NTG_PAUSED:
			goStreamType = PausedStream
		case C.NTG_IDLING:
			goStreamType = IdlingStream
		}

		mapReturn[int64(call.chatId)] = goStreamType
	}

	return mapReturn
}

// This function is not yet fully functional
func (ctx *Client) SetLogger(fn func(string)) {
	C.ntg_register_logger((C.ntg_log_message_callback)(unsafe.Pointer(&fn)))
}

func Version() string {
	var buffer [8]C.char
	size := C.int(len(buffer))
	C.ntg_get_version(&buffer[0], size)

	return C.GoString(&buffer[0])
}

func (ctx *Client) Free() {
	C.ntg_destroy(C.uint32_t(ctx.uid))
	delete(handlerEnd, ctx.uid)
	delete(handlerUpgrade, ctx.uid)
	delete(handlerConnectionChange, ctx.uid)
	delete(handlerSignal, ctx.uid)
	ctx.exists = false
}
