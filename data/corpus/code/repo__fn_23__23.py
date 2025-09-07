public static function trace($trace = null, $addObject = false)
    {
        if (!self::isDebug()) {
            return false;
        }

        $_this = self::i();

        $trace = $trace ? $trace : debug_backtrace($addObject);
        unset($trace[0]);

        $result = $_this->convertTrace($trace, $addObject);

        return $_this->dump($result, '! backtrace !');
    }