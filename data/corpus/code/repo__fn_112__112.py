def start
      if(@sockets.size < 0)
        raise 'No sockets available for listening'
      elsif(!@runner.nil? && @runner.alive?)
        raise AlreadyRunning.new
      else
        @stop = false
        @runner = Thread.new{watch}
      end
    end