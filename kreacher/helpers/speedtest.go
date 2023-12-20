package helpers

import (
	st "github.com/showwin/speedtest-go/speedtest"
)

func Speedtest() *st.Server {
	var stc = st.New()

	// Use a proxy for the speedtest. eg: socks://127.0.0.1:7890
	// st.WithUserConfig(&speedtest.UserConfig{Proxy: "socks://127.0.0.1:7890"})(speedtestClient)

	// Select a network card as the data interface.
	// st.WithUserConfig(&speedtest.UserConfig{Source: "192.168.1.101"})(speedtestClient)

	// Get user's network information
	// user, _ := stc.FetchUserInfo()

	// Get a list of servers near a specified location
	// user.SetLocationByCity("Tokyo")
	// user.SetLocation("Osaka", 34.6952, 135.5006)

	// Search server using serverID.
	// eg: fetch server with ID 28910.
	// st.ErrServerNotFound will be returned if the server cannot be found.
	// server, err := st.FetchServerByID("28910")

	serverList, _ := stc.FetchServers()
	targets, _ := serverList.FindServer([]int{})

	for _, s := range targets {
		// Please make sure your host can access this test server,
		// otherwise you will get an error.
		// It is recommended to replace a server at this time
		s.PingTest(nil)
		s.DownloadTest()
		s.UploadTest()
		s.Context.Reset() // reset counter
		return s
	}

	return nil
}
