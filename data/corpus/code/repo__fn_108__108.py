public function getSqlPaginateParams($pickedPage = false) {
        $p = new SqlPaginateParams();
        if ($pickedPage) {
            $this->pickedPage = $pickedPage;
        }
        if ($this->pages == 0) {
            $p->setOffset(0);
            $p->setLimit(20);
            return $p;
        }
        if ($this->pickedPage > $this->pages) {
            $this->pickedPage = $this->pages;
        }
        if ($this->pickedPage < 1) {
            $this->pickedPage = 1;
        }
        $p->setOffset($this->pickedPage * $this->elementsPerPage - $this->elementsPerPage);
        $p->setLimit($this->elementsPerPage);

        return $p;
    }