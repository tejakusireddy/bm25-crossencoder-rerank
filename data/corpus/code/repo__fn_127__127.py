public function link($page, $args = array())
    {
        $this->setElement('a');
        $this->setAttr('href', $this->app->url($page, $args));

        return $this;
    }