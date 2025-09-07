func (e *Engine) fullCompactionStrategy(group CompactionGroup, optimize bool) *compactionStrategy {
	s := &compactionStrategy{
		group:     group,
		logger:    e.logger.With(zap.String("tsm1_strategy", "full"), zap.Bool("tsm1_optimize", optimize)),
		fileStore: e.FileStore,
		compactor: e.Compactor,
		fast:      optimize,
		engine:    e,
		level:     5,
		tracker:   e.compactionTracker,
	}

	if optimize {
		s.level = 4
	}
	return s
}