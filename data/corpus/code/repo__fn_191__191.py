public function skipDiscounts()
    {
        // already loaded skip discounts config
        if ($this->_blSkipDiscounts !== null) {
            return $this->_blSkipDiscounts;
        }

        if ($this->oxarticles__oxskipdiscounts->value) {
            return true;
        }


        $this->_blSkipDiscounts = false;
        if (\OxidEsales\Eshop\Core\Registry::get(\OxidEsales\Eshop\Application\Model\DiscountList::class)->hasSkipDiscountCategories()) {
            $oDb = \OxidEsales\Eshop\Core\DatabaseProvider::getDb();
            $sO2CView = getViewName('oxobject2category', $this->getLanguage());
            $sViewName = getViewName('oxcategories', $this->getLanguage());
            $sSelect = "select 1 from $sO2CView as $sO2CView left join {$sViewName} on {$sViewName}.oxid = $sO2CView.oxcatnid
                         where $sO2CView.oxobjectid=" . $oDb->quote($this->getId()) . " and {$sViewName}.oxactive = 1 and {$sViewName}.oxskipdiscounts = '1' ";
            $this->_blSkipDiscounts = ($oDb->getOne($sSelect) == 1);
        }

        return $this->_blSkipDiscounts;
    }