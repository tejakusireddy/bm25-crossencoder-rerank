func (nm *NodeMonitor) State() *models.MonitorStatus {
	nm.Mutex.RLock()
	state := nm.state
	nm.Mutex.RUnlock()
	return state
}