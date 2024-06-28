package logger

import (
	"path"

	"go.uber.org/zap"
	"go.uber.org/zap/zapcore"
	lj "gopkg.in/natefinch/lumberjack.v2"
)

func init() {
	writer := zapcore.AddSync(&lj.Logger{
		MaxBackups: 3,  // old log files to retain
		MaxSize:    10, // megabytes
		MaxAge:     7,  // days
		Filename:   LogsPath,
	})

	encoder := zapcore.NewJSONEncoder(zap.NewProductionEncoderConfig())
	core := zapcore.NewCore(encoder, writer, zap.DebugLevel)

	T = zap.New(core)
	defer func() { _ = T.Sync() }()
}

var T = &zap.Logger{}
var LogsPath = path.Join("..", "logs", "bot.json")

// Info logger, redirect info to log file.
func Info(msg string, v ...zapcore.Field) {
	T.Info(msg, v...)
}

// Warn logger, redirect warning to log file.
func Warn(msg string, v ...zapcore.Field) {
	T.Warn(msg, v...)
}

// Error logger, redirect error to log file.
func Error(msg string, v ...zapcore.Field) {
	T.Error(msg, v...)
}

// Infof logger, redirect info to log file.
func Infof(msg string, v ...interface{}) {
	T.Sugar().Infof(msg, v...)
}

// Warnf logger, redirect warning to log file.
func Warnf(msg string, v ...interface{}) {
	T.Sugar().Warnf(msg, v...)
}

// Errorf logger, redirect error to log file.
func Errorf(msg string, v ...interface{}) {
	T.Sugar().Errorf(msg, v...)
}
