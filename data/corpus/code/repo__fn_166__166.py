private function _createNewCell($pCoordinate)
	{
		$cell = $this->_cellCollection->addCacheData(
			$pCoordinate,
			new PHPExcel_Cell(
				NULL, 
				PHPExcel_Cell_DataType::TYPE_NULL, 
				$this
			)
		);
        $this->_cellCollectionIsSorted = false;

        // Coordinates
        $aCoordinates = PHPExcel_Cell::coordinateFromString($pCoordinate);
        if (PHPExcel_Cell::columnIndexFromString($this->_cachedHighestColumn) < PHPExcel_Cell::columnIndexFromString($aCoordinates[0]))
            $this->_cachedHighestColumn = $aCoordinates[0];
        $this->_cachedHighestRow = max($this->_cachedHighestRow, $aCoordinates[1]);

        // Cell needs appropriate xfIndex from dimensions records
		//    but don't create dimension records if they don't already exist
        $rowDimension    = $this->getRowDimension($aCoordinates[1], FALSE);
        $columnDimension = $this->getColumnDimension($aCoordinates[0], FALSE);

        if ($rowDimension !== NULL && $rowDimension->getXfIndex() > 0) {
            // then there is a row dimension with explicit style, assign it to the cell
            $cell->setXfIndex($rowDimension->getXfIndex());
        } elseif ($columnDimension !== NULL && $columnDimension->getXfIndex() > 0) {
            // then there is a column dimension, assign it to the cell
            $cell->setXfIndex($columnDimension->getXfIndex());
        }

        return $cell;
	}