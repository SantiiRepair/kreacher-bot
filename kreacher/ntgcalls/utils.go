package ntgcalls

//#include "ntgcalls.h"
import "C"
import (
	"fmt"
	"unsafe"
)

func parseBool(res C.int) (bool, error) {
	return res == 0, parseErrorCode(res)
}

func parseBytes(data []byte) (*C.uint8_t, C.int) {
	if len(data) > 0 {
		rawBytes := C.CBytes(data)
		return (*C.uint8_t)(rawBytes), C.int(len(data))
	}

	return nil, 0
}

func parseStringVector(data unsafe.Pointer, size C.int) []string {
	result := make([]string, size)
	for i := 0; i < int(size); i++ {
		result[i] = C.GoString(*(**C.char)(unsafe.Pointer(uintptr(data) + uintptr(i)*unsafe.Sizeof(uintptr(0)))))
	}
	return result
}

func parseStringVectorC(data []string) (**C.char, C.int) {
	result := make([]*C.char, len(data))
	for i, v := range data {
		result[i] = C.CString(v)
	}

	return &result[0], C.int(len(data))
}

func parseErrorCode(errorCode C.int) error {
	pErrorCode := int16(errorCode)
	switch pErrorCode {
	case -100:
		return fmt.Errorf("connection already made")
	case -101:
		return fmt.Errorf("connection not found")
	case -102:
		return fmt.Errorf("cryptation error")
	case -103:
		return fmt.Errorf("missing fingerprint")
	case -200:
		return fmt.Errorf("file not found")
	case -201:
		return fmt.Errorf("encoder not found")
	case -202:
		return fmt.Errorf("ffmpeg not found")
	case -203:
		return fmt.Errorf("error while executing shell command")
	case -300:
		return fmt.Errorf("rtmp needed")
	case -301:
		return fmt.Errorf("invalid transport")
	case -302:
		return fmt.Errorf("connection failed")
	}
	if pErrorCode >= 0 {
		return nil
	} else {
		return fmt.Errorf("unknown error")
	}
}

//export handleStream
func handleStream(uid C.uint32_t, chatID C.int64_t, streamType C.ntg_stream_type_enum, _ unsafe.Pointer) {
	goUID := uint32(uid)
	goChatID := int64(chatID)
	var goStreamType StreamType
	if streamType == C.NTG_STREAM_AUDIO {
		goStreamType = AudioStream
	} else {
		goStreamType = VideoStream
	}

	if handlerEnd[goUID] != nil {
		for _, x0 := range handlerEnd[goUID] {
			go x0(goChatID, goStreamType)
		}
	}
}

//export handleUpgrade
func handleUpgrade(uid C.uint32_t, chatID C.int64_t, state C.ntg_media_state_struct, _ unsafe.Pointer) {
	goChatID := int64(chatID)
	goUID := uint32(uid)
	goState := MediaState{
		Muted:        bool(state.muted),
		VideoPaused:  bool(state.videoPaused),
		VideoStopped: bool(state.videoStopped),
	}

	if handlerUpgrade[goUID] != nil {
		for _, x0 := range handlerUpgrade[goUID] {
			go x0(goChatID, goState)
		}
	}
}

//export handleSignal
func handleSignal(uid C.uint32_t, chatID C.int64_t, data *C.uint8_t, size C.int, _ unsafe.Pointer) {
	goChatID := int64(chatID)
	goUID := uint32(uid)
	if handlerSignal[goUID] != nil {
		for _, x0 := range handlerSignal[goUID] {
			go x0(goChatID, C.GoBytes(unsafe.Pointer(data), size))
		}
	}
}

//export handleConnectionChange
func handleConnectionChange(uid C.uint32_t, chatID C.int64_t, state C.ntg_connection_state_enum, _ unsafe.Pointer) {
	goChatID := int64(chatID)
	goUID := uint32(uid)
	var goState ConnectionState
	switch state {
	case C.NTG_STATE_CONNECTING:
		goState = Connecting
	case C.NTG_STATE_CONNECTED:
		goState = Connected
	case C.NTG_STATE_FAILED:
		goState = Failed
	case C.NTG_STATE_TIMEOUT:
		goState = Timeout
	case C.NTG_STATE_CLOSED:
		goState = Closed
	}

	if handlerConnectionChange[goUID] != nil {
		for _, x0 := range handlerConnectionChange[goUID] {
			go x0(goChatID, goState)
		}
	}
}
