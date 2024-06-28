package logger

import (
	"path"

	"go.uber.org/zap"
	"go.uber.org/zap/zapcore"
	lj "gopkg.in/natefinch/lumberjack.v2"
)

func init() {
	logWriter := zapcore.AddSync(&lj.Logger{
		Filename: LogsPath,
		// MaxBackups: 3,
		// MaxSize:    1, // megabytes
		// MaxAge:     7, // days
	})

	logCore := zapcore.NewCore(
		zapcore.NewJSONEncoder(zap.NewProductionEncoderConfig()),
		logWriter,
		zap.DebugLevel,
	)

	T = zap.New(logCore)
	defer func() { _ = T.Sync() }()
}

var T = &zap.Logger{}
var LogsPath = path.Join("..", "logs", "bot.json")

// Info logger, redirect info to log file.
func Info(format string, v ...interface{}) {
	T.Sugar().Infof(format, v...)
}

// Warn logger, redirect warning to log file.
func Warn(format string, v ...interface{}) {
	T.Sugar().Warnf(format, v...)
}

// Error logger, redirect error to log file.
func Error(format error, v ...interface{}) {
	T.Sugar().Errorf(format.Error(), v...)
}
